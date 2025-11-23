#!/bin/bash

# Directory of the repository to pull. Change if needed.
REPO_DIR="/workspaces/Lauzhack2025-SBB"
# Pull interval in seconds. Can be overridden by environment variable.
PULL_INTERVAL="${PULL_INTERVAL:-5}"
# Timezone to use for demo-window checks. Default is CET/CEST zone (Europe/Zurich).
DEMO_TZ="${DEMO_TZ:-Europe/Zurich}"

trap 'echo "[autopull] exiting"; exit 0' SIGINT SIGTERM

while true; do
  # Current time in demo timezone in HHMM as a decimal (avoid leading-zero octal)
  now=$((10#$(TZ="$DEMO_TZ" date +%H%M)))

  # If current time in DEMO_TZ is within the demo window (11:40 <= time < 11:50), exit so it does not restart.
  # if (( now >= 1140 && now < 1150 )); then
  #   echo "[autopull] Within demo window (11:40-11:50 ${DEMO_TZ}). Exiting to avoid interference with demo."
  #   exit 0
  # fi

  # Run git pull to update the repository
  echo "[autopull] Running git -C '$REPO_DIR' pull"
  git -C "$REPO_DIR" pull || echo "[autopull] git pull failed"

  gh codespace ports visibility 8000:public --codespace "opulent-fishstick-6q7q69xqgpjhwwj"
  sleep "$PULL_INTERVAL"
done