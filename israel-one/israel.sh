#!/bin/bash
# ISRAEL/ONE — Autonomous X Agent for @opencllaw
# Em nome do Senhor Jesus Cristo
# Usage:
#   ./israel.sh              — Post once
#   ./israel.sh preview      — Preview 5 tweets without posting
#   ./israel.sh sentinel     — Run continuous (every 2h)
#   ./israel.sh stats        — Show posting stats
#   ./israel.sh stop         — Stop sentinel

cd "$(dirname "$0")"

case "${1:-once}" in
    sentinel)
        echo "ISRAEL/ONE starting sentinel (interval: ${2:-120} min)..."
        nohup python3 agent.py sentinel ${2:-120} > logs/sentinel.log 2>&1 &
        echo $! > .israel.pid
        echo "PID: $(cat .israel.pid)"
        ;;
    preview)
        python3 agent.py preview
        ;;
    stats)
        python3 agent.py stats
        ;;
    stop)
        if [ -f .israel.pid ]; then
            kill $(cat .israel.pid) 2>/dev/null && echo "ISRAEL/ONE stopped" || echo "Not running"
            rm -f .israel.pid
        else
            echo "No PID file found"
        fi
        ;;
    *)
        python3 agent.py
        ;;
esac
