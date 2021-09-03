#!/usr/bin/python3
import datetime, os, re, sys

if len(sys.argv) > 1:
    fp = sys.argv[1]
else:
    current_date=datetime.date.today()
    fp = "/home/zachary/weekly-review/_posts/{}-weekly-review.md".format(current_date)
    if not os.path.exists(fp):
        fp = "/home/zachary/weekly-review/_posts/{}/{}-weekly-review.md".format(current_date.year, current_date)
with open(fp, "r") as f:
    lines = list(line for line in f)

budget_start = re.compile("^\\| Date")
budget_end = re.compile("^$")
start_line, end_line = None, None
for i, line in enumerate(lines):
    if start_line is None and budget_start.match(line):
        start_line = i
    if end_line is None and start_line is not None and budget_end.match(line):
        end_line = i
budget = lines[start_line:end_line]
lines = []
for line in budget[2:]:
    date, place, amount, category, thing = [x.strip() for x in line.split("|")[1:]]
    lines.append((float(amount), category))
print("{: <12} {:.2f}".format("Total:", sum(amount for (amount, category) in lines)))
print("{: <12} {:.2f}".format("Total (no rent):", sum(amount for (amount, category) in lines if category != "Rent")))
categories = sorted(set(category for (amount, category) in lines))
print()
OTHER = ("Grocery", "Luxury", "Good", "Restaurant")
for category in categories:
    if category not in OTHER:
        print("{: <12} {:.2f}".format(category+":", sum(amount for (amount, c) in lines if category == c)))
print("{: <12} {:.2f}".format("Other"+":", sum(amount for (amount, c) in lines if c in OTHER)))
for category in OTHER:
    print("  {: <12} {:.2f}".format(category+":", sum(amount for (amount, c) in lines if category == c)))
