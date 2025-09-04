"""Three-address code: the shape every intermediate representation has.

Each instruction has an operator and at most three addresses, one target and
two operands. A tree of arbitrary depth becomes a flat list, with temporaries
holding what used to be subtrees.

Flattening is what makes the later phases possible. A register allocator needs
to know when a value is live, an optimiser needs to compare expressions, and
neither can do that on a tree where a value has no name.
"""

from __future__ import annotations

_counter = {"temporary": 0, "label": 0}


class Instruction:
    """One three-address instruction: `target := left op right`."""

    def __init__(self, target, operator, left, right=None):
        """Record the target, the operator and up to two operands."""
        self.target = target
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        """The instruction in the usual notation."""
        if self.right is None:
            return f"{self.target} := {self.left}"
        return f"{self.target} := {self.left} {self.operator} {self.right}"

    def __eq__(self, other):
        """Two instructions are equal when all four fields agree."""
        return (isinstance(other, Instruction) and self.target == other.target
                and self.operator == other.operator
                and self.left == other.left and self.right == other.right)


def reset():
    """Restart the temporary and label counters, for reproducible output."""
    _counter["temporary"] = 0
    _counter["label"] = 0


def fresh_temporary():
    """A new temporary name."""
    name = f"t{_counter['temporary']}"
    _counter["temporary"] += 1
    return name


def fresh_label():
    """A new label name."""
    name = f"L{_counter['label']}"
    _counter["label"] += 1
    return name


def generate(tree):
    """Flatten an expression tree into three-address code.

    Post-order, because an operator needs its operands' names before it can be
    emitted. The temporaries are therefore numbered in evaluation order, which
    is also the order a stack machine would push them, and the reason the two
    representations convert into each other so easily.
    """
    reset()
    code = []
    _emit(tree, code)
    return code


def _emit(tree, code):
    """Emit code for one subtree and return the name holding its value."""
    kind = tree[0]

    if kind == "num":
        return str(tree[1])
    if kind == "var":
        return tree[1]

    left = _emit(tree[1], code)
    right = _emit(tree[2], code)
    target = fresh_temporary()
    code.append(Instruction(target, kind, left, right))
    return target


def interpret(code, environment=None):
    """Run three-address code, returning the last computed value.

    Not a compiler's job, but it is what makes a translation testable: the
    generated code and the original tree must produce the same number, and
    that is a much stronger check than inspecting the instruction list.
    """
    values = dict(environment or {})
    result = None

    for line in code:
        left = _value(line.left, values)
        right = _value(line.right, values) if line.right is not None else None

        if line.operator == "+":
            result = left + right
        elif line.operator == "-":
            result = left - right
        elif line.operator == "*":
            result = left * right
        elif line.operator == "/":
            result = left // right
        else:
            result = left

        values[line.target] = result

    return result


def _value(name, values):
    """A name or a literal, resolved to a number."""
    if name is None:
        return None
    if name in values:
        return values[name]
    return int(name)


def used_names(code):
    """Every name the code reads, which is what a liveness analysis starts from."""
    names = set()
    for line in code:
        for operand in (line.left, line.right):
            if operand is not None and not operand.lstrip("-").isdigit():
                names.add(operand)
    return names


def defined_names(code):
    """Every name the code writes."""
    return {line.target for line in code}
