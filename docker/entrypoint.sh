#!/bin/sh
# AstraIX backend entrypoint
#
# Seeds the persistent knowledge-base volume (/app/knowledge-base) from the
# immutable image copy (/opt/astraix-kb) on first boot. Because the KB is
# baked into the image, it survives host-side file deletions/quarantines
# and lives entirely inside the Docker sandbox.
set -e

KB_DIR=/app/knowledge-base
SEED=/opt/astraix-kb

if [ -d "$SEED" ] && [ ! -s "$KB_DIR/embeddings/chunks.json" ]; then
  echo "[astraix-entrypoint] Seeding knowledge base from image into $KB_DIR ..."
  mkdir -p "$KB_DIR"
  cp -a "$SEED/." "$KB_DIR/"
  echo "[astraix-entrypoint] Seeded $(find "$KB_DIR" -type f | wc -l | tr -d ' ') KB files."
fi

# KB_SYNC_REPOS=true: re-pull every manifest source repo straight into the
# container (kb-data volume). Content still never touches the host.
if [ "$KB_SYNC_REPOS" = "true" ] && [ -x /usr/local/bin/kb-pull ] && [ -f /kb-repos.txt ]; then
  echo "[astraix-entrypoint] Syncing KB source repos from manifest ..."
  while IFS='=' read -r name url; do
    case "$name" in "" | \#*) continue ;; esac
    [ -n "$url" ] || continue
    /usr/local/bin/kb-pull "$url" "$name" "$KB_DIR" || \
      echo "[astraix-entrypoint] kb-pull failed for $name (skipped)"
  done < /kb-repos.txt
  echo "[astraix-entrypoint] KB repo sync complete."
fi

exec "$@"
