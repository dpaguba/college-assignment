"""Pattern matching, and the exhaustiveness question it makes decidable.

A pattern names a constructor and binds its arguments, so matching is a
comparison of the constructor and then a binding of names. Because a data
type lists its constructors, a compiler can tell whether a set of equations
covers them all, which is the property that makes a missing case a warning
rather than a run time surprise.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "algebraic-data-types"))
import algebraic_data_types as adt


class MatchError(Exception):
    """Raised when no equation applies to a value."""


def match(pattern, value):
    """The bindings a pattern produces, or nothing when it does not apply."""
    if pattern[0] == "_":
        return {}
    if pattern[0] != adt.name_of(value):
        return None
    arguments = adt.arguments_of(value)
    if len(pattern) - 1 != len(arguments):
        return None
    bindings = {}
    for name, argument in zip(pattern[1:], arguments):
        if name == "_":
            continue
        bindings[name] = argument
    return bindings


def run(equations, value):
    """The result of the first equation that matches.

    The order matters, which is why a catch-all equation written first makes
    everything after it unreachable, and why the module reports a missing
    case instead of returning a default.
    """
    for pattern, body in equations:
        bindings = match(pattern, value)
        if bindings is not None:
            return body(bindings)
    raise MatchError("no equation for %s" % adt.name_of(value))


def is_exhaustive(type_name, patterns):
    """Whether the patterns cover every constructor of the type."""
    if any(pattern[0] == "_" for pattern in patterns):
        return True
    covered = {pattern[0] for pattern in patterns}
    return set(adt.constructors(type_name)) <= covered


def missing_cases(type_name, patterns):
    """The constructors the patterns leave out."""
    if is_exhaustive(type_name, patterns):
        return []
    covered = {pattern[0] for pattern in patterns}
    return [name for name in adt.constructors(type_name) if name not in covered]
