#!/usr/bin/python3
import datetime, glob, os, re, sys

DATE_FORMAT="%Y-%m-%d"
def load_review():
    if len(sys.argv) > 1:
        fp = sys.argv[1]
        current_date = '-'.join(fp.split("/")[-1].split("-")[:3])
        current_date = datetime.datetime.strptime(current_date, DATE_FORMAT)
    else:
        current_date=datetime.date.today()
        fp = "/home/zachary/weekly-review/_posts/{}/{}-weekly-review.md".format(current_date.year, current_date)
    if not os.path.exists(fp):
        fp = "/home/zachary/weekly-review/_posts/{}/{}-weekly-review.md".format(current_date.year, current_date.strftime(DATE_FORMAT))
    with open(fp, "r") as f:
        return list(f)
def load_budget():
    review_lines = load_review()
    budget_start = re.compile("^\\| Date")
    budget_end = re.compile("^$")
    start_line, end_line = None, None
    for i, line in enumerate(review_lines):
        if start_line is None and budget_start.match(line):
            start_line = i
        if end_line is None and start_line is not None and budget_end.match(line):
            end_line = i
    budget = review_lines[start_line:end_line]

    lines = []
    for line in budget[2:]:
        date, place, amount, category, thing = [x.strip() for x in line.split("|")[1:]]
        lines.append((float(amount), category))
    return lines
def load_finances():
    log_book = glob.glob("/home/zachary/physicalish_documents/log-book*CURRENT*")[0]
    with open(log_book, "r") as f:
        return list(f)
def parse_finance_page(finance_page):
    total = 0
    hand_total = None
    for line in finance_page[1:]:
        assert "--page" not in line
        date, place, amount, hand_total, thing = line[:10], line[28:48].strip(), line[48:57].strip(), line[57:65].strip(), line[66:].strip()
        if "error" != place:
            total += float(amount)
        hand_total = float(hand_total)
        print("| {date:<11}| {place:<14}|{amount:>11} | {category:<14}| {thing}".format(date=date, place=place, amount=amount, category="", thing=thing))
    return total, hand_total

def parse_week(lines, date):
    assert date is None
    finance_page = re.compile('--page (?P<page>[1-9][0-9]*), finances ')
    start_line, end_line = None, None
    total, hand_total = 0, None
    for i, line in enumerate(lines + ["--page 999, finances final"]):
        m = finance_page.match(line)
        if m:
            if start_line is None:
                cont = "cont" in line
                start_line = i
            else:
                end_line = i
                page_total, page_hand_total = parse_finance_page(lines[start_line:end_line])
                if hand_total is None:
                    hand_total = page_hand_total
                total += page_total
                start_line, end_line = i, None
                if cont:
                    cont = "cont" in line
                    continue
                break
    return total, hand_total

if __name__ == "__main__":
    budget_items = load_budget()

    if budget_items == []: # Budget not done yet
        finance_lines = load_finances()
        total, hand_total = parse_week(finance_lines, None) # ALWAYS returns the latest week
        print()
        if abs(total - hand_total) < 0.005:
            print("Total was correct, {}".format(hand_total))
        else:
            print("Correct total should be {:.2f}, was {:.2f}".format(total, hand_total))
    else: # Budget is done yet
        print("{: <12} {:.2f}".format("Total:", sum(amount for (amount, category) in budget_items)))
        print("{: <12} {:.2f}".format("Total (no rent):", sum(amount for (amount, category) in budget_items if category != "Rent")))
        categories = sorted(set(category for (amount, category) in budget_items))
        print()
        OTHER = ("Grocery", "Luxury", "Good", "Restaurant")
        for category in categories:
            if category not in OTHER:
                print("{: <12} {:.2f}".format(category+":", sum(amount for (amount, c) in budget_items if category == c)))
        print("{: <12} {:.2f}".format("Other"+":", sum(amount for (amount, c) in budget_items if c in OTHER)))
        for category in OTHER:
            print("  {: <12} {:.2f}".format(category+":", sum(amount for (amount, c) in budget_items if category == c)))
