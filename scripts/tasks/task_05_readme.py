#!/usr/bin/env python3
import json, glob
from pathlib import Path

def run():
    files = sorted(glob.glob("data/*.json"))
    files = [f for f in files if "_" not in f.split("/")[-1]]
    if not files: return
    latest = json.load(open(files[-1]))
    lines = [f"# Market Snapshot — {latest['date']}", "",
             f"_Captured {latest['timestamp']}_", "",
             "| Symbol | Close | Change |", "|---|---|---|"]
    for r in latest["instruments"]:
        lines.append(f"| {r['symbol']} | {r['close']} | {r['change_pct']:+.2f}% |")
    lines += ["", "## Historical data", "",
              f"- {len(files)} daily snapshots in `data/`", ""]
    Path("LATEST.md").write_text("\n".join(lines) + "\n")
    print("README regenerated")

if __name__ == "__main__": run()
