#!/bin/sh
set -eu
cd -- "$(dirname -- "$0")"
command -v python3 >/dev/null 2>&1 || {
    echo 'Install Python: sudo apt-get update && sudo apt-get install -y python3' >&2
    exit 1
}
exec python3 ./cover_traffic.py "$@"
