#!/usr/bin/env bash
#
# run.sh: Convenient launcher for the Critical Memory Benchmark Suite.
# Standard Usage: ./benchmark/run.sh [--scenario <scenario_id>] [--sprints <N>]
# Live Agent Usage: ./benchmark/run.sh --live-agent [--models <gemini|claude|all>] [--scenario <id>]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

IS_LIVE=false
ARGS=()

for arg in "$@"; do
  if [ "$arg" == "--live-agent" ]; then
    IS_LIVE=true
  else
    ARGS+=("$arg")
  fi
done

if [ "$IS_LIVE" = true ]; then
  python3 -m benchmark.live_runner "${ARGS[@]}"
else
  python3 -m benchmark.runner "$@"
fi
