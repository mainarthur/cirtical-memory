#!/usr/bin/env bash
#
# run.sh: Convenient launcher for the Critical Memory Benchmark Suite.
# Usage: ./benchmark/run.sh [--scenario <scenario_id>] [--format <markdown|json|both>]
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

export PYTHONPATH="${REPO_ROOT}:${PYTHONPATH:-}"

python3 -m benchmark.runner "$@"
