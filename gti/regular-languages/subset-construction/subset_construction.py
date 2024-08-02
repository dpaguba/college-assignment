"""The subset construction: an NFA becomes a DFA.

The other direction of the equivalence, and the one with a cost. A state of
the DFA is a **set** of NFA states: exactly the set the NFA could be in after
reading the word so far. Determinism is recovered by tracking all
possibilities at once instead of guessing.

The price is in the name. An NFA with n states has 2^n possible subsets, and
there are languages where every one of them is needed, so the blow-up is not
an artefact of the construction. The classic witness is "the k-th symbol from
the end is an a", which needs 2^k deterministic states and k+1 non-deterministic
ones.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))

from finite_automata import DFA, EPSILON, NFA


def determinise(nfa, keep_names=False):
    """Convert an NFA into an equivalent DFA by tracking sets of states.

    Only the subsets actually reachable are built, which is what keeps the
    construction usable: the worst case is exponential, and the typical case
    is not. Starting from the epsilon closure of the start states and adding
    successors on demand is the whole algorithm.

    The empty set is a legitimate state: it is the trap the automaton falls
    into when the NFA has no move at all. It is only created when it is
    reachable, which keeps the result partial rather than cluttered.
    """
    start = frozenset(nfa.epsilon_closure(nfa.start))

    states = {start}
    transitions = {}
    queue = [start]

    while queue:
        current = queue.pop(0)
        for symbol in nfa.alphabet:
            target = frozenset(nfa.move(current, symbol))
            if not target:
                continue
            transitions[(current, symbol)] = target
            if target not in states:
                states.add(target)
                queue.append(target)

    accepting = {state for state in states if state & nfa.accepting}
    dfa = DFA(states, nfa.alphabet, transitions, start, accepting,
              name=f"det({nfa.name})")

    return dfa if keep_names else _readable(dfa)


def _readable(dfa):
    """Rename frozensets to short names, keeping a map back to the sets."""
    order = [dfa.start] + sorted((state for state in dfa.states if state != dfa.start),
                                 key=lambda state: (len(state), sorted(map(str, state))))
    names = {state: f"D{index}" for index, state in enumerate(order)}

    transitions = {(names[state], symbol): names[target]
                   for (state, symbol), target in dfa.transitions.items()}

    result = DFA({names[state] for state in dfa.states}, dfa.alphabet, transitions,
                 names[dfa.start], {names[state] for state in dfa.accepting}, dfa.name)
    result.subsets = {names[state]: sorted(map(str, state)) for state in dfa.states}
    return result


def construction_table(nfa):
    """The table the exercises ask to be filled in by hand.

    One row per reachable subset, one column per symbol, plus a marker for the
    accepting subsets. Reading it out is the manual version of the algorithm.
    """
    start = frozenset(nfa.epsilon_closure(nfa.start))
    rows = []
    seen = {start}
    queue = [start]

    while queue:
        current = queue.pop(0)
        row = {"subset": sorted(map(str, current)),
               "accepting": bool(current & nfa.accepting)}

        for symbol in nfa.alphabet:
            target = frozenset(nfa.move(current, symbol))
            row[symbol] = sorted(map(str, target))
            if target and target not in seen:
                seen.add(target)
                queue.append(target)

        rows.append(row)

    return rows


def blowup_example(k, alphabet=("a", "b")):
    """The language where the subset construction really does need 2^k states.

    "The k-th symbol from the end is an a" is accepted by an NFA with k+1
    states, which guesses where the end is, and by no DFA with fewer than 2^k,
    because a deterministic machine has to remember the last k symbols.

    It is the standard proof that the exponential bound is tight, and running
    it for a few values of k is the fastest way to believe it.
    """
    states = {f"n{index}" for index in range(k + 1)}
    transitions = {}

    for symbol in alphabet:
        transitions.setdefault(("n0", symbol), set()).add("n0")
    transitions.setdefault(("n0", "a"), set()).add("n1")

    for index in range(1, k):
        for symbol in alphabet:
            transitions.setdefault((f"n{index}", symbol), set()).add(f"n{index + 1}")

    return NFA(states, tuple(alphabet), transitions, {"n0"}, {f"n{k}"},
               name=f"kth-from-end({k})")
