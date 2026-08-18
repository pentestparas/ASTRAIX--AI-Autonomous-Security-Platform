#!/bin/sh
# Build-time KB fetcher: clones every repo in the manifest straight into the
# image (/opt/astraix-kb/sources/<name>). The content lives only in the Docker
# layer filesystem — never on the host, where AV quarantines payload files.
#
#   usage: fetch-kb <manifest> <dest-sources-dir>
#
# Manifest line formats (docker/kb-repos.txt):
#   name=repo-url            git clone INSIDE the build -> sources/<name>/
#   doc:name=https://...     curl webpage -> html-to-text -> sources/<name>.md
set -e

MANIFEST="${1:?usage: fetch-kb <manifest> <dest-sources-dir>}"
DEST="${2:?usage: fetch-kb <manifest> <dest-sources-dir>}"
TMP=/tmp/kb-fetch

mkdir -p "$DEST" "$TMP"

while IFS='=' read -r name url; do
  case "$name" in "" | \#*) continue ;; esac
  if [ -z "$url" ]; then
    echo "[kb] skipping $name (no url)"
    continue
  fi
  case "$name" in
    doc:*)
      n="${name#doc:}"
      echo "[kb] doc $n <- $url"
      rm -f "$DEST/$n.md"
      curl -fsSL --max-time 90 -A "astraix-kb-fetch/1.0" "$url" \
        | python3 -c '
import html, re, sys
raw = sys.stdin.buffer.read().decode("utf-8", "ignore")
raw = re.sub(r"(?is)<(script|style|noscript|svg|iframe)[^>]*>.*?</\1>", " ", raw)
raw = re.sub(r"(?is)<br\s*/?>", "\n", raw)
raw = re.sub(r"(?is)<[^>]+>", " ", raw)
raw = html.unescape(raw)
raw = re.sub(r"[ \t\r]+", " ", raw)
raw = re.sub(r"\n\s*\n+", "\n\n", raw)
print(raw.strip())
' > "$DEST/$n.md" || echo "[kb] doc fetch FAILED for $n (skipped)"
      continue
      ;;
  esac
  echo "[kb] cloning $name <- $url"
  rm -rf "$TMP/$name"
  git clone --depth 1 --quiet "$url" "$TMP/$name"
  rm -rf "$TMP/$name/.git"
  rm -rf "$DEST/$name"
  cp -a "$TMP/$name" "$DEST/$name"
  rm -rf "$TMP/$name"
done < "$MANIFEST"

echo "[kb] fetched $(ls "$DEST" | wc -l | tr -d ' ') source dirs into $DEST"