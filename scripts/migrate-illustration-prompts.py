#!/usr/bin/env python3
"""
Migrate EduMost Illustration Prompts out of lab Markdown into prompts/ILL-*.md
Replace lab blocks with :::illustration fences.
"""
from __future__ import annotations

import re
from pathlib import Path

ILL_ID_RE = re.compile(r"ILL-T\d+-L\d+-\d+")
ARTIST_START_RE = re.compile(r"^📷\s*\*\*\[Для художника\]\*\*", re.M)
SECTION_RE = re.compile(r"^## 📷 Иллюстрация\s*\n", re.M)
NEXT_H2_RE = re.compile(r"^## ", re.M)

BOOKS_ROOT = Path("/Users/marinatarasenko/Documents/EduMost-Books")
ROADMAP_ROOT = Path("/Users/marinatarasenko/Documents/ENGINEERING_ROADMAP")

BOOK_MAP = [
    ("TOM_01_OSNOVY", "engineering-roadmap-tom-01"),
    ("TOM_02_ELEKTRONIKA", "engineering-roadmap-tom-02"),
    ("TOM_03_SISTEMNY_INZHENER", "engineering-roadmap-tom-03"),
    ("TOM_04_ROBOTOTEHNIKA", "engineering-roadmap-tom-04"),
    ("TOM_05_INZHENER_BUDUSCHEGO", "engineering-roadmap-tom-05"),
]


def extract_id(block: str) -> str | None:
    m = re.search(r"\*\*ID:\*\*\s*\n\s*(ILL-T\d+-L\d+-\d+)", block)
    if m:
        return m.group(1)
    m = ILL_ID_RE.search(block)
    return m.group(0) if m else None


def split_illustration_section(text: str) -> tuple[str, str, str] | None:
    """Return (before, section_body, after) for ## 📷 Иллюстрация … next ##."""
    m = SECTION_RE.search(text)
    if not m:
        return None
    start = m.end()
    # section includes the heading
    heading_start = m.start()
    rest = text[start:]
    nm = NEXT_H2_RE.search(rest)
    if nm:
        body = rest[: nm.start()]
        after = rest[nm.start() :]
    else:
        body = rest
        after = ""
    before = text[:heading_start]
    return before, body, after


def extract_artist_blocks(body: str) -> list[tuple[str, str]]:
    """Return list of (id, full_block_text including 📷 header)."""
    blocks: list[tuple[str, str]] = []
    starts = list(ARTIST_START_RE.finditer(body))
    if not starts:
        return blocks

    for i, sm in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        # Don't eat trailing ASCII fences that are NOT part of prompt —
        # but ASCII after prompt is usually AFTER the whole artist section.
        # Artist block ends at next artist start OR at a fenced ASCII that
        # starts after "Связь с лабораторией" / end of prompt.
        raw = body[sm.start() : end].rstrip()
        # Trim trailing blank lines and standalone ASCII code fences that follow prompt
        # Keep everything that is the prompt; strip only trailing ```...``` if after negative/связь
        ill_id = extract_id(raw)
        if not ill_id:
            continue
        # Remove leading 📷 line for file content? Keep full artist spec as-is
        # File should be the full EduMost Illustration Prompt — keep from 📷 line
        blocks.append((ill_id, raw.strip() + "\n"))
    return blocks


def strip_artist_keep_ascii(body: str) -> str:
    """Remove artist prompt blocks; keep ASCII/code fences and other notes."""
    starts = list(ARTIST_START_RE.finditer(body))
    if not starts:
        return body

    parts: list[str] = []
    cursor = 0
    for i, sm in enumerate(starts):
        parts.append(body[cursor : sm.start()])
        end = starts[i + 1].start() if i + 1 < len(starts) else len(body)
        chunk = body[sm.start() : end]
        # After "Связь с лабораторией" section, trailing ``` ascii may remain —
        # find last --- after Связь or end of prompt fields, then keep code fences
        # Simpler: remove from 📷 to just before a line that is only ```
        # if that fence is NOT inside the prompt (prompts don't use ``` usually)
        # Most prompts don't contain ```. Find first ``` after artist start as ASCII keep.
        fence = re.search(r"\n```", chunk)
        if fence:
            parts.append(chunk[fence.start() :])  # keep ASCII
        # else drop entire chunk
        cursor = end
    parts.append(body[cursor:])
    return "".join(parts)


def build_fence_section(ids: list[str], leftover: str) -> str:
    fences = []
    for ill_id in ids:
        fences.append(f":::illustration\n{ill_id}\n:::")
    body = "\n\n".join(fences)
    leftover = leftover.strip()
    if leftover:
        body = body + "\n\n" + leftover
    return f"## 📷 Иллюстрация\n\n{body}\n\n"


