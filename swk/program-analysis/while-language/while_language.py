"""The While language: syntax, labels, and the control flow functions of the lecture.

Every analysis in this folder starts here. A While program is a labelled
statement, and the four functions ``init``, ``final``, ``flow`` and ``blocks``
turn that syntax tree into the graph the analyses run on.

Concrete syntax, with the label written after the bracketed block, exactly as
the lecture writes it::

    [y := x]1; [z := 1]2;
    while [y > 1]3 do ([z := x * y]4; [y := y - 1]5);
    [y := 0]6

Labels identify statements uniquely, which the lecture assumes throughout and
``parse`` enforces.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class Expression:
    """Base class of arithmetic and boolean expressions."""

    def variables(self):
        """Every variable name occurring in the expression."""
        raise NotImplementedError

    def evaluate(self, state):
        """The value of the expression under a mapping from names to values."""
        raise NotImplementedError


@dataclass(frozen=True)
class Num(Expression):
    """An integer literal."""

    value: int

    def variables(self):
        """No variables occur in a literal."""
        return frozenset()

    def evaluate(self, state):
        """The literal itself."""
        return self.value

    def __str__(self):
        """The literal."""
        return str(self.value)


@dataclass(frozen=True)
class Bool(Expression):
    """A boolean literal."""

    value: bool

    def variables(self):
        """No variables occur in a literal."""
        return frozenset()

    def evaluate(self, state):
        """The literal itself."""
        return self.value

    def __str__(self):
        """The boolean literal."""
        return "true" if self.value else "false"


@dataclass(frozen=True)
class Var(Expression):
    """A variable reference."""

    name: str

    def variables(self):
        """The variable itself."""
        return frozenset({self.name})

    def evaluate(self, state):
        """The value bound to the name, which must be present in the state."""
        if self.name not in state:
            raise KeyError(f"{self.name} is not bound in this state")
        return state[self.name]

    def __str__(self):
        """The variable name."""
        return self.name


@dataclass(frozen=True)
class BinOp(Expression):
    """An arithmetic, relational or boolean operator applied to two operands."""

    op: str
    left: Expression
    right: Expression

    def variables(self):
        """Every variable of either operand."""
        return self.left.variables() | self.right.variables()

    def evaluate(self, state):
        """Apply the operator to the evaluated operands.

        Division is integer division, and division by zero raises rather than
        returning a value, which is what makes it visible to the analyses that
        care.
        """
        left = self.left.evaluate(state)
        right = self.right.evaluate(state)
        return _APPLY[self.op](left, right)

    def __str__(self):
        """The operation, bracketed."""
        return f"({self.left} {self.op} {self.right})"


@dataclass(frozen=True)
class Not(Expression):
    """Boolean negation."""

    operand: Expression

    def variables(self):
        """Every variable of the operand."""
        return self.operand.variables()

    def evaluate(self, state):
        """The negated value of the operand."""
        return not self.operand.evaluate(state)

    def __str__(self):
        """The negation."""
        return f"!{self.operand}"


_APPLY = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a // b,
    "%": lambda a, b: a % b,
    "<": lambda a, b: a < b,
    ">": lambda a, b: a > b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    "=": lambda a, b: a == b,
    "!=": lambda a, b: a != b,
    "&&": lambda a, b: a and b,
    "||": lambda a, b: a or b,
}


class Statement:
    """Base class of While statements."""


@dataclass(frozen=True)
class Assign(Statement):
    """A labelled assignment ``[x := a]^l``."""

    label: int
    variable: str
    expression: Expression

    def __str__(self):
        """The assignment with its label, as the lecture writes it."""
        return f"[{self.variable} := {self.expression}]{self.label}"


@dataclass(frozen=True)
class Skip(Statement):
    """A labelled ``[skip]^l``."""

    label: int

    def __str__(self):
        """The labelled skip."""
        return f"[skip]{self.label}"


@dataclass(frozen=True)
class Seq(Statement):
    """The sequential composition ``S1; S2``.

    Composition carries no label of its own: the lecture labels elementary
    blocks only, and a sequence is not one.
    """

    first: Statement
    second: Statement

    def __str__(self):
        """Both statements, separated by a semicolon."""
        return f"{self.first}; {self.second}"


@dataclass(frozen=True)
class If(Statement):
    """A conditional ``if [b]^l then S1 else S2``."""

    label: int
    condition: Expression
    then_branch: Statement
    else_branch: Statement

    def __str__(self):
        """The conditional with its labelled test."""
        return (f"if [{self.condition}]{self.label} then ({self.then_branch}) "
                f"else ({self.else_branch})")


@dataclass(frozen=True)
class While(Statement):
    """A loop ``while [b]^l do S``."""

    label: int
    condition: Expression
    body: Statement

    def __str__(self):
        """The loop with its labelled test."""
        return f"while [{self.condition}]{self.label} do ({self.body})"


@dataclass(frozen=True)
class Block:
    """One elementary block: an assignment, a skip, or a test.

    The lecture writes these as ``[x := a]^l``, ``[skip]^l`` and ``[b]^l``.
    Tests appear as blocks even though they are part of a larger statement,
    which is what lets the analyses treat a loop head as a node of its own.
    """

    label: int
    kind: str
    variable: str = None
    expression: Expression = None

    def variables(self):
        """Every variable occurring in the block, assigned or read."""
        names = self.expression.variables() if self.expression is not None else frozenset()
        return names | ({self.variable} if self.variable else frozenset())

    def __str__(self):
        """The block in the notation used by the data flow tables."""
        if self.kind == "assign":
            return f"[{self.variable} := {self.expression}]{self.label}"
        if self.kind == "skip":
            return f"[skip]{self.label}"
        return f"[{self.expression}]{self.label}"


def blocks(statement):
    """Every elementary block of a statement, as a dictionary keyed by label.

    ``blocks`` of the lecture returns a set; a dictionary is returned here
    because every analysis needs to look a block up by its label, and the
    labels are unique by assumption.
    """
    found = {}
    _collect_blocks(statement, found)
    return found


def _collect_blocks(statement, found):
    """Collects the labelled blocks of the statement."""
    if isinstance(statement, Assign):
        found[statement.label] = Block(statement.label, "assign",
                                       statement.variable, statement.expression)
    elif isinstance(statement, Skip):
        found[statement.label] = Block(statement.label, "skip")
    elif isinstance(statement, Seq):
        _collect_blocks(statement.first, found)
        _collect_blocks(statement.second, found)
    elif isinstance(statement, If):
        found[statement.label] = Block(statement.label, "test",
                                       expression=statement.condition)
        _collect_blocks(statement.then_branch, found)
        _collect_blocks(statement.else_branch, found)
    elif isinstance(statement, While):
        found[statement.label] = Block(statement.label, "test",
                                       expression=statement.condition)
        _collect_blocks(statement.body, found)
    else:
        raise TypeError(f"not a While statement: {statement!r}")


def labels(statement):
    """Every label occurring in the statement."""
    return set(blocks(statement))


def init(statement):
    """The label of the block that runs first.

    A single label, not a set: a While program has exactly one entry point.
    """
    if isinstance(statement, (Assign, Skip, If, While)):
        return statement.label
    if isinstance(statement, Seq):
        return init(statement.first)
    raise TypeError(f"not a While statement: {statement!r}")


def final(statement):
    """The labels of the blocks that can run last.

    A set, because a conditional can end in either branch. A loop ends at its
    test, since leaving the loop means the test failed.
    """
    if isinstance(statement, (Assign, Skip)):
        return {statement.label}
    if isinstance(statement, Seq):
        return final(statement.second)
    if isinstance(statement, If):
        return final(statement.then_branch) | final(statement.else_branch)
    if isinstance(statement, While):
        return {statement.label}
    raise TypeError(f"not a While statement: {statement!r}")


def flow(statement):
    """The control flow relation: pairs of labels that can follow each other.

    This is the edge set of the control flow graph. The definition is
    syntax-directed, so it is computed without ever running the program.

    The loop case is the interesting one: it produces an edge from the test
    into the body and an edge from every final label of the body back to the
    test. The edge that leaves the loop is not here, it comes from whatever
    follows the loop in a sequence.
    """
    if isinstance(statement, (Assign, Skip)):
        return set()
    if isinstance(statement, Seq):
        return (flow(statement.first) | flow(statement.second)
                | {(label, init(statement.second)) for label in final(statement.first)})
    if isinstance(statement, If):
        return (flow(statement.then_branch) | flow(statement.else_branch)
                | {(statement.label, init(statement.then_branch)),
                   (statement.label, init(statement.else_branch))})
    if isinstance(statement, While):
        return (flow(statement.body)
                | {(statement.label, init(statement.body))}
                | {(label, statement.label) for label in final(statement.body)})
    raise TypeError(f"not a While statement: {statement!r}")


def reverse_flow(statement):
    """The control flow relation with every edge turned around.

    Backward analyses such as live variables run on this, which is the only
    difference between them and the forward ones.
    """
    return {(target, source) for source, target in flow(statement)}


def free_variables(statement):
    """Every variable occurring anywhere in the statement."""
    names = set()
    for block in blocks(statement).values():
        names |= set(block.variables())
    return names


def assignments(statement):
    """Every label that assigns to a variable, grouped by variable name."""
    found = {}
    for block in blocks(statement).values():
        if block.kind == "assign":
            found.setdefault(block.variable, set()).add(block.label)
    return found


class ParseError(Exception):
    """Raised when the input is not a syntactically correct While program."""


@dataclass
class _Token:
    """One token of the source, with the position it came from."""
    kind: str
    text: str
    position: int


_KEYWORDS = {"while", "do", "if", "then", "else", "skip", "true", "false"}
_OPERATORS = ["<=", ">=", "!=", "&&", "||", ":=", "+", "-", "*", "/", "%", "<", ">", "=", "!"]


def tokenise(text):
    """Split the source into tokens.

    Two-character operators are tried before one-character ones, or ``<=``
    would come out as ``<`` followed by ``=``.
    """
    tokens = []
    position = 0

    while position < len(text):
        character = text[position]

        if character.isspace():
            position += 1
            continue

        if character in "[]();":
            tokens.append(_Token(character, character, position))
            position += 1
            continue

        if character.isdigit():
            start = position
            while position < len(text) and text[position].isdigit():
                position += 1
            tokens.append(_Token("number", text[start:position], start))
            continue

        if character.isalpha() or character == "_":
            start = position
            while position < len(text) and (text[position].isalnum() or text[position] == "_"):
                position += 1
            word = text[start:position]
            tokens.append(_Token(word if word in _KEYWORDS else "name", word, start))
            continue

        for operator in _OPERATORS:
            if text.startswith(operator, position):
                tokens.append(_Token(operator, operator, position))
                position += len(operator)
                break
        else:
            raise ParseError(f"unexpected character {character!r} at {position}")

    tokens.append(_Token("end", "", len(text)))
    return tokens


class _Parser:
    """Recursive descent over the token stream."""

    def __init__(self, tokens):
        """A parser positioned at the first token."""
        self.tokens = tokens
        self.position = 0

    def peek(self):
        """The token at the current position."""
        return self.tokens[self.position]

    def take(self, kind=None):
        """Consumes the next token, checking its kind when one is given."""
        token = self.tokens[self.position]
        if kind is not None and token.kind != kind:
            raise ParseError(f"expected {kind!r} but found {token.text!r} at {token.position}")
        self.position += 1
        return token

    def statement(self):
        """Parses a sequence of statements."""
        first = self.single_statement()
        while self.peek().kind == ";":
            self.take(";")
            if self.peek().kind in ("end", ")"):
                break
            first = Seq(first, self.single_statement())
        return first

    def single_statement(self):
        """Parses one statement."""
        token = self.peek()

        if token.kind == "(":
            self.take("(")
            inner = self.statement()
            self.take(")")
            return inner

        if token.kind == "while":
            self.take("while")
            self.take("[")
            condition = self.expression()
            self.take("]")
            label = int(self.take("number").text)
            self.take("do")
            return While(label, condition, self.single_statement())

        if token.kind == "if":
            self.take("if")
            self.take("[")
            condition = self.expression()
            self.take("]")
            label = int(self.take("number").text)
            self.take("then")
            then_branch = self.single_statement()
            self.take("else")
            return If(label, condition, then_branch, self.single_statement())

        if token.kind == "[":
            self.take("[")
            if self.peek().kind == "skip":
                self.take("skip")
                self.take("]")
                return Skip(int(self.take("number").text))
            name = self.take("name").text
            self.take(":=")
            value = self.expression()
            self.take("]")
            return Assign(int(self.take("number").text), name, value)

        raise ParseError(f"unexpected {token.text!r} at {token.position}")

    def expression(self):
        """Parses an expression at the loosest binding level."""
        return self.disjunction()

    def disjunction(self):
        """Parses an alternation."""
        left = self.conjunction()
        while self.peek().kind == "||":
            self.take()
            left = BinOp("||", left, self.conjunction())
        return left

    def conjunction(self):
        """Parses a conjunction, which binds tighter."""
        left = self.comparison()
        while self.peek().kind == "&&":
            self.take()
            left = BinOp("&&", left, self.comparison())
        return left

    def comparison(self):
        """Parses a comparison, which binds tighter still."""
        left = self.sum()
        if self.peek().kind in ("<", ">", "<=", ">=", "=", "!="):
            operator = self.take().kind
            return BinOp(operator, left, self.sum())
        return left

    def sum(self):
        """Parses addition and subtraction."""
        left = self.product()
        while self.peek().kind in ("+", "-"):
            operator = self.take().kind
            left = BinOp(operator, left, self.product())
        return left

    def product(self):
        """Parses multiplication, division and remainder."""
        left = self.atom()
        while self.peek().kind in ("*", "/", "%"):
            operator = self.take().kind
            left = BinOp(operator, left, self.atom())
        return left

    def atom(self):
        """Parses a literal, a variable or a bracketed expression."""
        token = self.peek()

        if token.kind == "!":
            self.take("!")
            return Not(self.atom())
        if token.kind == "(":
            self.take("(")
            inner = self.expression()
            self.take(")")
            return inner
        if token.kind == "number":
            return Num(int(self.take("number").text))
        if token.kind == "true":
            self.take("true")
            return Bool(True)
        if token.kind == "false":
            self.take("false")
            return Bool(False)
        if token.kind == "name":
            return Var(self.take("name").text)

        raise ParseError(f"unexpected {token.text!r} at {token.position}")


def parse(text):
    """Parse a While program and check that its labels are unique.

    Uniqueness is an assumption of the whole lecture: labels identify
    statements, and every analysis keys its results by label. A program that
    reuses one is rejected here rather than producing quietly wrong analyses
    later.
    """
    parser = _Parser(tokenise(text))
    program = parser.statement()
    if parser.peek().kind != "end":
        token = parser.peek()
        raise ParseError(f"unexpected {token.text!r} at {token.position}")

    seen = []
    _collect_labels(program, seen)
    duplicates = {label for label in seen if seen.count(label) > 1}
    if duplicates:
        raise ParseError(f"labels are not unique: {sorted(duplicates)}")

    return program


def _collect_labels(statement, seen):
    """Collects the labels in the order the program uses them."""
    if isinstance(statement, (Assign, Skip)):
        seen.append(statement.label)
    elif isinstance(statement, Seq):
        _collect_labels(statement.first, seen)
        _collect_labels(statement.second, seen)
    elif isinstance(statement, If):
        seen.append(statement.label)
        _collect_labels(statement.then_branch, seen)
        _collect_labels(statement.else_branch, seen)
    elif isinstance(statement, While):
        seen.append(statement.label)
        _collect_labels(statement.body, seen)


LECTURE_EXAMPLE = """
[y := x]1; [z := 1]2;
while [y > 1]3 do ([z := x * y]4; [y := y - 1]5);
[y := 0]6
"""
"""The running example of the lecture, used by every folder in this topic.

It looks like a factorial and is not one: the body assigns ``z := x * y``
rather than ``z := z * y``, so every iteration overwrites the product instead
of accumulating it. The lecture uses it to demonstrate control flow, not to
compute anything, and the analyses here inherit it for the same reason.
"""
