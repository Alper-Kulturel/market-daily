#!/usr/bin/env python3
"""Task 1 — Fetch EOD market data."""
import json, sys
from datetime import datetime, timezone
from pathlib import Path
import yfinance as yf

TICKERS = {"SPX":"^GSPC","VIX":"^VIX","BTC":"BTC-USD","ETH":"ETH-USD",
           "US10Y":"^TNX","DXY":"DX-Y.NYB","GOLD":"GC=F","OIL":"CL=F"}

def run():
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    rows = []
    for name, tick in TICKERS.items():
        try:
            df = yf.Ticker(tick).history(period="5d", interval="1d")
            if df.empty: continue
            last = df.iloc[-1]; prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last["Close"]); prev_c = float(prev["Close"])
            pct = (close - prev_c)/prev_c*100 if prev_c else 0
            rows.append({"symbol":name,"ticker":tick,"close":round(close,4),
                         "prev_close":round(prev_c,4),"change_pct":round(pct,3),
                         "volume":int(last["Volume"]) if last.get("Volume") else 0})
        except Exception as e:
            print(f"WARN {name}: {e}", file=sys.stderr)
    Path(f"data/{date}.json").write_text(json.dumps({"date":date,"timestamp":ts,"instruments":rows}, indent=2))
    lines = ["symbol,close,prev_close,change_pct,volume"]
    for r in rows:
        lines.append(f"{r['symbol']},{r['close']},{r['prev_close']},{r['change_pct']},{r['volume']}")
    Path(f"data/{date}.csv").write_text("\n".join(lines) + "\n")
    print(f"fetched {len(rows)} instruments")

if __name__ == "__main__": run()
