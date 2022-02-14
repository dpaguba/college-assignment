"""Kripke structures: worlds, an accessibility relation, and what holds where.

Propositional logic evaluates a formula against one assignment. Modal logic
evaluates it against a **world** inside a structure, and the two modal
operators quantify over the worlds that world can see:

- `[]phi` holds at `w` when `phi` holds at **every** successor of `w`
- `<>phi` holds at `w` when `phi` holds at **some** successor of `w`

Everything surprising about modal logic follows from those two lines. A world
with no successors satisfies `[]phi` for every `phi`, including `[]false`, and
satisfies `<>phi` for none. That is not a corner case to be patched around; it
is what makes the logic able to say "nothing can happen from here".
"""

from __future__ import annotations


class Kripke:
    """A set of worlds, an accessibility relation, and a labelling."""

    def __init__(self, worlds, accessible, labels):
        """Store the worlds, their successors and the atoms true at each."""
        self.worlds = list(worlds)
        self.accessible = {world: list(accessible.get(world, [])) for world in self.worlds}
        self.labels = {world: set(labels.get(world, set())) for world in self.worlds}

    def successors(self, world):
        """The worlds one world can see."""
        return self.accessible[world]

    def holds(self, formula, world):
        """Whether a formula holds at a world.

        Evaluated bottom up over the formula and outwards over the relation,
        which is the order the exercise sheets fill their tables in: the atoms
        first, then each operator applied to the row below it.
        """
        kind = formula[0]

        if kind == "true":
            return True
        if kind == "false":
            return False
        if kind == "var":
            return formula[1] in self.labels[world]
        if kind == "!":
            return not self.holds(formula[1], world)
        if kind == "[]":
            return all(self.holds(formula[1], target)
                       for target in self.successors(world))
        if kind == "<>":
            return any(self.holds(formula[1], target)
                       for target in self.successors(world))

        left = self.holds(formula[1], world)
        right = self.holds(formula[2], world)

        if kind == "&":
            return left and right
        if kind == "|":
            return left or right
        if kind == "->":
            return (not left) or right
        return left == right

    def worlds_satisfying(self, formula):
        """Every world where a formula holds."""
        return [world for world in self.worlds if self.holds(formula, world)]

    def table(self, formulas):
        """The evaluation table the sheets ask for, one row per subformula."""
        return {text: [self.holds(formula, world) for world in self.worlds]
                for text, formula in formulas}

    def is_reflexive(self):
        """Whether every world sees itself, the frame condition behind `[]A -> A`."""
        return all(world in self.successors(world) for world in self.worlds)

    def is_transitive(self):
        """Whether the relation is transitive, the condition behind `[]A -> [][]A`."""
        for world in self.worlds:
            for middle in self.successors(world):
                for target in self.successors(middle):
                    if target not in self.successors(world):
                        return False
        return True

    def is_serial(self):
        """Whether every world has a successor, the condition behind `[]A -> <>A`.

        The condition that fails in world 2 of the sheet's structure, and the
        whole reason that world satisfies the implication vacuously.
        """
        return all(self.successors(world) for world in self.worlds)

    def __repr__(self):
        """The worlds with their labels and successors."""
        parts = []
        for world in self.worlds:
            labels = ",".join(sorted(self.labels[world])) or "-"
            parts.append(f"{world}[{labels}]->{self.successors(world)}")
        return " ".join(parts)
