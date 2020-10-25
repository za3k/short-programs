#!/usr/bin/env python3
letters           = "abcdefghijklmnopqrstuvwxyz"
english_frequency = "etaoinsrhldcumfpgwybvkxjqz"
UNASSIGNED = "?"
assignment = { x: UNASSIGNED for x in letters }
ciphertext = ""

def sort_by_frequency(x):
    import collections
    return [value for value,count in collections.Counter(x).most_common()]

def print_clear():
    print("\u001b[2J\u001b[H")
def print_color(x, color="gray"):
    COLORCODE = {
        "black":  "\u001b[30m",
        "gray":   "\u001b[30;1m", # "bright black"
        "grey":   "\u001b[30;1m",
        "red":    "\u001b[31m",
        "green":  "\u001b[32m",
        "yellow": "\u001b[33m",
        "blue":   "\u001b[34m",
        "magenta":"\u001b[35m",
        "cyan":   "\u001b[36m",
        "white":  "\u001b[37m",
    }
    print(COLORCODE[color], end='')
    print(x, end='')
    print("\u001b[0m", end='') # reset
def print_newline():
    print()

def display(active_cipher=None):
    print_clear()
    print_color("substitution", "white")
    print_newline()
    for x in letters:
        if x == active_cipher:
            print_color(x, "blue")
        elif assignment[x] == UNASSIGNED:
            print_color(x)
        else:
            print_color(x, "green")
    print_newline()
    for x in letters:
        if x == active_cipher:
            print_color(x, "blue")
        elif assignment[x] == UNASSIGNED:
            print_color("?")
        else:
            print_color(assignment[x], "green")
    print_newline()
    print_newline()

    print_color("frequency", "white")
    print_newline()
    ciphertext_frequency = "".join(sort_by_frequency([x for x in ciphertext.lower() if x in letters]))
    for x in ciphertext_frequency:
        if x == active_cipher:
            print_color(x, "blue")
        elif assignment[x] == UNASSIGNED:
            print_color(x)
        else:
            print_color(x, "green")
    print_newline()
    for x in english_frequency:
        count = len([y for y in letters if assignment[y] == x])
        if active_cipher and x == assignment[active_cipher]:
            print_color(x, "blue")
        elif count > 1:
            print_color(x, "red")
        elif count == 1:
            print_color(x, "green")
        elif count == 0:
            print_color(x)
    print_newline()
    print_newline()

    print_color("cipher", "white")
    print_newline()
    for x in ciphertext:
        if x.lower() not in letters:
            print_color(x)
        elif x.lower() == active_cipher:
            print_color(x, "blue")
        elif assignment[x.lower()] == UNASSIGNED:
            print_color(x)
        else:
            print_color(x, "green")
    print_newline()
    for x in ciphertext:
        if x.lower() not in letters:
            print_color(x)
            continue
        if assignment[x.lower()] == UNASSIGNED:
            plaintext = "?"
        elif x in assignment and assignment[x] != UNASSIGNED:
            plaintext = assignment[x]
        else:
            plaintext = assignment[x.lower()].upper()
        count = len([y for y in letters if assignment[y] == assignment[x.lower()]])
            
        if x.lower() == active_cipher:
            print_color(plaintext, "blue")
        elif plaintext == "?":
            print_color("?")
        elif count > 1:
            print_color(plaintext, "red")  
        else:
            print_color(plaintext, "green")
    print_newline()

import sys, termios, tty
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
def get_okch(ok, error):
    while True:
        c = getch().lower()
        if c in ok:
            return c
        else:
            print(repr(c), error)

if __name__ == "__main__":
    assert len(sys.argv) == 2
    ciphertext = sys.argv[1]
    while True:
        display()
        c = get_okch(ciphertext.lower() + "\r\x7f", "not in ciphertext, or enter (exit), or backspace (clear all)")
        if c == "\r":
            sys.exit(1)
        elif c == "\x7f":
            assignment = { x: UNASSIGNED for x in letters }
            continue
        display(c)

        p = None
        p = get_okch(letters + " \r\x7f", "not an english letter, space (clear), or enter (exit)")
        if p == " " or p == "\x7f":
            assignment[c] = UNASSIGNED
        elif p == "\r":
            sys.exit(1)
        else:
            assignment[c] = p
            
            
