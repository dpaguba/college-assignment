"""Context-free grammars: rules, derivations, and the trees they produce.

A grammar is a set of variables, a set of terminals, a start variable and
rules of the form ``A -> alpha`` where alpha is any string of symbols. The
left side is always a single variable, and that restriction is exactly what
"context-free" means: a variable is replaced without looking at what surrounds
it.

The step up from regular languages is real. A grammar can count, because a
rule may put symbols on both sides of a recursive call, which is what makes
``a^n b^n`` expressible here and impossible one level down.
"""

from __future__ import annotations

from dataclasses import dataclass, field

EPSILON = ()


@dataclass
class Grammar:
    """Variables, terminals, rules and a start symbol.

    ``rules`` maps a variable to a list of right-hand sides, each a tuple of
    symbols. The empty tuple is the empty word.
    """

    variables: set
    terminals: set
    rules: dict
    start: str
    name: str = "G"

    def productions(self):
        """Every rule as a (variable, right-hand side) pair, in a stable order."""
        return [(variable, right)
                for variable in sorted(self.rules)
                for right in self.rules[variable]]

    def is_variable(self, symbol):
        """Whether a symbol is a variable of this grammar."""
        return symbol in self.variables

    def add(self, variable, right):
        """Add one rule, keeping the right-hand sides free of duplicates."""
        self.variables.add(variable)
        sides = self.rules.setdefault(variable, [])
        if tuple(right) not in sides:
            sides.append(tuple(right))

    def copy(self, name=None):
        """A deep enough copy that changing the rules does not affect the original."""
        return Grammar(set(self.variables), set(self.terminals),
                       {variable: list(sides) for variable, sides in self.rules.items()},
                       self.start, name or self.name)

    def derive_step(self, sentential, position=None, leftmost=True):
        """Every sentential form reachable by replacing one variable.

        With ``leftmost`` the first variable is the only one replaced, which is
        the canonical derivation order a parser follows.
        """
        indices = [index for index, symbol in enumerate(sentential)
                   if self.is_variable(symbol)]
        if not indices:
            return []

        chosen = [indices[0]] if leftmost else (indices if position is None else [position])
        results = []

        for index in chosen:
            for right in self.rules.get(sentential[index], []):
                results.append(sentential[:index] + tuple(right) + sentential[index + 1:])

        return results

    def derivations(self, word, max_steps=25, leftmost=True):
        """Search for a derivation of a word, returning the sequence of forms.

        Breadth-first over sentential forms, with two prunings that make it
        terminate in practice: a form longer than the target is dropped, and so
        is one whose terminal prefix already disagrees.

        This is not a parser. It is the definition, run forwards, and it is
        here so that a derivation can be printed the way an exercise asks. For
        deciding membership use [CYK](../cyk/), which is cubic and complete.
        """
        start = (self.start,)
        queue = [(start, [start])]
        seen = {start}

        while queue:
            form, history = queue.pop(0)

            if form == tuple(word):
                return history
            if len(history) > max_steps:
                continue

            for following in self.derive_step(form, leftmost=leftmost):
                if len(following) > len(word) + 2 or following in seen:
                    continue
                if not self._prefix_possible(following, word):
                    continue
                seen.add(following)
                queue.append((following, history + [following]))

        return None

    def _prefix_possible(self, form, word):
        """Whether the terminals already fixed still agree with the target."""
        position = 0
        for symbol in form:
            if self.is_variable(symbol):
                return True
            if position >= len(word) or word[position] != symbol:
                return False
            position += 1
        return position == len(word)

    def language(self, max_length, max_steps=14):
        """Every word up to a length the grammar can derive.

        Breadth-first over sentential forms, keeping those whose terminals
        cannot already exceed the bound. Exponential in the worst case and
        adequate for the small grammars the exercises use.
        """
        found = set()
        queue = [(self.start,)]
        seen = {(self.start,)}
        steps = 0

        while queue and steps < max_steps:
            steps += 1
            following = []

            for form in queue:
                if all(not self.is_variable(symbol) for symbol in form):
                    if len(form) <= max_length:
                        found.add("".join(form))
                    continue

                for produced in self.derive_step(form, leftmost=False):
                    terminals = sum(1 for symbol in produced if not self.is_variable(symbol))
                    if terminals > max_length or produced in seen:
                        continue
                    if len(produced) > max_length + len(self.variables) + 2:
                        continue
                    seen.add(produced)
                    following.append(produced)

            queue = following

        return sorted(found, key=lambda word: (len(word), word))

    def is_ambiguous(self, max_length=6):
        """Look for a word with two different leftmost derivations.

        Ambiguity is **undecidable** in general, so this can only ever find a
        witness, never prove there is none. What it returns is a word and two
        parse trees, which is exactly what an exercise asks for.

        The bounded search uses [CYK](../cyk/) counting instead of enumerating
        derivations, because the number of derivations grows much faster than
        the number of words.
        """
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cyk"))
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "chomsky-normal-form"))

        from chomsky_normal_form import to_chomsky_normal_form
        from cyk import count_parses

        normal = to_chomsky_normal_form(self)

        for word in self.language(max_length):
            if not word:
                continue
            if count_parses(normal, word) > 1:
                return word

        return None

    def __str__(self):
        """The rules, one line per variable, starting with the start symbol."""
        rows = [f"{self.name}: start {self.start}"]
        for variable in sorted(self.rules, key=lambda name: (name != self.start, name)):
            sides = " | ".join("".join(right) if right else "eps"
                               for right in self.rules[variable])
            rows.append(f"  {variable} -> {sides}")
        return "\n".join(rows)


def parse_grammar(text, start=None, name="G"):
    """Read a grammar from the notation the exercises use.

    ::

        S -> Dd | Aa | aE
        A -> Da | aD | B

    Variables are the symbols appearing on a left-hand side, so a name of more
    than one character such as ``Wa`` works as long as it has its own rule.
    Right-hand sides are tokenised by longest match against that set, and
    anything else is a terminal. ``eps`` denotes the empty word.
    """
    lines = [line.strip() for line in text.strip().split("\n") if line.strip()]
    variables = []

    for line in lines:
        head, _, _ = line.partition("->")
        variables.append(head.strip())

    order = sorted(set(variables), key=len, reverse=True)
    rules = {}
    terminals = set()

    for line in lines:
        head, _, body = line.partition("->")
        variable = head.strip()

        for alternative in body.split("|"):
            alternative = alternative.strip()
            if alternative in ("eps", "ε", ""):
                rules.setdefault(variable, []).append(())
                continue

            symbols = _tokenise(alternative, order)
            for symbol in symbols:
                if symbol not in variables:
                    terminals.add(symbol)
            rules.setdefault(variable, []).append(tuple(symbols))

    return Grammar(set(variables), terminals, rules, start or variables[0], name)


def _tokenise(text, variable_names):
    """Split a right-hand side, matching the longest declared variable first."""
    symbols = []
    position = 0

    while position < len(text):
        if text[position].isspace():
            position += 1
            continue

        for name in variable_names:
            if text.startswith(name, position):
                symbols.append(name)
                position += len(name)
                break
        else:
            symbols.append(text[position])
            position += 1

    return symbols
