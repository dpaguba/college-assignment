"""Decidable, semi-decidable, and the line between them.

    decidable          some machine always halts and answers yes or no
    semi-decidable     some machine halts and says yes on the words in the
                       language, and may run for ever on the others

The halting problem is the standard example of the gap: it is semi-decidable,
because running the machine and waiting is a procedure that says yes when the
answer is yes, and it is not decidable, because no machine can always say no.

The proof is diagonalisation. Suppose H decides halting. Build D which, on
input x, asks H whether x halts on x, and does the opposite: loops if it halts,
halts if it loops. Then D on D halts exactly when it does not.

Nothing here can implement D, and that is the point: the contradiction shows
the assumption was false. What **is** implemented is everything decidable
around it, and the two searches that make semi-decidability concrete.
"""

from __future__ import annotations

import sys
from itertools import count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "turing-machines"))

from turing_machines import TuringMachine


def halts_within(machine, word, steps):
    """Whether the machine halts on the word within a step bound.

    **Decidable**, and trivially so: run it that many steps and look. The
    bounded question is easy and the unbounded one is not, which is the whole
    content of the halting problem.
    """
    result = machine.run(word, limit=steps)
    return result["outcome"] != "limit"


def accepts_within(machine, word, steps):
    """Whether the machine accepts within a step bound."""
    return machine.run(word, limit=steps)["outcome"] == "accept"


def semi_decide(machine, word, budget=10 ** 6, chunk=1000):
    """The semi-decision procedure: run and wait.

    Returns True when the machine accepts, and never returns False. The budget
    exists because this code has to end; a real semi-decision procedure would
    simply keep going, and that difference is exactly what "semi" means.
    """
    for limit in range(chunk, budget + 1, chunk):
        result = machine.run(word, limit=limit)
        if result["outcome"] == "accept":
            return True
        if result["outcome"] == "reject":
            return False
    return None


def decide_by_both(machine, complement_machine, word, budget=10 ** 5, chunk=500):
    """Decide a language when it **and its complement** are semi-decidable.

    Run both machines a bit at a time and stop when either accepts. One of them
    must, since the word is in exactly one of the two languages, so this always
    halts. That is the proof that a language is decidable exactly when both it
    and its complement are semi-decidable, and it is four lines of dovetailing.
    """
    for limit in range(chunk, budget + 1, chunk):
        if machine.run(word, limit=limit)["outcome"] == "accept":
            return True
        if complement_machine.run(word, limit=limit)["outcome"] == "accept":
            return False
    return None


def enumerate_language(machine, alphabet, limit=6, budget=2000):
    """List the words a machine accepts, by dovetailing over words and steps.

    Running each word to completion in turn would hang on the first word the
    machine loops on. Dovetailing runs every word a little, then a little more,
    so every accepted word is eventually printed and no rejection blocks the
    others.

    That construction is what "recursively enumerable" means, and it is the
    reason semi-decidable and recursively enumerable are the same class.
    """
    words = [""]
    queue = [""]
    while queue and len(words) < 200:
        word = queue.pop(0)
        if len(word) < limit:
            for symbol in alphabet:
                extended = word + symbol
                words.append(extended)
                queue.append(extended)

    found = []
    for rounds in count(1):
        steps = rounds * 50
        if steps > budget:
            break
        for word in words[:rounds * 5]:
            if word in found:
                continue
            if machine.run(word, limit=steps)["outcome"] == "accept":
                found.append(word)

    return sorted(found, key=lambda word: (len(word), word))


def diagonal_argument(deciders, inputs):
    """Show that no list of total deciders covers every language.

    Given finitely many deciders and finitely many inputs, build the diagonal
    answer: disagree with decider i on input i. The result is a function none
    of them computes, which is the finite shadow of Cantor's argument and of
    the halting proof.

    The real theorem needs the list to be **all** machines, and the diagonal
    then has to be computable to reach a contradiction. Here it is only a
    demonstration that the shape of the argument is sound.
    """
    diagonal = {}
    for index, word in enumerate(inputs):
        if index < len(deciders):
            diagonal[word] = not deciders[index](word)
        else:
            diagonal[word] = False

    disagreements = []
    for index, decider in enumerate(deciders):
        if index < len(inputs):
            word = inputs[index]
            disagreements.append((index, word, decider(word), diagonal[word]))

    return diagonal, disagreements


def always_accept(alphabet=("a", "b")):
    """A machine that accepts every input, for testing the procedures above."""
    from turing_machines import BLANK, STAY

    transitions = {("q", symbol): ("accept", symbol, STAY)
                   for symbol in tuple(alphabet) + (BLANK,)}
    return TuringMachine({"q", "accept"}, tuple(alphabet), tuple(alphabet) + (BLANK,),
                         transitions, "q", "accept", None, BLANK, "accept everything")


def never_halt(alphabet=("a", "b")):
    """A machine that loops on every input, which no decider can be built from.

    Running it is what makes the difference between decidable and
    semi-decidable visible: ``semi_decide`` on this machine returns None,
    meaning "still running", for ever.
    """
    from turing_machines import BLANK, RIGHT

    transitions = {("q", symbol): ("q", symbol, RIGHT)
                   for symbol in tuple(alphabet) + (BLANK,)}
    return TuringMachine({"q", "accept"}, tuple(alphabet), tuple(alphabet) + (BLANK,),
                         transitions, "q", "accept", None, BLANK, "never halts")
