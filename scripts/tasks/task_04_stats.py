#!/usr/bin/env python3
import pandas as pd, json
from datetime import datetime
from pathlib import Path
import yfinance as yf

SYMS = {"SPX":"^GSPC","BTC":"BTC-USD","GOLD":"GC=F","US10Y":"^TNX","DXY":"DX-Y.NYB"}

def run():
    date = datetime.utcnow().strftime("%Y-%m-%d")
    prices = {}
    for name, tick in SYMS.items():
        df = yf.Ticker(tick).history(period="180d", interval="1d")
        if not df.empty: prices[name] = df["Close"]
    if not prices: return
    df = pd.DataFrame(prices).dropna()
    rets = df.pct_change().dropna()
    vol = (rets.std() * (252**0.5) * 100).round(2).to_dict()
    corr = rets.corr().round(3).to_dict()
    Path(f"data/{date}_stats.json").write_text(json.dumps(
        {"annualized_vol_pct": vol, "correlation": corr}, indent=2))
    print(f"stats updated for {len(vol)} symbols")

if __name__ == "__main__": run()
