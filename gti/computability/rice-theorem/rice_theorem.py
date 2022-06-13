"""Rice's theorem: every non-trivial question about what a machine computes.

    If a property of languages is non-trivial, then deciding whether the
    language of a given machine has it is undecidable.

Non-trivial means some machine has the property and some machine does not.
That is the entire hypothesis, and the conclusion covers every interesting
semantic question at once: is the language empty, is it finite, is it regular,
does it contain a particular word, is it equal to another one.

The proof is one reduction. Given a property P and a machine that lacks it,
build from an instance ``(M, w)`` a machine that behaves like the witness for P
when M accepts w, and like the machine lacking P otherwise. Deciding P would
then decide halting.

The point for exercises is the boundary: the theorem is about **semantic**
properties, those that depend only on the language. Syntactic questions such as
"does the machine have five states" or "does it halt within 100 steps" are
decidable, and are not counterexamples.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "turing-machines"))

from turing_machines import TuringMachine


def language_sample(machine, alphabet, max_length=3, budget=2000):
    """The words up to a length the machine accepts, as a fingerprint of its language.

    A finite approximation, and every semantic test below is only as good as
    this sample. That is a limitation of running code, not of the theorem.
    """
    found = []
    queue = [""]

    while queue:
        word = queue.pop(0)
        if machine.run(word, limit=budget)["outcome"] == "accept":
            found.append(word)
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in alphabet)

    return tuple(found)


def is_semantic(property_function, machines, alphabet, max_length=3):
    """Test whether a property depends only on the language, on a sample.

    Two machines with the same sampled language must get the same answer. A
    disagreement proves the property is syntactic; agreement is evidence and
    not proof, since the sample is finite.
    """
    by_language = {}

    for machine in machines:
        fingerprint = language_sample(machine, alphabet, max_length)
        verdict = property_function(machine)

        if fingerprint in by_language and by_language[fingerprint] != verdict:
            return False, fingerprint

        by_language[fingerprint] = verdict

    return True, None


def is_trivial(property_function, machines):
    """Whether every machine in the sample answers the same way.

    Trivial properties are decidable: answer yes always, or no always. Rice
    says nothing about them, and forgetting that is the usual misuse of the
    theorem.
    """
    verdicts = {property_function(machine) for machine in machines}
    return len(verdicts) <= 1


def verdict(property_function, machines, alphabet, max_length=3):
    """Classify a property: undecidable by Rice, trivial, or syntactic.

    The three outcomes are the three ways an exercise can go, and naming which
    one applies is usually the whole answer.
    """
    semantic, witness = is_semantic(property_function, machines, alphabet, max_length)
    trivial = is_trivial(property_function, machines)

    if not semantic:
        return {"verdict": "syntactic, Rice does not apply",
                "detail": f"two machines with the sampled language {witness} disagree"}
    if trivial:
        return {"verdict": "trivial, decidable",
                "detail": "every machine in the sample answers the same way"}

    return {"verdict": "undecidable by Rice",
            "detail": "the property is semantic and non-trivial"}


def accepts_empty_word(machine, budget=2000):
    """Semantic: does the language contain the empty word."""
    return machine.run("", limit=budget)["outcome"] == "accept"


def language_is_empty(machine, alphabet=("a", "b"), max_length=3, budget=2000):
    """Semantic: is the language empty, as far as the sample can tell."""
    return not language_sample(machine, alphabet, max_length, budget)


def accepts_something_long(machine, alphabet=("a", "b"), max_length=3, budget=2000):
    """Semantic: does the language contain a word of length at least two."""
    return any(len(word) >= 2 for word in language_sample(machine, alphabet, max_length, budget))


def has_few_states(machine, limit=5):
    """Syntactic: a property of the machine, not of its language.

    Decidable by counting, and the standard example of what Rice does **not**
    cover. Two machines with the same language can differ here, which is what
    ``is_semantic`` detects.
    """
    return len(machine.states) <= limit


def halts_quickly(machine, word="", steps=20):
    """Syntactic: does it halt on this input within a fixed number of steps.

    Decidable, because the bound makes it a finite check. The unbounded version
    is the halting problem, and the only difference is the bound.
    """
    return machine.run(word, limit=steps)["outcome"] != "limit"


def sample_machines():
    """A handful of machines, including two with the same language.

    The pair with equal languages and **different state counts** is what makes
    the semantic test meaningful. Without a pair that a syntactic property can
    separate, every property looks semantic and the classifier is toothless,
    which is exactly what happened the first time this sample was written: both
    "same language" machines had fewer than five states, so the state-count
    property passed as semantic.
    """
    from turing_machines import BLANK, RIGHT, STAY
    from turing_machines import equal_counts, three_equal_blocks

    accept_all = TuringMachine(
        {"q", "accept"}, ("a", "b"), ("a", "b", BLANK),
        {("q", symbol): ("accept", symbol, STAY) for symbol in ("a", "b", BLANK)},
        "q", "accept", None, BLANK, "accept everything")

    detour = {}
    chain = [f"d{index}" for index in range(6)]
    for index, state in enumerate(chain):
        following = chain[index + 1] if index + 1 < len(chain) else "accept"
        for symbol in ("a", "b", BLANK):
            detour[(state, symbol)] = (following, symbol, STAY)

    accept_all_slowly = TuringMachine(
        set(chain) | {"accept"}, ("a", "b"), ("a", "b", BLANK), detour,
        chain[0], "accept", None, BLANK, "accept everything, seven states")

    accept_nothing = TuringMachine(
        {"q", "accept"}, ("a", "b"), ("a", "b", BLANK), {},
        "q", "accept", None, BLANK, "accept nothing")

    return [accept_all, accept_all_slowly, accept_nothing,
            equal_counts(), three_equal_blocks()]
