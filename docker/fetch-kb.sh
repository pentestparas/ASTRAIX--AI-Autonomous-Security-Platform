#!/bin/sh
# Build-time KB fetcher: clones every repo in the manifest straight into the
# image (/opt/astraix-kb/sources/<name>). The content lives only in the Docker
# layer filesystem — never on the host, where AV quarantines payload files.
#
#   usage: fetch-kb <manifest> <dest-sources-dir>
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
  echo "[kb] cloning $name <- $url"
  rm -rf "$TMP/$name"
  git clone --depth 1 --quiet "$url" "$TMP/$name"
  rm -rf "$TMP/$name/.git"
  rm -rf "$DEST/$name"
  cp -a "$TMP/$name" "$DEST/$name"
  rm -rf "$TMP/$name"
done < "$MANIFEST"

echo "[kb] fetched $(ls "$DEST" | wc -l | tr -d ' ') source dirs into $DEST"