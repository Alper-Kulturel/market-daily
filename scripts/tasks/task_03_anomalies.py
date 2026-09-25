#!/usr/bin/env python3
import pandas as pd, json
from datetime import datetime
from pathlib import Path
import yfinance as yf

SYMS = {"SPX":"^GSPC","VIX":"^VIX","BTC":"BTC-USD","ETH":"ETH-USD"}

def run():
    date = datetime.utcnow().strftime("%Y-%m-%d")
    anomalies = []
    for name, tick in SYMS.items():
        df = yf.Ticker(tick).history(period="1y", interval="1d")
        if df.empty or len(df) < 30: continue
        rets = df["Close"].pct_change().dropna()
        mu, sd = rets.mean(), rets.std()
        latest = rets.iloc[-1]
        z = (latest - mu) / sd if sd else 0
        if abs(z) > 2:
            anomalies.append({"symbol":name,"return_pct":round(latest*100,3),
                              "z_score":round(z,2),"direction":"up" if z>0 else "down"})
    Path(f"data/{date}_anomalies.json").write_text(json.dumps(anomalies, indent=2))
    print(f"{len(anomalies)} anomalies detected")

if __name__ == "__main__": run()
