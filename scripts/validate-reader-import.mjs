#!/usr/bin/env node
/**
 * Reader import validation (no code changes to Reader).
 * Simulates extractBookZip + openBook page discovery from release ZIPs.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import JSZip from "jszip";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const RELEASES = path.join(ROOT, "releases");

function parseBookToml(raw) {
  const getQuoted = (key) => raw.match(new RegExp(`^${key}\\s*=\\s*"([^"]*)"`, "m"))?.[1];
  const defaultLocale = getQuoted("defaultLocale") ?? getQuoted("sourceLocale") ?? "ru";
  const volumes = [];
  const re = /\[\[volumes\]\]\s*\n([\s\S]*?)(?=\n\[\[|$)/g;
  let m;
  while ((m = re.exec(raw)) !== null) {
    const block = m[1];
    const getVol = (key) => block.match(new RegExp(`^${key}\\s*=\\s*"([^"]*)"`, "m"))?.[1];
    volumes.push({
      id: getVol("id") ?? `vol-${volumes.length + 1}`,
      path: getVol("path") ?? "tom-01",
      title: getVol("title") ?? "",
    });
  }
  return {
    id: getQuoted("id") ?? "book",
    title: getQuoted("title") ?? "Book",
    defaultLocale,
    volumes,
  };
}

function contentDirForVolume(manifest, volume, locale) {
  const loc = locale ?? manifest.defaultLocale;
  return `${loc}/${volume.path}/content`;
}

function firstPagePath(paths) {
  const md = paths.filter((p) => p.endsWith(".md") && !/\/readme/i.test(p));
  md.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
  return md[0] ?? null;
}

async function validateZipBuffer(label, buffer) {
  const zip = await JSZip.loadAsync(buffer);
  const entries = Object.entries(zip.files).filter(([, e]) => !e.dir);
  const names = entries.map(([p]) => p.replace(/\\/g, "/"));
  const bookToml = names.filter((p) => p === "book.toml" || p.endsWith("/book.toml"));
  if (!bookToml.length) return { ok: false, error: "NO_BOOK_TOML" };
  bookToml.sort((a, b) => a.split("/").length - b.split("/").length);
  const root = bookToml[0].endsWith("book.toml")
    ? bookToml[0].slice(0, -"book.toml".length)
    : "";
  const relPaths = names
    .filter((p) => p.startsWith(root))
    .map((p) => p.slice(root.length))
    .filter(Boolean);

  const tomlRaw = await zip.file(bookToml[0]).async("string");
  const manifest = parseBookToml(tomlRaw);
  const locale = manifest.defaultLocale;

  let tocCount = 0;
  let firstPage = null;
  for (const vol of manifest.volumes) {
    const dir = contentDirForVolume(manifest, vol, locale);
    const pages = relPaths.filter((p) => p.startsWith(`${dir}/`) && p.endsWith(".md"));
    tocCount += pages.length;
    if (!firstPage) firstPage = firstPagePath(pages);
  }

  const svgCount = relPaths.filter((p) => p.endsWith(".svg")).length;
  const hasLib = relPaths.includes("metadata/library.json");

  return {
    ok: tocCount >= 10 && !!firstPage,
    label,
    id: manifest.id,
    title: manifest.title,
    tocCount,
    firstPage,
    svgCount,
    hasLib,
  };
}

async function validateLocalZip(zipPath) {
  const buffer = fs.readFileSync(zipPath);
  return validateZipBuffer(path.basename(zipPath), buffer);
}

async function validateRemoteZip(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buffer = Buffer.from(await res.arrayBuffer());
  return validateZipBuffer(url, buffer);
}

const books = ["01", "02", "03", "04", "05"];
const rows = [];

for (const num of books) {
  const id = `engineering-roadmap-tom-${num}`;
  const zipPath = path.join(RELEASES, `${id}.zip`);
  const local = await validateLocalZip(zipPath);
  const url = `https://github.com/edumost-pl/edumost-books/blob/main/releases/${id}.zip`;
  const rawUrl = `https://raw.githubusercontent.com/edumost-pl/edumost-books/main/releases/${id}.zip`;
  let remote = { ok: false, error: "" };
  try {
    remote = await validateRemoteZip(rawUrl);
  } catch (e) {
    remote = { ok: false, error: String(e.message ?? e) };
  }
  rows.push({ tom: `Tom ${Number(num)}`, local, remote, url });
}

console.log(JSON.stringify(rows, null, 2));
