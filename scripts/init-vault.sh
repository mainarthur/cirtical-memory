#!/usr/bin/env bash
#
# init-vault.sh: Bootstrap a memdoc (memory + documentation) vault in a project directory.
# Usage: ./init-vault.sh [TARGET_DIR] [PROJECT_NAME]
# Default TARGET_DIR: ./docs/obsidian
# Default PROJECT_NAME: Current directory basename

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TEMPLATES_DIR="${REPO_ROOT}/templates"

TARGET_DIR="${1:-docs/obsidian}"
CURRENT_DIR_NAME="$(basename "$(pwd)")"
PROJECT_NAME="${2:-$CURRENT_DIR_NAME}"
TODAY="$(date +%Y-%m-%d)"

echo "Initializing Memdoc Vault..."
echo "  Target: ${TARGET_DIR}"
echo "  Project: ${PROJECT_NAME}"
echo "  Date: ${TODAY}"

mkdir -p "${TARGET_DIR}/docs"
mkdir -p "${TARGET_DIR}/tasks/items"

render_template() {
  local src="$1"
  local dest="$2"
  if [ -f "${dest}" ]; then
    echo "  [skip] ${dest} already exists"
  else
    sed -e "s/{{PROJECT_NAME}}/${PROJECT_NAME}/g" \
        -e "s/{{DATE}}/${TODAY}/g" \
        "${src}" > "${dest}"
    echo "  [created] ${dest}"
  fi
}

render_template "${TEMPLATES_DIR}/Index.md" "${TARGET_DIR}/Index.md"
render_template "${TEMPLATES_DIR}/docs/Architecture.md" "${TARGET_DIR}/docs/Architecture.md"
render_template "${TEMPLATES_DIR}/docs/Setup-and-Usage.md" "${TARGET_DIR}/docs/Setup-and-Usage.md"
render_template "${TEMPLATES_DIR}/docs/Decisions.md" "${TARGET_DIR}/docs/Decisions.md"
render_template "${TEMPLATES_DIR}/docs/ADR-template.md" "${TARGET_DIR}/docs/ADR-template.md"
render_template "${TEMPLATES_DIR}/tasks/Kanban-Board.base" "${TARGET_DIR}/tasks/Kanban-Board.base"
render_template "${TEMPLATES_DIR}/tasks/prompts-log.md" "${TARGET_DIR}/tasks/prompts-log.md"
render_template "${TEMPLATES_DIR}/tasks/items/task-template.md" "${TARGET_DIR}/tasks/items/task-template.md"
render_template "${TEMPLATES_DIR}/AGENTS.md" "${TARGET_DIR}/AGENTS.md"

if [ ! -f "AGENTS.md" ] && [ "${TARGET_DIR}" != "." ]; then
  cp "${TARGET_DIR}/AGENTS.md" "AGENTS.md"
  echo "  [created] Root AGENTS.md (Universal GenAI agent instructions)"
fi

echo "Critical Memory vault initialized successfully at: ${TARGET_DIR}"

