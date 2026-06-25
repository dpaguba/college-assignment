"""Unification, the engine underneath type inference.

Two types are unified by making them equal with the least commitment
possible, which is what "most general" means: any other solution is an
instance of the one returned. The occurs check is what stops a variable from
being bound to a type containing itself, and dropping it is how a type
checker ends up looping on self application.
"""


def unify(first, second, substitution=None):
    """The most general unifier of two types, or nothing when they clash."""
    substitution = dict(substitution or {})
    left = apply(substitution, first)
    right = apply(substitution, second)
    if left == right:
        return substitution
    if _is_variable(left):
        if occurs(left[1], right):
            return None
        substitution[left[1]] = right
        return substitution
    if _is_variable(right):
        return unify(right, left, substitution)
    if isinstance(left, str) or isinstance(right, str):
        return None
    if left[0] != right[0] or len(left) != len(right):
        return None
    for position in range(1, len(left)):
        substitution = unify(left[position], right[position], substitution)
        if substitution is None:
            return None
    return substitution


def _is_variable(kind):
    """Whether the type is a variable."""
    return isinstance(kind, tuple) and kind and kind[0] == "var"


def apply(substitution, kind):
    """The type with every bound variable replaced."""
    if _is_variable(kind):
        if kind[1] in substitution:
            return apply(substitution, substitution[kind[1]])
        return kind
    if isinstance(kind, str):
        return kind
    return (kind[0],) + tuple(apply(substitution, part) for part in kind[1:])


def occurs(name, kind):
    """Whether a variable occurs in a type.

    Without this check, unifying ``a`` with ``a -> int`` succeeds and builds
    an infinite type, which is the classic way a type checker stops
    terminating.
    """
    if _is_variable(kind):
        return kind[1] == name
    if isinstance(kind, str):
        return False
    return any(occurs(name, part) for part in kind[1:])


def variables(kind):
    """Every type variable occurring in a type."""
    if _is_variable(kind):
        return {kind[1]}
    if isinstance(kind, str):
        return set()
    found = set()
    for part in kind[1:]:
        found |= variables(part)
    return found
