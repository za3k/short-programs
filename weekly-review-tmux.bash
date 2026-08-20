#!/usr/bin/env bash
# Written by Claude (anthropic)
# Create or resume this cycle's review tmux session. Runs on the laptop.
# Flow: transcribe first; the review window waits at a prompt, then
# generates the template (budget included) and opens it when you hit Enter.
set -euo pipefail
shopt -s nullglob

gen="$(cd "$(dirname "$0")" && pwd)/weekly-review-template.py"
rday=$(date -d "-$(( ($(date +%u) + 2) % 7 )) days" +%F)  # most recent Friday
session="weekly-$rday"

books=()
for b in "$HOME"/physicalish_documents/*CURRENT*; do [[ -f $b ]] && books+=("$b"); done
(( ${#books[@]} )) || { echo "no CURRENT log book found" >&2; exit 1; }

if ! tmux has-session -t "$session" 2>/dev/null; then
    tmux new-session -d -s "$session" -n logbook "vim '${books[-1]}'"
    tmux new-window -t "$session" -n review -c "$HOME/documents/weekly-review" \
        "echo 'transcribe in the logbook window, then press Enter'; read _; if f=\$('$gen') && [ -f \"\$f\" ]; then vim \"\$f\"; else echo 'review generation failed (see above)'; fi; exec bash"
    tmux new-window -t "$session" -n "sleep" "summarize_activity --mode SLEEP; read _"
    tmux select-window -t "$session:logbook"
fi

if [[ -n ${TMUX:-} ]]; then exec tmux switch-client -t "$session"
else exec tmux attach -t "$session"; fi
