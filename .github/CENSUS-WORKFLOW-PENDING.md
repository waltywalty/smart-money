name: Kalshi boundary census (CI durable write-path test)

# Purpose is the WRITE PATH, not the census. Packet 5 Phase C: does a GitHub
# Actions runner reach Kalshi cleanly, what status codes does it see, and can it
# commit WITHOUT a pasted secret? The built-in GITHUB_TOKEN is the whole point -
# if this works, the project has a write path that survives having no human present.

on:
  workflow_dispatch:
  schedule:
    - cron: '17 4 * * *'

permissions:
  contents: write

jobs:
  census:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Probe Kalshi, status codes only, with an impossible control
        id: probe
        run: |
          set -uo pipefail
          UA='smart-money-research/1.0 (+CI census; contact rogerlgk@gmail.com)'
          B=https://api.elections.kalshi.com/trade-api/v2
          probe () { curl -sS -A "$UA" -H 'Expect:' --max-time 25 -o /tmp/body -w '%{http_code}' "$1"; }
          CUT=$(probe "$B/historical/cutoff")
          SETTLED=$(python3 -c "import json;print(json.load(open('/tmp/body')).get('market_settled_ts','?'))" 2>/dev/null || echo '?')
          FLOOR=$(probe "$B/markets?series_ticker=KXHIGHNY&limit=1000")
          MIN=$(python3 -c "import json;m=json.load(open('/tmp/body')).get('markets',[]);print(min([x['close_time'] for x in m]) if m else 'none')" 2>/dev/null || echo '?')
          CTL=$(probe "$B/markets?series_ticker=KXDEFINITELYNOTREAL&limit=10")
          CTLN=$(python3 -c "import json;print(len(json.load(open('/tmp/body')).get('markets',[])))" 2>/dev/null || echo '?')
          POS=$(probe "$B/series/KXHIGHNY")
          echo "cutoff_http=$CUT settled=$SETTLED floor_http=$FLOOR min_close=$MIN ctl_http=$CTL ctl_rows=$CTLN pos_http=$POS"
          {
            echo "cut=$CUT"; echo "settled=$SETTLED"; echo "floor=$FLOOR"; echo "min=$MIN"
            echo "ctl=$CTL"; echo "ctln=$CTLN"; echo "pos=$POS"
          } >> "$GITHUB_OUTPUT"

      - name: Append one line and commit with the built-in token
        run: |
          set -euo pipefail
          mkdir -p registry/retention
          F=registry/retention/CI-CENSUS-LOG.md
          if [ ! -f "$F" ]; then
            {
              echo '# CI census log - written by GitHub Actions, no pasted secret'
              echo
              echo 'Control discipline: `ctl` is an impossible series (must return 200 with 0 rows)'
              echo 'and `pos` is a known-present series (must return 200). A control that must fail'
              echo 'is only half of one - see SKILL.md rule 10.'
              echo
              echo '| date (UTC) | cutoff http | market_settled_ts | live floor http | min close_time | ctl http/rows | pos http | run |'
              echo '|---|---|---|---|---|---|---|---|'
            } > "$F"
          fi
          printf '| %s | %s | %s | %s | %s | %s / %s | %s | [%s](%s) |\n' \
            "$(date -u +%Y-%m-%dT%H:%MZ)" \
            '${{ steps.probe.outputs.cut }}' '${{ steps.probe.outputs.settled }}' \
            '${{ steps.probe.outputs.floor }}' '${{ steps.probe.outputs.min }}' \
            '${{ steps.probe.outputs.ctl }}' '${{ steps.probe.outputs.ctln }}' \
            '${{ steps.probe.outputs.pos }}' \
            "${GITHUB_RUN_ID}" "${GITHUB_SERVER_URL}/${GITHUB_REPOSITORY}/actions/runs/${GITHUB_RUN_ID}" >> "$F"
          git config user.name  'github-actions[bot]'
          git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add "$F"
          git commit -m "CI census $(date -u +%Y-%m-%d): boundary probe from an Actions runner"
          git push
