#!/usr/bin/python3
import datetime
import re

current_date=str(datetime.date.today())
with open("blog2.za3k.com/_posts/{}-weekly-review.md".format(current_date), "r") as f:
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
print("{: <12} {}".format("Total:", sum(amount for (amount, category) in lines)))
print("{: <12} {}".format("Total (no rent):", sum(amount for (amount, category) in lines if category != "Rent")))
categories = sorted(set(category for (amount, category) in lines))
print()
for category in categories:
    print("{: <12} {}".format(category+":", sum(amount for (amount, c) in lines if category == c)))
