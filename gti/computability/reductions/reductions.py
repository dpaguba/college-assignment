"""Many-one reductions: transporting undecidability from one problem to another.

    A <=m B     when a computable f exists with   x in A  <=>  f(x) in B

If A reduces to B and B were decidable, A would be too: run f, then the decider
for B. So a reduction from a known undecidable problem is a proof that the new
one is undecidable, and this is how every result after the halting problem is
obtained.

The direction is the thing exercises get wrong. To show B is **hard**, reduce
the known-hard A **to** B. Reducing B to A shows nothing about B.

The reductions here are executable: each builds a real Turing machine, and the
equivalence is checked on samples with bounded simulation.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "turing-machines"))

from turing_machines import BLANK, LEFT, RIGHT, STAY, TuringMachine


def prefix_writer(machine, word, name=None):
    """Build a machine that writes a fixed word, then behaves like the given one.

    The machine ignores whatever is on the tape, writes ``word`` from the
    left, returns the head to the start and hands over to ``machine``. It is
    the workhorse of the reductions below, and the reason they can be run:
    "hard-code the input" is a transformation of machines, not a thought
    experiment.

    The head must end on cell 0, not cell 1. Writing k symbols leaves the head
    at k, so k moves left bring it back, and the handover must then **stay**.
    Moving once more starts the simulated machine one cell off and it reads the
    second symbol of its own input first, which fails on some words and not on
    others: exactly the kind of bug the sample check below is for, and the
    reason this construction is verified rather than trusted.
    """
    transitions = {}
    states = set()

    for index, symbol in enumerate(word):
        current = f"write{index}"
        following = f"write{index + 1}" if index + 1 < len(word) else "rewind0"
        states.add(current)
        for seen in set(machine.tape_alphabet) | {BLANK}:
            transitions[(current, seen)] = (following, symbol, RIGHT)

    if not word:
        transitions[("write_start", BLANK)] = (machine.start, BLANK, STAY)
        states.add("write_start")
        start = "write_start"
    else:
        start = "write0"

    for index in range(len(word)):
        current = "rewind0" if index == 0 else f"rewind{index}"
        states.add(current)
        following = f"rewind{index + 1}" if index + 1 < len(word) else "handover"
        for seen in set(machine.tape_alphabet) | {BLANK}:
            transitions[(current, seen)] = (following, seen, LEFT)

    if word:
        states.add("handover")
        for seen in set(machine.tape_alphabet) | {BLANK}:
            transitions[("handover", seen)] = (machine.start, seen, STAY)

    renamed = {}
    for (state, symbol), move in machine.transitions.items():
        renamed[(state, symbol)] = move

    transitions.update(renamed)

    return TuringMachine(
        states | set(machine.states),
        machine.input_alphabet,
        tuple(set(machine.tape_alphabet) | set(word) | {BLANK}),
        transitions,
        start,
        machine.accept,
        machine.reject,
        BLANK,
        name or f"write({word})+{machine.name}",
    )


def halting_to_epsilon_acceptance(machine, word):
    """Reduce "does M halt on w" to "does M' accept the empty word".

    The built machine ignores its input, writes w, and runs M. It accepts the
    empty word exactly when M accepts w, so a decider for the second problem
    would decide the first.

    This is the shortest real reduction in the course and the template for the
    rest: **hard-code the input into the machine**.
    """
    return prefix_writer(machine, word, name=f"eps[{machine.name},{word}]")


def halting_to_nonempty_language(machine, word):
    """Reduce halting to "is the language of M' non-empty".

    The same construction serves: M' ignores its input entirely, so its
    language is either everything or nothing, and it is non-empty exactly when
    M accepts w.

    That "everything or nothing" trick is what makes one machine answer many
    different questions, and it is the engine behind
    [Rice's theorem](../rice-theorem/).
    """
    return prefix_writer(machine, word, name=f"nonempty[{machine.name},{word}]")


def verify(reduction, source_test, target_test, samples, budget=4000):
    """Check ``x in A <=> f(x) in B`` on a list of samples.

    A reduction cannot be verified in general, since both sides are usually
    undecidable. Checking it on instances where both answers are known within a
    step budget is what an exercise means by "check the reduction", and it
    catches the direction being backwards, which is the usual error.
    """
    rows = []
    for sample in samples:
        left = source_test(sample, budget)
        right = target_test(reduction(*sample) if isinstance(sample, tuple)
                           else reduction(sample), budget)
        rows.append({"sample": sample, "in A": left, "f(x) in B": right,
                     "agrees": left == right})

    return all(row["agrees"] for row in rows), rows


def halts_on(pair, budget=4000):
    """The source test: does the machine halt on the word within the budget."""
    machine, word = pair
    return machine.run(word, limit=budget)["outcome"] != "limit"


def accepts_on(pair, budget=4000):
    """Does the machine accept the word within the budget."""
    machine, word = pair
    return machine.run(word, limit=budget)["outcome"] == "accept"


def accepts_epsilon(machine, budget=4000):
    """The target test: does the machine accept the empty word."""
    return machine.run("", limit=budget)["outcome"] == "accept"


def language_non_empty(machine, budget=1500, max_length=3):
    """Does the machine accept anything at all, searched up to a length."""
    queue = [""]
    while queue:
        word = queue.pop(0)
        if machine.run(word, limit=budget)["outcome"] == "accept":
            return True
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in machine.input_alphabet)
    return False


def composition(first, second):
    """Reductions compose: ``A <=m B`` and ``B <=m C`` give ``A <=m C``.

    Which is why a library of reductions is worth building: once a problem is
    known hard, every problem it reduces to is hard, and the relation is
    transitive by construction.
    """
    def reduce(*arguments):
        """The composed reduction, applied in the order given."""
        return second(first(*arguments))
    return reduce


def catalogue():
    """The reductions in this module, with what each proves."""
    return [
        {
            "from": "HALT = {(M, w) : M halts on w}",
            "to": "EPS = {M : M accepts the empty word}",
            "by": "hard-code w into a machine that ignores its input",
            "proves": "EPS is undecidable",
        },
        {
            "from": "HALT",
            "to": "NONEMPTY = {M : L(M) is not empty}",
            "by": "the same construction; the language is all or nothing",
            "proves": "NONEMPTY is undecidable",
        },
        {
            "from": "PCP",
            "to": "ambiguity of context-free grammars",
            "by": "one variable per domino side, matching sequences become "
                  "two derivations of the same word",
            "proves": "ambiguity is undecidable, which is why the checker in "
                      "context-free-grammars can only find witnesses",
        },
    ]
