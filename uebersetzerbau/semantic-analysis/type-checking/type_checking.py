"""Type checking as a derivation, in the style of the lecture's rules.

A typing judgement is written `L, C, M, V |- e : t`: under a class table `L`,
inside class `C`, in method `M`, with variables `V`, the expression `e` has
type `t`. A rule has premises above the line and a conclusion below, and a
program is type-correct exactly when a derivation exists.

Implementing it as a derivation rather than as a boolean has one concrete
benefit: when a program fails to check, the partial derivation says which
premise could not be established, which is the difference between a usable
error message and "type error".

The sheet's fragment is the interesting case, because static correctness and
runtime success come apart:

    B x; if (x == null) x = (B)this;

checks in class `C` where `B` is a subclass of `C`, and throws
`ClassCastException` when it runs, because `this` is definitely a `C`.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "symbol-tables"))
import symbol_tables as st

NULL = "null"
"""The artificial type of the null expression, assignable to every class type."""


class TypeError_(Exception):
    """No typing rule applies, so the program has no derivation."""


class Checker:
    """A type checker carrying the four components of the judgement."""

    def __init__(self, classes, current_class, method=None):
        """Fix the class table, the enclosing class and the method being checked."""
        self.classes = classes
        self.current_class = current_class
        self.method = method
        self.variables = st.SymbolTable()

    def declare(self, name, type_name):
        """Add a variable to the environment `V`."""
        return self.variables.declare(name, type_name)

    def assignable(self, source, target):
        """Whether a value of one type may be assigned to a variable of another.

        Reference assignment is allowed upwards: a `B` fits where a `C` is
        expected when `B` is a subclass. The null type fits everywhere, which
        is exactly what the extra rule the sheet grants amounts to.
        """
        if source == target:
            return True
        if source == NULL:
            return target not in ("int", "boolean")
        if source in ("int", "boolean") or target in ("int", "boolean"):
            return False
        return self.classes.is_subtype(source, target)

    def type_of(self, expression):
        """The type of an expression, raising when no rule applies."""
        return self._type_of(expression)["type"]

    def proof(self, statement):
        """The derivation tree for a statement, premises included.

        The statement is checked inside a fresh scope, so the declarations it
        makes disappear afterwards. Without that, checking the same fragment
        twice fails on its own declarations, which is both wrong as Java
        semantics (a block is a scope) and a trap for anything that inspects a
        program more than once.
        """
        self.variables.enter()
        try:
            return self._check(statement)
        finally:
            self.variables.leave()

    def check(self, statement):
        """Whether a statement is type-correct."""
        self.proof(statement)
        return True

    def _type_of(self, expression):
        """One expression, returning a derivation node."""
        kind = expression[0]

        if kind == "num":
            return {"rule": "num", "type": "int", "premises": []}

        if kind == "bool":
            return {"rule": "bool", "type": "boolean", "premises": []}

        if kind == "null":
            return {"rule": "null", "type": NULL, "premises": []}

        if kind == "this":
            return {"rule": "this", "type": self.current_class, "premises": []}

        if kind == "var":
            symbol = self.variables.resolve(expression[1])
            return {"rule": "var", "type": symbol.type, "premises": []}

        if kind == "field":
            target = self._type_of(expression[1])
            field = self.classes.field(target["type"], expression[2])
            if field is None:
                raise TypeError_(f"class {target['type']} has no field {expression[2]}")
            return {"rule": "field", "type": field, "premises": [target]}

        if kind == "cast":
            inner = self._type_of(expression[2])
            if not self._castable(inner["type"], expression[1]):
                raise TypeError_(f"cannot cast {inner['type']} to {expression[1]}")
            return {"rule": "cast", "type": expression[1], "premises": [inner]}

        if kind == "eq":
            left = self._type_of(expression[1])
            right = self._type_of(expression[2])
            if not (self.assignable(left["type"], right["type"])
                    or self.assignable(right["type"], left["type"])):
                raise TypeError_(f"cannot compare {left['type']} with {right['type']}")
            return {"rule": "eq", "type": "boolean", "premises": [left, right]}

        if kind == "call":
            target = self._type_of(expression[1])
            signature = self.classes.method(target["type"], expression[2])
            if signature is None:
                raise TypeError_(f"class {target['type']} has no method {expression[2]}")
            result, parameters = signature
            arguments = [self._type_of(argument) for argument in expression[3]]
            if len(arguments) != len(parameters):
                raise TypeError_(f"method {expression[2]} takes {len(parameters)} argument(s)")
            for argument, expected in zip(arguments, parameters):
                if not self.assignable(argument["type"], expected):
                    raise TypeError_(f"cannot pass {argument['type']} where {expected} is expected")
            return {"rule": "call", "type": result, "premises": [target] + arguments}

        raise TypeError_(f"no typing rule for {kind}")

    def _castable(self, source, target):
        """Whether a cast is statically allowed.

        Upcasts and downcasts along the same chain are; a cast between
        unrelated classes is not, because no object can ever have both types.
        A downcast is allowed **statically** and checked again at run time,
        which is precisely the gap the sheet's second question is about.
        """
        if source == NULL:
            return True
        return (self.classes.is_subtype(source, target)
                or self.classes.is_subtype(target, source))

    def _check(self, statement):
        """One statement, returning a derivation node."""
        kind = statement[0]

        if kind == "seq":
            premises = [self._check(part) for part in statement[1:]]
            return {"rule": "seq", "type": "void", "premises": premises}

        if kind == "declare":
            self.declare(statement[2], statement[1])
            return {"rule": "declare", "type": "void", "premises": []}

        if kind == "assign":
            symbol = self.variables.resolve(statement[1])
            value = self._type_of(statement[2])
            if not self.assignable(value["type"], symbol.type):
                raise TypeError_(f"cannot assign {value['type']} to {symbol.type}")
            return {"rule": "assign", "type": "void", "premises": [value]}

        if kind == "if":
            condition = self._type_of(statement[1])
            if condition["type"] != "boolean":
                raise TypeError_(f"condition has type {condition['type']}, not boolean")
            branches = [self._check(part) for part in statement[2:]]
            return {"rule": "if", "type": "void", "premises": [condition] + branches}

        if kind == "while":
            condition = self._type_of(statement[1])
            if condition["type"] != "boolean":
                raise TypeError_(f"condition has type {condition['type']}, not boolean")
            return {"rule": "while", "type": "void",
                    "premises": [condition, self._check(statement[2])]}

        raise TypeError_(f"no typing rule for statement {kind}")


def rules_used(proof):
    """Every rule name appearing in a derivation."""
    names = {proof["rule"]}
    for premise in proof["premises"]:
        names |= rules_used(premise)
    return names


def render(proof, indent=0):
    """The derivation as indented text, premises above their conclusion."""
    lines = []
    for premise in proof["premises"]:
        lines.extend(render(premise, indent + 1))
    lines.append("  " * indent + f"{proof['rule']} : {proof['type']}")
    return lines


def run_time_outcome(classes, statement, current_class, actual_class):
    """What the fragment does when it runs, given the real class of `this`.

    A static check reasons about the declared type of `this`, which is the
    class the code sits in. At run time `this` has whatever class the object
    was created with, and a downcast succeeds only if that class really is a
    subclass of the target.

    That is the whole content of the sheet's second question: the fragment is
    type-correct and still throws, because `this` is not assignable and is
    therefore definitely a `C`.
    """
    outcome = {"result": "ok"}

    def evaluate(expression, environment):
        """Enough of an interpreter to reach the cast."""
        kind = expression[0]
        if kind == "null":
            return None
        if kind == "this":
            return actual_class
        if kind == "var":
            return environment.get(expression[1])
        if kind == "eq":
            return evaluate(expression[1], environment) == evaluate(expression[2], environment)
        if kind == "cast":
            value = evaluate(expression[2], environment)
            if value is None:
                return None
            if not classes.is_subtype(value, expression[1]):
                outcome["result"] = "ClassCastException"
                raise _Thrown()
            return value
        raise ValueError(f"cannot evaluate {kind}")

    def run(current, environment):
        """Execute a statement, stopping at the first exception."""
        kind = current[0]
        if kind == "seq":
            for part in current[1:]:
                run(part, environment)
        elif kind == "declare":
            environment[current[2]] = None
        elif kind == "assign":
            environment[current[1]] = evaluate(current[2], environment)
        elif kind == "if":
            if evaluate(current[1], environment):
                run(current[2], environment)

    try:
        run(statement, {})
    except _Thrown:
        pass

    return outcome["result"]


class _Thrown(Exception):
    """Internal marker for an exception raised by the interpreted fragment."""
