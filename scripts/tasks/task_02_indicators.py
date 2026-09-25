#!/usr/bin/env python3
import pandas as pd, json
from datetime import datetime
from pathlib import Path
import yfinance as yf

SYMS = {"SPX":"^GSPC","BTC":"BTC-USD","GOLD":"GC=F","OIL":"CL=F"}

def rsi(s, n=14):
    d = s.diff()
    up = d.clip(lower=0).rolling(n).mean()
    dn = -d.clip(upper=0).rolling(n).mean()
    return 100 - 100/(1 + up/dn)

def run():
    date = datetime.utcnow().strftime("%Y-%m-%d")
    out = {}
    for name, tick in SYMS.items():
        df = yf.Ticker(tick).history(period="120d", interval="1d")
        if df.empty: continue
        c = df["Close"]
        macd = c.ewm(span=12).mean() - c.ewm(span=26).mean()
        signal = macd.ewm(span=9).mean()
        out[name] = {"close": round(float(c.iloc[-1]),4),
                     "rsi14": round(float(rsi(c).iloc[-1]),2),
                     "ma20": round(float(c.rolling(20).mean().iloc[-1]),4),
                     "ma50": round(float(c.rolling(50).mean().iloc[-1]),4),
                     "macd": round(float(macd.iloc[-1]),4),
                     "macd_signal": round(float(signal.iloc[-1]),4)}
    Path(f"data/{date}_indicators.json").write_text(json.dumps(out, indent=2))
    print(f"indicators computed for {len(out)} symbols")

if __name__ == "__main__": run()
