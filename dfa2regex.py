import itertools, functools, copy, re

# x%7 == 0 dfa
DFA = {str(x): { "0": str((x*2)%7), "1": str((x*2+1)%7)  } for x in range(7) }
DFA_START = "0"
DFA_ACCEPT = {"0"}

# Make sure there's a unique start and end state with no transitions in or out
DFA["start"] = copy.copy(DFA[DFA_START])
DFA["end"] = {}
for state in DFA_ACCEPT:
    DFA[state][""] = "end"
dfa = copy.deepcopy(DFA)

def atom(x):
    return (0, x)
def parenthesize(r1):
    if r1[0] == 0:
        return r1
    return (0, "({})".format(r1[1]))
def kleene_star(r1):
    if r1[0] > 1:
        r1 = parenthesize(r1)
    return (1, "{}*".format(r1[1]))
def sequence(r1, r2):
    if r1[0] > 2:
        r1 = parenthesize(r1)
    if r2[0] > 2:
        r2 = parenthesize(r2)
    return (2,  "{}{}".format(r1[1], r2[1]))
def or_(r1, r2):
    return (3, "{}|{}".format(r1[1], r2[1]))
for state in DFA:
    dfa[state] = {atom(key): dfa[state][key] for key in dfa[state]}

def combine_duplicate_transitions(t, s1):
    # If there are multiple transitions S1-A->S2, S1->B->S2, combine them as S1-A|B->S2
    outgoing = [(t[s1][key], key) for key in t[s1]]
    for target, group in itertools.groupby(sorted(outgoing), lambda x: x[0]):
        group = list(group)
        if len(group) <= 1:
            continue
        keys = []
        for (target, key) in group:
            keys.append(key)
            assert t[s1][key] == target
            del t[s1][key]
        newkey = functools.reduce(or_, keys)
        t[s1][newkey] = target
def find_self_transition(t, s1):
    for key in t[s1]:
        if t[s1][key] == s1:
            return key
    return None
def remove_self_transitions(t, s1):
    while True:
        key = find_self_transition(t, s1)
        if key is None:
            return
        # If there's any transition S1 -A-> S1, remove it.
        # For every S1 -B-> S2, replace it with S1 -A*B-> S2
        assert t[s1][key] == s1
        del t[s1][key]
        ks = kleene_star(key)
        t[s1] = {sequence(ks, key2): t[s1][key2] for key2 in t[s1]}
def remove_transition(t, s1, key):
    # To replace the transition S1 -A-> S2:
    # For every S2 -B-> S3, add S1 -AB -> S3.
    # Then S1 -A-> S2 can be removed.
    s2 = t[s1].pop(key)
    assert s1 != s2
    #print(inp, poss_keys, len(poss_keys), state, t[state])#, t)
    for key2 in t[s2]:
        combined = sequence(key, key2)
        print(s1, "-", key, "->", s2, "-", key2, "->", t[s2][key2], "=", s1 , "-", combined, "->", t[s2][key2])
        t[s1][combined] = t[s2][key2]
def remove_state(t, s2):
    # S2 is not the start or end state, and you want to remove it.
    # Remove all incoming transitions to S2. It can be deleted as unreachable.
    assert find_self_transition(t, s2) is None
    assert s2 in t
    incoming = []
    for s1 in t:
        for key in t[s1]:
            if t[s1][key] == s2:
                incoming.append([s1, key])
    for (s1, key) in incoming:
        remove_transition(t, s1, key)
    del t[s2]

def simplify(t):
    for s in t:
        combine_duplicate_transitions(t, s)
        print_dfa("Combined duplicates {}".format(s), t)
        remove_self_transitions(t, s)
        print_dfa("Removed self-transitions {}".format(s), t)
        combine_duplicate_transitions(t, s)
        print_dfa("Combined duplicates {}".format(s), t)

def simulate_state(dfa, s):
    state = "start"
    for x in s:
        state = dfa[state][x]
    return state
def simulate_t(t, inp, debug=False):
    state = "start"
    orig_inp = inp
    while True:
        poss_keys = []
        for key in t[state]:
            if re.match(key[1], inp):
                poss_keys.append(key)
        if debug:
            print(orig_inp, inp, poss_keys, len(poss_keys), state, t[state])#, t)
        if len(poss_keys) == 0:
            return (state == "end" and not inp)
        else:
            assert len(poss_keys) >= 1
            key = poss_keys[0]
            m = re.match(key[1], inp)
            chars = len(m.group(0))
            state, inp = t[state][key], inp[chars:]
def verify_against(t, f, tests=["{:b}".format(x) for x in range(100)]):
    for x in tests:
        if simulate_t(t, x) != f(x):
            print("INCORRECT ON {}: {} {}".format(x, simulate_t(t, x), f(x)))
            simulate_t(t, x, debug=True)
            return False
    return True
    
def repr_dfa(t):
    out = "State\tRegex\tTo\n"
    for state in sorted(t.keys()):
        for key in sorted(t[state].keys()):
            out += "{}\t{}\t{}\n".format(state, key, t[state][key])
    return out
last = ""
def print_dfa(reason, t):
    global last
    cur = repr_dfa(t)
    if cur == last:
        return
    print(reason)
    print(cur)
    last = cur
    if not verify_against(t, lambda x: int(x,2)%7==0):
        print("WRONG")

def dfa2regex(t):
    for x in [str(x) for x in range(7)]:
        print_dfa("Initial configuration", t)
        simplify(t)
        remove_state(t, x)
        print_dfa("Removed state {}".format(x), t)
    simplify(t)
    assert set(t.keys()) == {"start", "end"}
    assert t["end"] == {}
    assert len(t["start"]) == 1
    regex = list(t["start"].keys())[0]
    assert t["start"][regex] == "end"
    return regex[1]

regex = dfa2regex(dfa)
regex = "^({})$".format(regex)
r = re.compile(regex)
print("number\tcorrect\tDFA\tregex")
correct = 0
for x in range(100):
    bin_ = bin(x)[2:]
    print("{}\t{}\t{}\t{}".format(x, x%7, bin_, simulate_state(DFA, bin_), bool(r.match(bin_))))
    if bool(r.fullmatch(bin_)) == bool(x%7==0):
        correct += 1
    if bool(r.match(bin_)) == bool(x%7==0):
        correct += 1
print(correct)

print(regex)
