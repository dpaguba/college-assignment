"""The abstract syntax tree: the parse tree with the grammar thrown away.

A parse tree records how the parser worked. It contains a node for every rule
application, including the chains `E ::= T ::= F` that exist only to encode
precedence, and the brackets that exist only to override it. None of that is
needed once the tree is built, and all of it gets in the way of every later
phase.

An abstract syntax tree keeps the operators and the operands and nothing else.
The precedence is not lost, it has been **absorbed into the shape**: the parse
tree encodes it in the derivation, the syntax tree in which node is whose
child.
"""

from __future__ import annotations


class Node:
    """A syntax tree node: an operator or a leaf, plus an optional value."""

    def __init__(self, label, children=None, value=None):
        """Create a node with a label, optional children and an optional value."""
        self.label = label
        self.children = children if children is not None else []
        self.value = value

    def is_leaf(self):
        """Whether the node has no children."""
        return not self.children

    def __repr__(self):
        """Prefix form, which reads as the tree shape."""
        if self.is_leaf():
            return f"{self.label}={self.value}" if self.value is not None else self.label
        return f"({self.label} {' '.join(repr(child) for child in self.children)})"

    def __eq__(self, other):
        """Structural equality, ignoring nothing: labels, children and values."""
        return (isinstance(other, Node) and self.label == other.label
                and self.value == other.value and self.children == other.children)


def from_parse_tree(node, shape):
    """Fold a parse tree into a syntax tree, guided by a per-rule instruction.

    The instruction for a rule is one of four:

    - `("binary", op)` keeps the two operand children and labels the node
    - `("bracket",)` keeps the middle child and drops the parentheses
    - `("chain",)` replaces the node by its only child
    - `("leaf",)` keeps the terminal

    Writing this table out is what a compiler does with semantic actions
    attached to the grammar rules; separating it makes visible that the shape
    of the syntax tree is a **choice**, not something the grammar dictates.
    """
    if not node.children:
        return Node(node.symbol)

    key = (node.symbol, tuple(child.symbol for child in node.children))
    instruction = shape.get(key)

    if instruction is None:
        kept = [from_parse_tree(child, shape) for child in node.children]
        return kept[0] if len(kept) == 1 else Node(node.symbol, kept)

    kind = instruction[0]

    if kind == "chain":
        return from_parse_tree(node.children[0], shape)
    if kind == "leaf":
        return Node(node.children[0].symbol)
    if kind == "bracket":
        return from_parse_tree(node.children[1], shape)

    left = from_parse_tree(node.children[0], shape)
    right = from_parse_tree(node.children[2], shape)
    return Node(instruction[1], [left, right])


def count_nodes(node):
    """Nodes in a syntax tree."""
    return 1 + sum(count_nodes(child) for child in node.children)


def count_nodes_of_parse_tree(node):
    """Nodes in a parse tree, for comparing the two representations."""
    return 1 + sum(count_nodes_of_parse_tree(child) for child in node.children)


def with_values(node, values):
    """Attach numbers to the leaves, left to right.

    A scanner delivers the value of a numeric literal alongside the token, so
    the parser never sees the digits. Splitting that here keeps the tree shape
    independent of the values it is tested with.
    """
    remaining = list(values)

    def walk(current):
        """Copy the tree, consuming one value per leaf."""
        if current.is_leaf():
            return Node(current.label, value=remaining.pop(0))
        return Node(current.label, [walk(child) for child in current.children])

    return walk(node)


def evaluate(node):
    """Evaluate an arithmetic syntax tree.

    The simplest possible tree walk, and the reason the tree is built at all:
    every later phase is a walk like this one, and each is short because the
    tree already says what belongs to what.
    """
    if node.is_leaf():
        return node.value

    left, right = (evaluate(child) for child in node.children)

    if node.label == "+":
        return left + right
    if node.label == "-":
        return left - right
    if node.label == "*":
        return left * right
    if node.label == "/":
        if right == 0:
            raise ZeroDivisionError("division by zero in the syntax tree")
        return left / right if left % right else left // right

    raise ValueError(f"unknown operator {node.label}")


def postorder(node):
    """Children before parents, which is the order evaluation needs."""
    for child in node.children:
        yield from postorder(child)
    yield node


def preorder(node):
    """Parents before children, which is the order printing needs."""
    yield node
    for child in node.children:
        yield from preorder(child)


def to_tokens(node):
    """Print the tree back as a token sequence, bracketing where needed.

    Brackets are re-inserted only where the shape demands them, which is the
    test that the tree really carries the precedence: printing and reparsing
    has to give back the same tree, and it does for every expression tried.
    """
    if node.is_leaf():
        return [node.label]

    left, right = node.children
    tokens = _side(left, node.label, False) + [node.label] + _side(right, node.label, True)
    return tokens


def _side(child, parent, is_right):
    """One operand, wrapped in brackets when the precedence requires it."""
    tokens = to_tokens(child)
    if child.is_leaf():
        return tokens

    if _precedence(child.label) < _precedence(parent):
        return ["("] + tokens + [")"]
    if is_right and _precedence(child.label) == _precedence(parent):
        return ["("] + tokens + [")"]
    return tokens


def _precedence(operator):
    """Binding strength, higher binds tighter."""
    return 2 if operator in ("*", "/") else 1


def height(node):
    """Height of the tree, which bounds the recursion depth of every walk."""
    if node.is_leaf():
        return 1
    return 1 + max(height(child) for child in node.children)
