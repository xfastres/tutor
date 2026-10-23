#!/usr/bin/env bash
# Link this tutor skill into the folders that common agents scan for skills.
#
# A skill is just this directory. Agents look in different places, so this
# script creates symlinks that all point back to the one source directory.
# Edit the repo once; every agent sees it.
#
# Default targets (user level):
#   ~/.agents/skills/tutor   Cursor, Codex, and other agents reading .agents/skills
#   ~/.claude/skills/tutor   Claude Code
#   ~/.codex/skills/tutor    Codex CLI
#
#   --cursor        also ~/.cursor/skills/tutor
#   --project DIR   also DIR/.agents/skills/tutor and DIR/.claude/skills/tutor
#   --uninstall     remove symlinks this script created; never deletes a real folder
set -euo pipefail

SRC="$(cd "$(dirname "$0")/.." && pwd -P)"
[ -f "$SRC/SKILL.md" ] || { echo "SKILL.md not found next to scripts/: $SRC" >&2; exit 1; }

TARGETS=("$HOME/.agents/skills/tutor" "$HOME/.claude/skills/tutor" "$HOME/.codex/skills/tutor")
UNINSTALL=0
while [ $# -gt 0 ]; do
  case "$1" in
    --cursor) TARGETS+=("$HOME/.cursor/skills/tutor") ;;
    --project) [ $# -ge 2 ] || { echo "--project needs a directory" >&2; exit 2; }
               PROJ="$(cd "$2" && pwd -P)"; TARGETS+=("$PROJ/.agents/skills/tutor" "$PROJ/.claude/skills/tutor"); shift ;;
    --uninstall) UNINSTALL=1 ;;
    *) echo "usage: install.sh [--cursor] [--project DIR] [--uninstall]" >&2; exit 2 ;;
  esac
  shift
done

resolve() { (cd "$1" 2>/dev/null && pwd -P); }

for t in "${TARGETS[@]}"; do
  if [ "$UNINSTALL" -eq 1 ]; then
    if [ -L "$t" ]; then rm "$t"; echo "removed  $t"
    elif [ -e "$t" ]; then echo "skip     $t (real folder, not touched)"
    else echo "absent   $t"; fi
    continue
  fi
  if [ -L "$t" ]; then
    if [ "$(resolve "$t")" = "$SRC" ]; then echo "ok       $t"
    else echo "conflict $t -> $(readlink "$t") (different source; remove it first)"; fi
    continue
  fi
  if [ -e "$t" ]; then echo "conflict $t is a real folder; move it away first"; continue; fi
  mkdir -p "$(dirname "$t")"
  ln -s "$SRC" "$t"
  echo "linked   $t -> $SRC"
done

if [ "$UNINSTALL" -eq 0 ]; then
  echo
  echo "Invoke with: /tutor 继续   (or: 用 tutor skill，继续)"
  echo "If an agent does not list the skill, tell it: 读 $SRC/SKILL.md，按 RUNBOOK 开课"
fi
