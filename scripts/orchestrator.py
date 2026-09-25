#!/usr/bin/env python3
import random, subprocess, sys, os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)

TASKS = [
    ("scripts/tasks/task_01_fetch.py",      "Fetch EOD market snapshot"),
    ("scripts/tasks/task_02_indicators.py", "Update technical indicators (RSI/MACD/MA)"),
    ("scripts/tasks/task_03_anomalies.py",  "Scan for 2-sigma market anomalies"),
    ("scripts/tasks/task_04_stats.py",      "Refresh rolling volatility and correlation"),
    ("scripts/tasks/task_05_readme.py",     "Regenerate README summary"),
]

def git(args, check=False):
    return subprocess.run(["git"] + args, check=check, capture_output=True, text=True)

def run():
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    guard = Path.home() / ".cache/market-daily/last_run"
    guard.parent.mkdir(parents=True, exist_ok=True)
    if guard.exists() and guard.read_text().strip() == date:
        print(f"already ran today ({date})"); return
    n = random.randint(1, 5)
    chosen = random.sample(TASKS, n)
    chosen.sort(key=lambda t: 0 if "fetch" in t[0] else 1)
    print(f"running {n} tasks for {date}")
    for script, msg in chosen:
        r = subprocess.run(["python", script], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"FAIL {script}: {r.stderr}"); continue
        git(["add", "."])
        diff = git(["diff", "--cached", "--quiet"])
        if diff.returncode == 0:
            print(f"no diff for {script}"); continue
        git(["commit", "-m", f"{msg} — {date}"])
        git(["push", "origin", "main"])
        print(f"committed: {msg}")
    guard.write_text(date)

if __name__ == "__main__": run()
