#!/usr/bin/env bash
# Deploy guardian CLAUDE.md to root.
#
# The root CLAUDE.md is gitignored rendered output. The source of
# truth is .guardian/CLAUDE.md. This script copies the source to
# the root at session-launch time.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "${DIR}")"

cp "${DIR}/CLAUDE.md" "${ROOT}/CLAUDE.md"
echo "Deployed .guardian/CLAUDE.md → CLAUDE.md"
