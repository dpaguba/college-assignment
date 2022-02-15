"""Modal equivalences, and the ones that look true and are not.

The box and the diamond are duals, `[]phi` is `!<>!phi`, exactly as the
universal and existential quantifiers are. Every equivalence follows from that
duality plus the propositional laws, and so does every non-equivalence.

The two asymmetries are worth stating plainly, because they are where the
mistakes happen:

- `[]` distributes over conjunction and **not** over disjunction
- `<>` distributes over disjunction and **not** over conjunction

Both failures have one-world counterexamples with two successors, and finding
one is more convincing than any amount of explanation.
"""

from __future__ import annotations

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "kripke-structures"))
sys.path.insert(0, os.path.join(_here, "..", "modal-satisfiability"))
import kripke_structures as ks
import modal_satisfiability as ms


def equivalent(first, second, limit=3):
    """Whether two formulas hold at the same worlds of every small structure.

    Equivalence in modal logic means agreement in every world of every
    structure, which cannot be checked by enumeration in general. Searching for
    a disagreement up to a bound is a refutation procedure: finding one settles
    it, finding none does not prove equivalence, only that no small
    counterexample exists.
    """
    return counterexample(first, second, limit) is None


def counterexample(first, second, limit=3):
    """A structure and world where two formulas disagree, or `None`."""
    left = ms.parse(first) if isinstance(first, str) else first
    right = ms.parse(second) if isinstance(second, str) else second
    variables = sorted(ms.variables_of(left) | ms.variables_of(right)) or ["p"]

    for size in range(1, limit + 1):
        for structure in ms.structures(variables, size):
            for world in structure.worlds:
                if structure.holds(left, world) != structure.holds(right, world):
                    return structure, world

    return None


DUALITIES = [
    ("[]A", "!<>!A"),
    ("<>A", "![]!A"),
    ("![]A", "<>!A"),
    ("!<>A", "[]!A"),
]
"""The four ways of writing the duality, all equivalent to each other."""

DISTRIBUTION = [
    ("[](A & B)", "[]A & []B", True),
    ("[](A | B)", "[]A | []B", False),
    ("<>(A | B)", "<>A | <>B", True),
    ("<>(A & B)", "<>A & <>B", False),
]
"""Which distributions hold, with the two that do not."""


def check_catalogue(limit=2):
    """Verify the stated dualities and distributions.

    Kept as a function rather than as a comment because a table of laws in a
    lecture is exactly the kind of thing that gets misremembered, and checking
    it costs a second.
    """
    results = []

    for first, second in DUALITIES:
        results.append((first, second, True, equivalent(first, second, limit)))

    for first, second, expected in DISTRIBUTION:
        results.append((first, second, expected, equivalent(first, second, limit)))

    return results


def frame_axioms():
    """The correspondence between axioms and properties of the relation.

    Each axiom is valid exactly on the frames whose relation has the stated
    property, which is the whole subject of correspondence theory and the
    reason modal logic is used to describe transition systems: choosing the
    axioms is choosing what the transitions are allowed to look like.
    """
    return [
        ("[]A -> A", "reflexive"),
        ("[]A -> [][]A", "transitive"),
        ("[]A -> <>A", "serial"),
        ("A -> []<>A", "symmetric"),
    ]


def holds_on_frame(axiom, structure, limit=2):
    """Whether an axiom holds at every world of one structure."""
    formula = ms.parse(axiom)
    return all(structure.holds(formula, world) for world in structure.worlds)
