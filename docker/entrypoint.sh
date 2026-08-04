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

exec "$@"
