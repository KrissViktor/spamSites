#!/bin/sh
set -eu
cd -- "$(dirname -- "$0")"
case "${1:-start}" in
    start)
        command -v python3 >/dev/null
        exec sudo systemd-run --unit=cover-traffic --collect \
            --property=CPUQuota=15% --property=MemoryMax=128M \
            /usr/bin/python3 "$(pwd)/cover_traffic.py"
        ;;
    stop) exec sudo systemctl stop cover-traffic ;;
    status) exec sudo systemctl status cover-traffic ;;
    logs) exec sudo journalctl -u cover-traffic -n 30 --no-pager ;;
    *) echo 'Usage: sh service.sh [start|stop|status|logs]' >&2; exit 2 ;;
esac
