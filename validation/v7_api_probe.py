from __future__ import annotations

import json
import urllib.request
import urllib.error

URLS = {
    "upbit_market": "https://api.upbit.com/v1/market/all?is_details=false",
    "upbit_btc_hour": "https://api.upbit.com/v1/candles/minutes/60?market=KRW-BTC&count=2",
    "binance_futures_ping": "https://fapi.binance.com/fapi/v1/ping",
    "binance_btc_hour": "https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=1h&limit=2",
    "binance_vision_month": "https://data.binance.vision/data/futures/um/monthly/klines/BTCUSDT/1h/BTCUSDT-1h-2024-01.zip",
    "frankfurter_fx": "https://api.frankfurter.app/2024-01-01..2024-01-05?from=USD&to=KRW",
}

out = {}
for name, url in URLS.items():
    req = urllib.request.Request(url, headers={"User-Agent": "v7-validation/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read(300)
            out[name] = {
                "ok": True,
                "status": r.status,
                "content_type": r.headers.get("content-type"),
                "content_length": r.headers.get("content-length"),
                "sample": body[:160].decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as e:
        out[name] = {"ok": False, "status": e.code, "error": str(e), "body": e.read(300).decode("utf-8", errors="replace")}
    except Exception as e:
        out[name] = {"ok": False, "error": type(e).__name__ + ": " + str(e)}

print(json.dumps(out, ensure_ascii=False, indent=2))
with open("validation_api_probe.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
