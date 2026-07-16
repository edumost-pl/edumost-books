#!/usr/bin/env bash
# Create Reader-ready release ZIPs from source book folders.
# Usage: ./scripts/make-releases.sh [tom-01|tom-02|...|all]

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
RELEASES="$ROOT/releases"
mkdir -p "$RELEASES"

pack_one() {
  local id="$1"
  local src="$ROOT/$id"
  local out="$RELEASES/$id.zip"
  if [[ ! -f "$src/book.toml" ]]; then
    echo "Skip $id — no book.toml" >&2
    return 1
  fi
  rm -f "$out"
  (cd "$src" && zip -r -q "$out" . \
    -x "*.DS_Store" \
    -x "__MACOSX/*" \
    -x "prompts/*" \
    -x "prompts/**")
  echo "Created $out ($(du -h "$out" | cut -f1))"
}

target="${1:-all}"
if [[ "$target" == "all" ]]; then
  for dir in "$ROOT"/engineering-roadmap-tom-*/; do
    pack_one "$(basename "$dir")"
  done
else
  pack_one "$target"
fi