def migrate_file(path: Path, prompts_dir: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    split = split_illustration_section(text)
    if not split:
        return []

    before, body, after = split
    written: list[str] = []

    # Already only fences?
    existing_ids = ILL_ID_RE.findall(
        "\n".join(re.findall(r":::illustration\s*\n(.*?)\n:::", body, re.S))
    )
    artist_blocks = extract_artist_blocks(body)

    if artist_blocks:
        for ill_id, block in artist_blocks:
            prompts_dir.mkdir(parents=True, exist_ok=True)
            # Normalize: ensure starts with artist header
            content = block
            if not content.startswith("📷"):
                content = "📷 **[Для художника]**\n\n" + content
            (prompts_dir / f"{ill_id}.md").write_text(content, encoding="utf-8")
            written.append(ill_id)

        leftover = strip_artist_keep_ascii(body)
        # Also remove any leftover :::illustration duplicates we're rewriting
        leftover = re.sub(r":::illustration\s*\n.*?\n:::\s*", "", leftover, flags=re.S)
        ids = [i for i, _ in artist_blocks]
        # Preserve order, unique
        seen = set()
        ordered = []
        for i in ids:
            if i not in seen:
                seen.add(i)
                ordered.append(i)
        new_section = build_fence_section(ordered, leftover)
        path.write_text(before + new_section + after, encoding="utf-8")
        return written

    # No artist blocks — ensure prompts exist from nowhere; just collect fence IDs
    if existing_ids:
        return existing_ids
    return []


def migrate_tree(content_glob: Path, prompts_dir: Path) -> dict[str, int]:
    stats = {"files": 0, "prompts": 0}
    for md in sorted(content_glob.glob("*_LAB_*.md")):
        ids = migrate_file(md, prompts_dir)
        if ids:
            stats["files"] += 1
            stats["prompts"] += len(ids)
    return stats


def main() -> None:
    total_prompts = 0
    # 1) ENGINEERING_ROADMAP (canonical author source)
    for tom_folder, book_id in BOOK_MAP:
        src = ROADMAP_ROOT / tom_folder
        prompts = src / "prompts"
        st = migrate_tree(src, prompts)
        print(f"ROADMAP {tom_folder}: files={st['files']} prompts={st['prompts']} → {prompts}")
        total_prompts += st["prompts"]

        # Copy prompts + migrated labs to EduMost-Books
        book = BOOKS_ROOT / book_id
        vol = book_id.replace("engineering-roadmap-", "")  # tom-01
        # volume path is tom-01 etc from book.toml
        m = re.search(r"tom-(\d+)", book_id)
        vol_path = f"tom-{m.group(1)}" if m else "tom-01"
        dst_content = book / "ru" / vol_path / "content"
        dst_prompts = book / "prompts"
        dst_prompts.mkdir(parents=True, exist_ok=True)

        for p in sorted(prompts.glob("ILL-*.md")):
            (dst_prompts / p.name).write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

        for md in sorted(src.glob("*_LAB_*.md")):
            dst = dst_content / md.name
            if dst.parent.exists():
                dst.write_text(md.read_text(encoding="utf-8"), encoding="utf-8")

        print(f"  synced → {book_id}/prompts ({len(list(dst_prompts.glob('ILL-*.md')))} files)")

    # 2) Catch any remaining artist blocks only in Books (e.g. already-fence tom1 labs)
    for _, book_id in BOOK_MAP:
        book = BOOKS_ROOT / book_id
        m = re.search(r"tom-(\d+)", book_id)
        vol_path = f"tom-{m.group(1)}" if m else "tom-01"
        content = book / "ru" / vol_path / "content"
        prompts = book / "prompts"
        st = migrate_tree(content, prompts)
        if st["prompts"]:
            print(f"BOOKS leftover {book_id}: {st}")

    # Report missing prompts for fences
    missing = []
    for _, book_id in BOOK_MAP:
        book = BOOKS_ROOT / book_id
        m = re.search(r"tom-(\d+)", book_id)
        vol_path = f"tom-{m.group(1)}" if m else "tom-01"
        content = book / "ru" / vol_path / "content"
        prompts = book / "prompts"
        for md in content.glob("*_LAB_*.md"):
            text = md.read_text(encoding="utf-8")
            for ill_id in re.findall(r":::illustration\s*\n\s*(ILL-T\d+-L\d+-\d+)\s*\n:::", text):
                if not (prompts / f"{ill_id}.md").exists():
                    missing.append(f"{book_id}:{ill_id}")
        # leftover artist?
        arts = list(ARTIST_START_RE.finditer("\n".join(p.read_text() for p in content.glob("*.md"))))
    print(f"Missing prompts for fences: {len(missing)}")
    for x in missing[:20]:
        print(" ", x)

    # Count final
    for _, book_id in BOOK_MAP:
        n = len(list((BOOKS_ROOT / book_id / "prompts").glob("ILL-*.md")))
        arts = 0
        m = re.search(r"tom-(\d+)", book_id)
        vol_path = f"tom-{m.group(1)}" if m else "tom-01"
        for md in (BOOKS_ROOT / book_id / "ru" / vol_path / "content").glob("*.md"):
            arts += len(ARTIST_START_RE.findall(md.read_text(encoding="utf-8")))
        fences = 0
        for md in (BOOKS_ROOT / book_id / "ru" / vol_path / "content").glob("*.md"):
            fences += len(re.findall(r":::illustration", md.read_text(encoding="utf-8")))
        print(f"{book_id}: prompts={n} fences={fences} artist_left_in_labs={arts}")


if __name__ == "__main__":
    main()
