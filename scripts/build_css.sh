#!/usr/bin/env bash
# Build the Tailwind CSS bundle. Pass --watch to rebuild on change during dev.
# The output (greengold/static/css/site.css) is committed so the Docker image
# does not need Node or the Tailwind binary.
set -euo pipefail
cd "$(dirname "$0")/.."

BIN=./tailwindcss
if [ ! -x "$BIN" ]; then
  echo "Tailwind standalone CLI not found at $BIN."
  echo "Download it for your platform from:"
  echo "  https://github.com/tailwindlabs/tailwindcss/releases (v3.4.x, e.g. tailwindcss-macos-x64)"
  echo "then: chmod +x tailwindcss"
  exit 1
fi

ARGS="-c tailwind.config.js -i theme/src/input.css -o greengold/static/css/site.css"
if [ "${1:-}" = "--watch" ]; then
  exec "$BIN" $ARGS --watch
else
  "$BIN" $ARGS --minify
  echo "Built greengold/static/css/site.css"
fi
