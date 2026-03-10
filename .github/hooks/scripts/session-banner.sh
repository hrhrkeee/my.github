#!/usr/bin/env bash
set -euo pipefail
cat <<'EOF'
COPILOT POLICY ACTIVE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Repository strategy files are active
- Do not push unless explicitly requested
- Update docs/tests/diagrams with behavior changes
- Work on a safe branch, never directly on main/master
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
