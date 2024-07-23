"""Minimisation: the smallest DFA for a language, and why it is unique.

Two states are **equivalent** when no word tells them apart: from either one,
exactly the same words lead to acceptance. Merging equivalent states loses
nothing, and the automaton that remains is the smallest one for the language.

That automaton is unique up to renaming, which is the strong part of the
theorem and what makes minimisation a decision procedure: two DFAs accept the
same language exactly when their minimal automata are isomorphic.

Two algorithms are here. Table filling is quadratic and shows which pair is
separated by which word, which is what an exercise asks for. Hopcroft's
partition refinement is O(n log n) and shows nothing, which is what a tool
uses.
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "finite-automata"))

from finite_automata import DFA


def table_filling(dfa, trace=False):
    """Mark distinguishable pairs until nothing changes.

    Start by marking every pair where one state accepts and the other does
    not, since the empty word already separates them. Then repeatedly mark a
    pair whose successors under some symbol are already marked, because the
    word that separated the successors, with that symbol in front, separates
    this pair too.

    When the marking stops, the unmarked pairs are exactly the equivalent
    ones. The witness word can be read back from the round in which a pair was
    marked, which is what ``trace`` records.
    """
    dfa = dfa.complete()
    states = sorted(dfa.states, key=str)

    marked = {}
    for first, second in combinations(states, 2):
        if (first in dfa.accepting) != (second in dfa.accepting):
            marked[(first, second)] = ""

    changed = True
    rounds = 0

    while changed:
        changed = False
        rounds += 1

        for first, second in combinations(states, 2):
            if (first, second) in marked:
                continue

            for symbol in dfa.alphabet:
                left = dfa.step(first, symbol)
                right = dfa.step(second, symbol)
                if left == right:
                    continue

                key = (left, right) if str(left) < str(right) else (right, left)
                if key in marked:
                    marked[(first, second)] = symbol + marked[key]
                    changed = True
                    break

    if trace:
        return marked, rounds
    return marked


def equivalence_classes(dfa):
    """Group the states that no word separates."""
    dfa = dfa.complete()
    states = sorted(dfa.states, key=str)
    marked = table_filling(dfa)

    parent = {state: state for state in states}

    def find(state):
        """The representative of a state's class, compressing the path on the way."""
        while parent[state] != state:
            parent[state] = parent[parent[state]]
            state = parent[state]
        return state

    for first, second in combinations(states, 2):
        if (first, second) not in marked:
            parent[find(first)] = find(second)

    groups = {}
    for state in states:
        groups.setdefault(find(state), []).append(state)

    return sorted(sorted(group, key=str) for group in groups.values())


def minimise(dfa, name=None, keep_trap=True):
    """The minimal DFA: drop unreachable states, then merge the equivalent ones.

    Unreachable states are removed first. They cannot be separated from
    anything by a word the automaton can actually read, so leaving them in
    produces a correct but larger result and breaks the uniqueness claim.

    ``keep_trap`` decides whether the result stays **complete**. A complete
    minimal DFA has one state per Nerode class, including the class of words
    with no continuation into the language, which is the trap. Dropping it
    gives a smaller partial automaton for the same language, and then the state
    count is no longer the Nerode index. The course counts the trap, so it is
    kept by default.
    """
    trimmed = _reachable_only(dfa).complete() if keep_trap else dfa.trim().complete()
    classes = equivalence_classes(trimmed)

    names = {}
    for index, group in enumerate(classes):
        for state in group:
            names[state] = f"m{index}"

    transitions = {}
    for state in trimmed.states:
        for symbol in trimmed.alphabet:
            target = trimmed.step(state, symbol)
            if target is not None:
                transitions[(names[state], symbol)] = names[target]

    result = DFA({names[state] for state in trimmed.states}, trimmed.alphabet,
                 transitions, names[trimmed.start],
                 {names[state] for state in trimmed.accepting},
                 name or f"min({dfa.name})")

    return result if keep_trap else result.trim()


def _reachable_only(dfa):
    """Drop unreachable states, keeping everything a word can still reach."""
    keep = dfa.reachable()
    transitions = {(state, symbol): target
                   for (state, symbol), target in dfa.transitions.items()
                   if state in keep and target in keep}
    return DFA(keep, dfa.alphabet, transitions, dfa.start,
               dfa.accepting & keep, dfa.name)


def hopcroft(dfa, name=None):
    """Minimisation by partition refinement, in O(n log n).

    Start with two blocks, accepting and not, and repeatedly split a block
    whose members disagree about which block they reach on some symbol. The
    trick that gives the bound is always processing the **smaller** half of a
    split, so each state is examined a logarithmic number of times.

    Same result as table filling, and no witness words: the algorithm knows
    which states differ and not why.
    """
    dfa = _reachable_only(dfa).complete()
    accepting = frozenset(dfa.accepting)
    rest = frozenset(dfa.states - dfa.accepting)

    partition = {block for block in (accepting, rest) if block}
    pending = {min(partition, key=len)} if len(partition) > 1 else set()

    while pending:
        splitter = pending.pop()

        for symbol in dfa.alphabet:
            arriving = {state for state in dfa.states if dfa.step(state, symbol) in splitter}

            for block in list(partition):
                inside = frozenset(block & arriving)
                outside = frozenset(block - arriving)

                if not inside or not outside:
                    continue

                partition.discard(block)
                partition.add(inside)
                partition.add(outside)

                if block in pending:
                    pending.discard(block)
                    pending.add(inside)
                    pending.add(outside)
                else:
                    pending.add(inside if len(inside) <= len(outside) else outside)

    order = sorted(partition, key=lambda block: sorted(map(str, block)))
    names = {}
    for index, block in enumerate(order):
        for state in block:
            names[state] = f"h{index}"

    transitions = {}
    for state in dfa.states:
        for symbol in dfa.alphabet:
            target = dfa.step(state, symbol)
            if target is not None:
                transitions[(names[state], symbol)] = names[target]

    return DFA({names[state] for state in dfa.states}, dfa.alphabet, transitions,
               names[dfa.start], {names[state] for state in dfa.accepting},
               name or f"hopcroft({dfa.name})")


def isomorphic(first, second):
    """Whether two DFAs are the same automaton up to renaming.

    Walks both from their start states in lockstep. Since both are
    deterministic, the mapping is forced, so a single traversal decides it.
    Applied to two minimal automata this decides language equivalence.
    """
    if len(first.states) != len(second.states) or set(first.alphabet) != set(second.alphabet):
        return False

    mapping = {first.start: second.start}
    queue = [(first.start, second.start)]

    while queue:
        left, right = queue.pop()
        if (left in first.accepting) != (right in second.accepting):
            return False

        for symbol in first.alphabet:
            left_target = first.step(left, symbol)
            right_target = second.step(right, symbol)

            if (left_target is None) != (right_target is None):
                return False
            if left_target is None:
                continue

            if left_target in mapping:
                if mapping[left_target] != right_target:
                    return False
            else:
                mapping[left_target] = right_target
                queue.append((left_target, right_target))

    return True


def separating_words(dfa):
    """For every distinguishable pair, a word that tells the two states apart.

    The by-product of table filling that makes it worth its worse complexity:
    the answer to "why are these not the same state" is a concrete word.
    """
    marked = table_filling(dfa.complete())
    return {pair: word for pair, word in sorted(marked.items(), key=lambda item: str(item[0]))}
