#!/usr/bin/env python3
"""Low-rate HTTPS HEAD requests; no response bodies or redirects."""

import argparse
import http.client
import random
import time
from datetime import datetime

HOSTS = (
    "mail.ru",
    "cloud.mail.ru",
    "news.mail.ru",
    "pogoda.mail.ru",
    "auto.mail.ru",
    "hi-tech.mail.ru",
    "vk.ru",
    "vkvideo.ru",
    "ok.ru",
    "rutube.ru",
    "ya.ru",
    "yandex.ru",
    "disk.yandex.ru",
    "mail.yandex.ru",
    "music.yandex.ru",
    "market.yandex.ru",
    "travel.yandex.ru",
    "rasp.yandex.ru",
    "rambler.ru",
    "news.rambler.ru",
    "lenta.ru",
    "ria.ru",
    "tass.ru",
    "rbc.ru",
    "iz.ru",
    "kommersant.ru",
    "vedomosti.ru",
    "gazeta.ru",
    "fontanka.ru",
    "rg.ru",
    "interfax.ru",
    "habr.ru",
    "ixbt.ru",
    "3dnews.ru",
    "overclockers.ru",
    "championat.ru",
    "sport-express.ru",
    "sports.ru",
    "kinopoisk.ru",
    "ivi.ru",
    "afisha.ru",
    "avito.ru",
    "ozon.ru",
    "wildberries.ru",
    "dns-shop.ru",
    "citilink.ru",
    "mvideo.ru",
    "eldorado.ru",
    "vseinstrumenti.ru",
    "intek-tool.ru",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--once", action="store_true", help="Make one request and exit")
    args = parser.parse_args()
    cooldown = {}
    rng = random.SystemRandom()
    print("Low-rate background requests started; Ctrl+C to stop.", flush=True)
    while True:
        if not args.once:
            time.sleep(rng.uniform(0.5, 3.0))
        available = [host for host in HOSTS
                     if cooldown.get(host, 0) <= time.monotonic()]
        if not available:
            continue
        host = rng.choice(available)
        connection = http.client.HTTPSConnection(host, timeout=5)
        ok = False
        try:
            connection.request("HEAD", "/", headers={
                "User-Agent": "LowRateBackgroundRequests/1.0",
                "Connection": "close",
            })
            response = connection.getresponse()
            ok = response.status < 400
            print(f"{datetime.now().isoformat(timespec='seconds')} "
                  f"{host}: HTTP {response.status}", flush=True)
        except (OSError, http.client.HTTPException) as exc:
            print(f"{host}: {type(exc).__name__}", flush=True)
        finally:
            connection.close()
        if not ok:
            cooldown[host] = time.monotonic() + 1800
        if args.once:
            return 0 if ok else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nStopped.")
