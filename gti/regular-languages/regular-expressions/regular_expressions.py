"""Regular expressions: syntax, semantics, and the languages they describe.

The course defines them inductively, and so does this module. A regular
expression over an alphabet is

    empty set | epsilon | a symbol | union | concatenation | Kleene star

and everything else, including ``+`` and ``?``, is an abbreviation. Keeping the
core that small is what makes the proofs short: an induction over the syntax
has five cases.

The semantics is a language, which is a set of words and usually infinite. So
two operations are offered instead of one: enumerate the words up to a length,
which is always finite, and match a single word, which is decided by Brzozowski
derivatives without building an automaton at all.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

EPSILON = ""


class Regex:
    """Base class of regular expressions."""

    def symbols(self):
        """Every alphabet symbol occurring in the expression."""
        raise NotImplementedError

    def nullable(self):
        """Whether the language contains the empty word."""
        raise NotImplementedError

    def derivative(self, symbol):
        """The Brzozowski derivative: what remains after reading one symbol.

        Defined so that ``w in L(derivative(a))`` exactly when ``a + w`` is in
        ``L(self)``. Matching is then reading the word one symbol at a time and
        asking at the end whether the remainder is nullable, which is a
        complete matcher in five recursive cases and no automaton.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class Empty(Regex):
    """The empty set, matching nothing at all."""

    def symbols(self):
        """No symbols occur."""
        return frozenset()

    def nullable(self):
        """The empty set does not contain the empty word."""
        return False

    def derivative(self, symbol):
        """Nothing remains of nothing."""
        return self

    def __str__(self):
        """The written form of the empty language."""
        return "empty"


@dataclass(frozen=True)
class Epsilon(Regex):
    """The language containing exactly the empty word."""

    def symbols(self):
        """No symbols occur."""
        return frozenset()

    def nullable(self):
        """The empty word is in this language by definition."""
        return True

    def derivative(self, symbol):
        """Reading anything at all leaves nothing."""
        return Empty()

    def __str__(self):
        """The written form of the empty word."""
        return "eps"


@dataclass(frozen=True)
class Symbol(Regex):
    """A single alphabet symbol."""

    value: str

    def symbols(self):
        """The symbol itself."""
        return frozenset({self.value})

    def nullable(self):
        """A single symbol is not the empty word."""
        return False

    def derivative(self, symbol):
        """Reading the symbol leaves the empty word; anything else fails."""
        return Epsilon() if symbol == self.value else Empty()

    def __str__(self):
        """The symbol itself."""
        return self.value


@dataclass(frozen=True)
class Union(Regex):
    """The union of two languages, written with a vertical bar."""

    left: Regex
    right: Regex

    def symbols(self):
        """The symbols of both sides."""
        return self.left.symbols() | self.right.symbols()

    def nullable(self):
        """A union contains the empty word if either side does."""
        return self.left.nullable() or self.right.nullable()

    def derivative(self, symbol):
        """The derivative distributes over union."""
        return union(self.left.derivative(symbol), self.right.derivative(symbol))

    def __str__(self):
        """The alternative, always bracketed so the parse is unambiguous."""
        return f"({self.left}|{self.right})"


@dataclass(frozen=True)
class Concat(Regex):
    """The concatenation of two languages."""

    left: Regex
    right: Regex

    def symbols(self):
        """The symbols of both sides."""
        return self.left.symbols() | self.right.symbols()

    def nullable(self):
        """A concatenation contains the empty word only if both sides do."""
        return self.left.nullable() and self.right.nullable()

    def derivative(self, symbol):
        """Two cases, because the first part may be skipped.

        If the left side can match the empty word, the symbol may belong to
        the right side instead, so both possibilities are kept.
        """
        first = concat(self.left.derivative(symbol), self.right)
        if self.left.nullable():
            return union(first, self.right.derivative(symbol))
        return first

    def __str__(self):
        """The concatenation, bracketed for the same reason."""
        return f"({self.left}{self.right})"


@dataclass(frozen=True)
class Star(Regex):
    """Kleene star: any number of repetitions, including none."""

    inner: Regex

    def symbols(self):
        """The symbols of the inner expression."""
        return self.inner.symbols()

    def nullable(self):
        """A star always contains the empty word."""
        return True

    def derivative(self, symbol):
        """One repetition is consumed and the star remains available."""
        return concat(self.inner.derivative(symbol), self)

    def __str__(self):
        """The starred expression."""
        return f"({self.inner})*"


def union(left, right):
    """Build a union, simplifying the trivial cases.

    Simplification is not cosmetic here. Derivatives grow the expression on
    every symbol, and without collapsing empty sets and duplicates the terms
    double in size per step, which turns matching into an exponential walk.
    """
    if isinstance(left, Empty):
        return right
    if isinstance(right, Empty):
        return left
    if left == right:
        return left
    return Union(left, right)


def concat(left, right):
    """Build a concatenation, simplifying the trivial cases."""
    if isinstance(left, Empty) or isinstance(right, Empty):
        return Empty()
    if isinstance(left, Epsilon):
        return right
    if isinstance(right, Epsilon):
        return left
    return Concat(left, right)


def star(inner):
    """Build a star, simplifying the trivial cases."""
    if isinstance(inner, (Empty, Epsilon)):
        return Epsilon()
    if isinstance(inner, Star):
        return inner
    return Star(inner)


