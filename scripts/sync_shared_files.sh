#!/bin/bash
# Sync shared files between ChronosAtlas and docs/Chronos-Atlas
# Usage: ./scripts/sync_shared_files.sh

set -e

# List of files to sync (relative to ChronosAtlas root)
FILES=(
  "docs/PROJECT_EXECUTION_PLAN.md"
  "docs/README_DETAILED.md"
  "README.md"
)

for file in "${FILES[@]}"; do
  dest="docs/Chronos-Atlas/$(basename $file)"
  if [ -f "$file" ]; then
    cp -u "$file" "$dest"
    echo "Synced $file -> $dest"
  fi
  # If symlink exists, skip
  if [ -L "$dest" ]; then
    echo "$dest is a symlink, skipping copy."
  fi

done
