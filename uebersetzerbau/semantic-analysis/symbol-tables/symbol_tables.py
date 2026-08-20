"""Symbol tables: what a name means at the point it is used.

A grammar can say that an identifier may appear; it cannot say which
declaration it refers to. Resolving that is the symbol table's job, and the
whole difficulty is scope: the same name may denote different things in
different parts of the program, and the rule for which one wins is that the
innermost open declaration does.

The structure follows from that rule directly. A stack of scopes, a lookup that
walks it from the top, and a declaration that only checks the topmost frame for
duplicates. Everything else, inheritance, imports, overloading, is a variation
on where the walk goes next.
"""

from __future__ import annotations


class Symbol:
    """One declaration: a name, its type, and the scope depth it lives at."""

    def __init__(self, name, type_name, depth):
        """Record one declaration and the scope depth it was made at."""
        self.name = name
        self.type = type_name
        self.depth = depth

    def __repr__(self):
        """Short form naming the symbol and its type."""
        return f"{self.name}: {self.type} @{self.depth}"


class RedeclarationError(Exception):
    """The same name was declared twice in one scope."""


class UndeclaredError(Exception):
    """A name was used with no declaration in scope.

    The position is carried because that is the only part of the message a
    programmer can act on: which use, not which name.
    """

    def __init__(self, name, position):
        """Record the name and the position of the offending use."""
        super().__init__(f"undeclared name {name!r}"
                         + (f" at position {position}" if position is not None else ""))
        self.name = name
        self.position = position


class SymbolTable:
    """A stack of scopes, innermost last."""

    def __init__(self):
        """Start with a single outermost scope."""
        self.scopes = [{}]

    def enter(self):
        """Open a nested scope."""
        self.scopes.append({})

    def leave(self):
        """Close the innermost scope, discarding its declarations.

        Discarding rather than keeping is what makes shadowing work and what
        makes a compiler's memory use independent of how many blocks a program
        has. A compiler that needs the information later, for a debugger or an
        IDE, keeps the scopes in a tree instead and pays for it.
        """
        if len(self.scopes) == 1:
            raise IndexError("cannot leave the outermost scope")
        return self.scopes.pop()

    def declare(self, name, type_name):
        """Add a declaration to the innermost scope."""
        if name in self.scopes[-1]:
            raise RedeclarationError(f"{name!r} is already declared in this scope")
        symbol = Symbol(name, type_name, len(self.scopes) - 1)
        self.scopes[-1][name] = symbol
        return symbol

    def lookup(self, name):
        """The innermost declaration of a name, or `None`."""
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def resolve(self, name, position=None):
        """The innermost declaration, raising if there is none."""
        symbol = self.lookup(name)
        if symbol is None:
            raise UndeclaredError(name, position)
        return symbol

    def depth_of(self, name):
        """The scope depth the visible declaration of a name lives at."""
        symbol = self.lookup(name)
        return None if symbol is None else symbol.depth

    def visible(self):
        """Every name currently visible, innermost declarations winning."""
        result = {}
        for scope in self.scopes:
            result.update(scope)
        return result

    def depth(self):
        """Current nesting depth, with the outermost scope at zero."""
        return len(self.scopes) - 1


class HierarchyError(Exception):
    """The class hierarchy would contain a cycle."""


class ClassTable:
    """Classes with single inheritance, their fields and their methods.

    A second kind of scope, and a different walk: a name not found in a class
    is looked for in its superclass rather than in an enclosing block. The
    subtype relation is the reflexive transitive closure of that same chain,
    which is why both live in one structure.
    """

    def __init__(self):
        """Start with no classes declared."""
        self.classes = {}

    def add(self, name, parent, fields, methods):
        """Declare a class, rejecting an inheritance cycle."""
        if parent is not None and self._reaches(parent, name):
            raise HierarchyError(f"{name} and {parent} would form a cycle")
        self.classes[name] = {"parent": parent, "fields": dict(fields),
                              "methods": dict(methods)}

    def _reaches(self, start, target):
        """Whether the superclass chain from one class reaches another."""
        current = start
        seen = set()
        while current is not None and current not in seen:
            if current == target:
                return True
            seen.add(current)
            current = self.classes.get(current, {}).get("parent")
        return False

    def field(self, class_name, field_name):
        """The type of a field, searching up the superclass chain."""
        current = class_name
        while current is not None:
            entry = self.classes.get(current)
            if entry is None:
                return None
            if field_name in entry["fields"]:
                return entry["fields"][field_name]
            current = entry["parent"]
        return None

    def method(self, class_name, method_name):
        """The signature of a method, searching up the superclass chain."""
        current = class_name
        while current is not None:
            entry = self.classes.get(current)
            if entry is None:
                return None
            if method_name in entry["methods"]:
                return entry["methods"][method_name]
            current = entry["parent"]
        return None

    def is_subtype(self, first, second):
        """Whether the first class is the second or inherits from it.

        Reflexive, so a class is its own subtype, which is what makes
        assignment of a value to a variable of its own type a special case of
        assignment compatibility rather than a separate rule.
        """
        return self._reaches(first, second)

    def ancestors(self, class_name):
        """The superclass chain, starting with the class itself."""
        chain = []
        current = class_name
        while current is not None and current not in chain:
            chain.append(current)
            current = self.classes.get(current, {}).get("parent")
        return chain
