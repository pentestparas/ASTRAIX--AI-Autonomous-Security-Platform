#!/bin/sh
# Runtime KB puller: clones one source repo DIRECTLY inside the container into
# the live kb volume (/app/knowledge-base/sources/<name>). Content never
# touches the host filesystem. Use for ad-hoc KB additions:
#
#   docker exec astraix-backend kb-pull <github-url> [source-dir-name]
#
# or set KB_SYNC_REPOS=true on the backend to re-pull the whole manifest on boot.
set -e

URL="${1:?usage: kb-pull <github-url> [source-dir-name] [kb-dir]}"
NAME="${2:-$(basename "$URL" | sed 's/\.git$//')}"
KB="${3:-/app/knowledge-base}"
DEST="$KB/sources/$NAME"
TMP=/tmp/kb-pull

echo "[kb-pull] fetching $NAME <- $URL straight into $DEST"
mkdir -p "$TMP" "$(dirname "$DEST")"
rm -rf "$TMP/$NAME"
git clone --depth 1 --quiet "$URL" "$TMP/$NAME"
rm -rf "$TMP/$NAME/.git"
rm -rf "$DEST"
cp -a "$TMP/$NAME" "$DEST"
rm -rf "$TMP/$NAME"

COUNT=$(find "$DEST" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "[kb-pull] done: $COUNT files in $DEST"