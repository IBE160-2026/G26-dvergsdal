#!/bin/bash
# Usage: run-story.sh <name>   (reads $SP/runs/<name>.prompt, writes $SP/runs/<name>.out)
# Runs a headless story session; if it stops on the usage limit, waits 20 min and resumes it (up to 20 times).
SP="<scratchpad>"
N="$1"; ID=$(python -c "import uuid;print(uuid.uuid4())"); echo "session $ID" > "$SP/runs/$N.session"
cd "/c/Rikke IBE160/AI'll handle it" || exit 1
claude -p --session-id "$ID" --permission-mode auto --add-dir "$SP" --output-format text < "$SP/runs/$N.prompt" > "$SP/runs/$N.out" 2>&1
for i in $(seq 1 20); do
  if tail -3 "$SP/runs/$N.out" | grep -q "STORY_RESULT\|RETRO_RESULT"; then break; fi
  if ! tail -3 "$SP/runs/$N.out" | grep -qi "limit"; then break; fi
  echo "limit hit, waiting (try $i)" >> "$SP/runs/$N.session"; sleep 1200
  echo "Du ble stoppet av bruksgrensen. Den er nullstilt nå. Fortsett der du slapp, etter instruksjonene du fikk. Agenter som ble stoppet: send dem en melding for å fortsette, eller start dem på nytt med samme prompt hvis det ikke går." | \
    claude -p --resume "$ID" --permission-mode auto --add-dir "$SP" --output-format text >> "$SP/runs/$N.out" 2>&1
done
tail -15 "$SP/runs/$N.out"