def plus(inner):
    """One or more repetitions, which is the abbreviation ``r+ = r r*``."""
    return concat(inner, star(inner))


def optional(inner):
    """Zero or one repetition, which is the abbreviation ``r? = eps | r``."""
    return union(Epsilon(), inner)


def matches(expression, word):
    """Whether the expression matches a word, by repeated differentiation.

    No automaton is built. Each symbol replaces the expression by its
    derivative, and the word is accepted when what is left contains the empty
    word. Brzozowski published this in 1964 and it is still the shortest
    correct matcher there is.
    """
    current = expression
    for symbol in word:
        current = current.derivative(symbol)
        if isinstance(current, Empty):
            return False
    return current.nullable()


def language(expression, max_length, alphabet=None):
    """Every word up to a length that the expression matches.

    The language itself is usually infinite, so a bound is required. This is
    the standard way to compare two expressions in practice, and it is only a
    test: agreement up to length k proves nothing about longer words.

    Words come out in shortlex order, shortest first and alphabetically within
    a length, which is the same order the automata in this folder use so that
    two results can be compared directly.
    """
    alphabet = sorted(alphabet or expression.symbols())
    found = []
    queue = [""]

    while queue:
        word = queue.pop(0)
        if matches(expression, word):
            found.append(word)
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in alphabet)

    return found


def equivalent_up_to(first, second, max_length, alphabet=None):
    """Compare two expressions on all words up to a length.

    Returns the first word where they disagree, or None. Deciding real
    equivalence needs automata, which is what the
    [decision algorithms](../decision-algorithms/) folder does; this is the
    cheap check that catches most mistakes.
    """
    alphabet = sorted(alphabet or (first.symbols() | second.symbols()))
    queue = [""]

    while queue:
        word = queue.pop(0)
        if matches(first, word) != matches(second, word):
            return word
        if len(word) < max_length:
            queue.extend(word + symbol for symbol in alphabet)

    return None


class ParseError(Exception):
    """Raised when the input is not a regular expression."""


def parse(text):
    """Parse a regular expression in the usual notation.

    Concatenation is written by juxtaposition, ``|`` is union, ``*`` is star,
    and ``+`` and ``?`` are the usual abbreviations. The empty word is ``eps``
    or the character epsilon, and the empty set is ``empty`` or the character
    for the empty set. Precedence is star over concatenation over union, which
    is what makes ``ab*|c`` mean what it looks like.

    A backslash escapes the next character, so ``\+`` is the symbol plus
    rather than the repetition operator.

    Digits are ordinary alphabet symbols. Writing the empty set as ``0``, the
    way some textbooks do, would silently turn the pattern ``(0|1)+`` into
    ``1+``, which is the kind of collision that produces a wrong answer with no
    error message.
    """
    parser = _Parser(text)
    result = parser.union()
    parser.skip_spaces()
    if parser.position < len(parser.text):
        raise ParseError(f"unexpected {parser.text[parser.position]!r} at {parser.position}")
    return result


class _Parser:
    """Recursive descent, one method per precedence level."""

    def __init__(self, text):
        """A parser positioned at the start of the text."""
        self.text = text
        self.position = 0

    def skip_spaces(self):
        """Advances past whitespace, which the grammar ignores."""
        while self.position < len(self.text) and self.text[self.position].isspace():
            self.position += 1

    def peek(self):
        """The next character, or None at the end of the text."""
        self.skip_spaces()
        return self.text[self.position] if self.position < len(self.text) else None

    def union(self):
        """Parses alternatives, the loosest binding level."""
        result = self.concatenation()
        while self.peek() == "|":
            self.position += 1
            result = union(result, self.concatenation())
        return result

    def concatenation(self):
        """Parses a sequence, which binds tighter than alternation."""
        result = None
        while True:
            character = self.peek()
            if character is None or character in "|)":
                break
            part = self.repetition()
            result = part if result is None else concat(result, part)
        return result if result is not None else Epsilon()

    def repetition(self):
        """Parses the postfix operators, which bind tightest."""
        result = self.atom()
        while True:
            character = self.peek()
            if character == "*":
                self.position += 1
                result = star(result)
            elif character == "+":
                self.position += 1
                result = plus(result)
            elif character == "?":
                self.position += 1
                result = optional(result)
            else:
                return result

    def atom(self):
        """Parses a symbol or a bracketed expression."""
        self.skip_spaces()
        if self.position >= len(self.text):
            raise ParseError("unexpected end of expression")

        character = self.text[self.position]

        if character == "(":
            self.position += 1
            inner = self.union()
            if self.peek() != ")":
                raise ParseError(f"missing ) at {self.position}")
            self.position += 1
            return inner

        if character == "\\":
            if self.position + 1 >= len(self.text):
                raise ParseError("a backslash must be followed by a character")
            self.position += 2
            return Symbol(self.text[self.position - 1])

        if self.text.startswith("eps", self.position):
            self.position += 3
            return Epsilon()

        if character == "\u03b5":
            self.position += 1
            return Epsilon()

        if self.text.startswith("empty", self.position):
            self.position += 5
            return Empty()

        if character == "\u2205":
            self.position += 1
            return Empty()

        if character in "|)*+?":
            raise ParseError(f"unexpected {character!r} at {self.position}")

        self.position += 1
        return Symbol(character)
