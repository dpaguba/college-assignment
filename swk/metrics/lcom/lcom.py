"""Lack of cohesion in methods: how loosely a class holds together.

The lecture's definition, for a class with ``a`` fields and ``m`` methods,
where ``n(Ai)`` is the number of methods touching field ``Ai``:

    LCOM = ((1/a) * sum of n(Ai) - m) / (1 - m)

The value runs from 0 to 1. Zero means every method uses every field, which is
as cohesive as a class can be. One means each field is touched by a single
method, which is a class that is really several classes sharing a name.

The measure is an estimate: it infers "belongs together" from "touches the
same data", which is a proxy and not the thing itself.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class ClassModel:
    """A class reduced to what the metric needs: fields, methods, and accesses."""

    name: str
    fields: tuple
    accesses: dict

    @property
    def methods(self):
        """Every method name, in a stable order."""
        return tuple(sorted(self.accesses))

    def accessing(self, field):
        """The methods that touch a given field."""
        return {method for method, touched in self.accesses.items() if field in touched}

    def access_counts(self):
        """``n(Ai)`` for every field: how many methods touch it."""
        return {field: len(self.accessing(field)) for field in self.fields}


def lcom(model):
    """The lecture's normalised LCOM, as an exact fraction.

    Returns a Fraction so that the exercise's answer comes out as 2/3 rather
    than 0.6666666666666666. The denominator ``1 - m`` is negative for any
    class with more than one method, which is what turns the formula into a
    value in [0, 1] rather than something unbounded.

    Undefined for a class with one method or no fields, where the formula
    divides by zero; those return None rather than raising, since a class that
    small has no cohesion question to answer.
    """
    field_count = len(model.fields)
    method_count = len(model.accesses)

    if method_count <= 1 or field_count == 0:
        return None

    total = sum(model.access_counts().values())
    return (Fraction(total, field_count) - method_count) / (1 - method_count)


def lcom1(model):
    """Chidamber and Kemerer's original: pairs of methods sharing no field.

    Counts the method pairs with disjoint field sets. Unbounded, so it grows
    with the size of the class and cannot be compared between classes of
    different sizes, which is exactly the flaw the normalised version fixes.
    """
    methods = model.methods
    disjoint = 0

    for index, first in enumerate(methods):
        for second in methods[index + 1:]:
            if not (set(model.accesses[first]) & set(model.accesses[second])):
                disjoint += 1

    return disjoint


def lcom2(model):
    """Disjoint pairs minus sharing pairs, floored at zero.

    The second Chidamber and Kemerer variant. It reads as "how much more
    disagreement than agreement there is", and it collapses to zero for any
    reasonably connected class, which makes it a poor discriminator.
    """
    methods = model.methods
    disjoint = sharing = 0

    for index, first in enumerate(methods):
        for second in methods[index + 1:]:
            if set(model.accesses[first]) & set(model.accesses[second]):
                sharing += 1
            else:
                disjoint += 1

    return max(0, disjoint - sharing)


def lcom4(model):
    """Connected components of the method graph, which is the version worth using.

    Two methods are joined when they share a field or one calls the other. The
    number of components is the number of independent responsibilities in the
    class, so LCOM4 = 1 means one cohesive class and LCOM4 = 3 means three
    classes waiting to be split out.

    Unlike the others this one is directly actionable: the components name the
    classes to extract.
    """
    methods = list(model.methods)
    parent = {method: method for method in methods}

    def find(method):
        """The representative of a method's component."""
        while parent[method] != method:
            parent[method] = parent[parent[method]]
            method = parent[method]
        return method

    def union(first, second):
        """Joins the components of two methods that share a field."""
        parent[find(first)] = find(second)

    for index, first in enumerate(methods):
        for second in methods[index + 1:]:
            if set(model.accesses[first]) & set(model.accesses[second]):
                union(first, second)

    return len({find(method) for method in methods}) if methods else 0


def components(model):
    """The groups of methods LCOM4 counts, which are the classes to extract."""
    methods = list(model.methods)
    parent = {method: method for method in methods}

    def find(method):
        """The representative of a method's component."""
        while parent[method] != method:
            parent[method] = parent[parent[method]]
            method = parent[method]
        return method

    for index, first in enumerate(methods):
        for second in methods[index + 1:]:
            if set(model.accesses[first]) & set(model.accesses[second]):
                parent[find(first)] = find(second)

    groups = {}
    for method in methods:
        groups.setdefault(find(method), []).append(method)
    return sorted(sorted(group) for group in groups.values())


def report(model):
    """All four measures for one class, with the field access counts."""
    value = lcom(model)
    return {
        "class": model.name,
        "fields": len(model.fields),
        "methods": len(model.accesses),
        "n(Ai)": model.access_counts(),
        "LCOM": value,
        "LCOM as float": float(value) if value is not None else None,
        "LCOM1": lcom1(model),
        "LCOM2": lcom2(model),
        "LCOM4": lcom4(model),
        "components": components(model),
    }


EXERCISE = ClassModel(
    name="exercise 2.3",
    fields=("A1", "A2", "A3"),
    accesses={"m1": {"A1", "A2"}, "m2": {"A2"}, "m3": {"A2", "A3"}, "m4": {"A3"}},
)
"""The class from exercise sheet 2, whose published answer is LCOM = 2/3."""

TRIANGLE = ClassModel(
    name="Dreieck",
    fields=("a", "b", "c"),
    accesses={f"m{index}": {"a", "b", "c"} for index in range(1, 5)},
)
"""The lecture's cohesive class: every method uses every field, so LCOM = 0."""

MERGED = ClassModel(
    name="Figur",
    fields=("a", "b", "c", "r"),
    accesses={**{f"t{index}": {"a", "b", "c"} for index in range(1, 5)},
              **{f"k{index}": {"r"} for index in range(1, 5)}},
)
"""Triangle and circle merged into one class, which the lecture scores at 4/7."""
