#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
exec bash .agents/skills/format-skill/setup.sh
