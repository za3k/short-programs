#!/usr/bin/env python3
"""Create this cycle's weekly-review file, budget included; print its path.

Anchored to Friday: run on any day Fri-Thu, it targets the most recent
Friday (the nominal review date), covering the preceding Fri-Thu week.
Run it AFTER transcribing the log book. The bare template is written
first (budget_summary.py needs the file on disk), then the budget rows
are spliced in; budget problems land in the file as CHECK lines.

Written by Claude (Anthropic).
"""
import datetime as dt
import pathlib
import subprocess
import sys

DIR = pathlib.Path.home() / "documents" / "weekly-review"
BUDGET = pathlib.Path.home() / ".projects" / "short-programs" / "budget_summary.py"

today = dt.date.today()
review = today - dt.timedelta((today.weekday() - 4) % 7)  # most recent Friday
start, end = review - dt.timedelta(7), review - dt.timedelta(1)

path = DIR / f"{review}-weekly-review.md"
if path.exists():
    print(path)
    sys.exit()


def day_line(i):
    d = start + dt.timedelta(i)
    return f"- **{d:%A}".ljust(14) + f"{d}**: "


days = "\n".join(day_line(i) for i in range(7))
path.write_text(f'''\
---
title: "Weekly Review of {start} to {end}"
date: {review}
tags: weekly-review
---
## Reflections

## Accomplishments

## Maybe next week

## Weekly 
{days}

## Weekly Budget
| Date       | Place         | Amount     | Category      | Thing |
|------------|---------------|-----------:|---------------|-------|

| Category         | Total    | Notes |
|------------------|---------:|-------|
''')

rows, checks = [], []
try:
    r = subprocess.run([BUDGET], text=True, capture_output=True)
except OSError as e:
    r = subprocess.CompletedProcess([], 1, "", str(e))
if r.returncode:
    err = (r.stderr or r.stdout).strip().splitlines()
    checks.append(f"budget_summary.py exited {r.returncode}: "
                  f"{err[-1] if err else 'no output'}; fill the table by hand")
else:
    for line in r.stdout.splitlines():
        if line.startswith("|") and not line.startswith(("| Date", "|-")):
            rows.append(line)
            try:
                ok = start <= dt.date.fromisoformat(line.split("|")[1].strip()) <= end
            except ValueError:
                ok = False
            if not ok:
                checks.append(f"out-of-week row: {line}")
        elif line:
            checks.append(line)

lines = path.read_text().splitlines()
sep = next(i for i, l in enumerate(lines) if l.startswith("|-")) + 1
lines[sep:sep] = rows
head = lines.index("## Weekly Budget") + 1
lines[head:head] = [f"CHECK: {c}" for c in checks]
path.write_text("\n".join(lines) + "\n")
print(path)
