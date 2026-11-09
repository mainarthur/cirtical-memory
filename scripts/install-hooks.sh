#!/usr/bin/env bash
#
# install-hooks.sh: Install a Git pre-commit hook that runs validate-vault.py
# whenever vault files (docs/obsidian/ or .memdoc/) are staged.
# Usage: ./scripts/install-hooks.sh [TARGET_REPO_DIR]

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VALIDATOR_SCRIPT="${SCRIPT_DIR}/validate-vault.py"
TARGET_REPO="${1:-$(pwd)}"
HOOKS_DIR="${TARGET_REPO}/.git/hooks"
PRE_COMMIT_HOOK="${HOOKS_DIR}/pre-commit"

if [ ! -d "${TARGET_REPO}/.git" ]; then
  echo "Error: ${TARGET_REPO} is not a Git repository (.git directory not found)."
  exit 1
fi

mkdir -p "${HOOKS_DIR}"

cat << 'EOF' > "${PRE_COMMIT_HOOK}"
#!/usr/bin/env bash
# Critical Memory Pre-Commit Hook — Deterministic Vault Validation
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
VALIDATOR="${REPO_ROOT}/scripts/validate-vault.py"

if [ ! -f "${VALIDATOR}" ]; then
  exit 0
fi

VAULT_DIR=""
if [ -d "${REPO_ROOT}/docs/obsidian" ]; then
  VAULT_DIR="${REPO_ROOT}/docs/obsidian"
elif [ -d "${REPO_ROOT}/.memdoc" ]; then
  VAULT_DIR="${REPO_ROOT}/.memdoc"
fi

if [ -n "${VAULT_DIR}" ]; then
  echo "[Critical Memory] Validating vault integrity..."
  python3 "${VALIDATOR}" "${VAULT_DIR}"
fi
EOF

chmod +x "${PRE_COMMIT_HOOK}"
chmod +x "${VALIDATOR_SCRIPT}"

echo "✅ Installed Critical Memory Git pre-commit hook at: ${PRE_COMMIT_HOOK}"
