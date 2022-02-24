"""Two operations at once, and what the second one costs.

A ring is an abelian group under addition and a monoid under multiplication,
with distribution tying them together. Dropping commutativity of
multiplication keeps matrices in; requiring inverses for everything but zero
takes the residues modulo a composite number out. The residues are the
running example because the modulus decides which of those conditions hold.
"""

import itertools


class Ring:
    """A finite set with an addition and a multiplication."""

    def __init__(self, elements, add, multiply, name=""):
        """A ring given by its elements and its two operations."""
        self.elements = list(elements)
        self.add = add
        self.multiply = multiply
        self.name = name

    def zero(self):
        """The neutral element of the addition."""
        for candidate in self.elements:
            if all(self.add(candidate, other) == other for other in self.elements):
                return candidate
        return None

    def one(self):
        """The neutral element of the multiplication, if there is one."""
        for candidate in self.elements:
            if all(self.multiply(candidate, other) == other
                   and self.multiply(other, candidate) == other
                   for other in self.elements):
                return candidate
        return None

    def negative(self, element):
        """The additive inverse."""
        zero = self.zero()
        for candidate in self.elements:
            if self.add(element, candidate) == zero:
                return candidate
        return None

    def check_laws(self):
        """Which of the ring laws hold, checked over every triple."""
        report = {"addition closed": True, "addition associative": True,
                  "addition commutative": True, "zero": self.zero() is not None,
                  "negatives": True, "multiplication closed": True,
                  "multiplication associative": True, "distributive": True}
        for left in self.elements:
            if self.negative(left) is None:
                report["negatives"] = False
            for right in self.elements:
                if self.add(left, right) not in self.elements:
                    report["addition closed"] = False
                if self.multiply(left, right) not in self.elements:
                    report["multiplication closed"] = False
                if self.add(left, right) != self.add(right, left):
                    report["addition commutative"] = False
                for third in self.elements:
                    if self.add(self.add(left, right), third) != \
                            self.add(left, self.add(right, third)):
                        report["addition associative"] = False
                    if self.multiply(self.multiply(left, right), third) != \
                            self.multiply(left, self.multiply(right, third)):
                        report["multiplication associative"] = False
                    if self.multiply(left, self.add(right, third)) != \
                            self.add(self.multiply(left, right),
                                     self.multiply(left, third)):
                        report["distributive"] = False
        return report

    def is_ring(self):
        """Whether every law holds."""
        return all(self.check_laws().values())

    def is_commutative(self):
        """Whether the multiplication commutes."""
        return all(self.multiply(left, right) == self.multiply(right, left)
                   for left in self.elements for right in self.elements)

    def units(self):
        """The elements with a multiplicative inverse."""
        one = self.one()
        if one is None:
            return []
        return [element for element in self.elements
                if any(self.multiply(element, other) == one
                       for other in self.elements)]

    def zero_divisors(self):
        """The non-zero elements whose product with another non-zero is zero."""
        zero = self.zero()
        found = []
        for element in self.elements:
            if element == zero:
                continue
            if any(other != zero and self.multiply(element, other) == zero
                   for other in self.elements):
                found.append(element)
        return found


def modular(modulus):
    """The residues modulo a number, with the usual operations."""
    return Ring(list(range(modulus)),
                lambda a, b: (a + b) % modulus,
                lambda a, b: (a * b) % modulus,
                "Z/%d" % modulus)


def polynomials(modulus, degree):
    """Polynomials over the residues, truncated at the given degree.

    Represented as tuples of coefficients, lowest first. Truncation keeps the
    carrier finite so the laws can be checked by enumeration, and it is the
    reason the degree stays small here.
    """
    elements = [tuple(values) for values in
                itertools.product(range(modulus), repeat=degree)]

    def add(left, right):
        """Coefficientwise addition."""
        return tuple((a + b) % modulus for a, b in zip(left, right))

    def multiply(left, right):
        """The product, with everything above the degree dropped."""
        result = [0] * degree
        for index, first in enumerate(left):
            for offset, second in enumerate(right):
                if index + offset < degree:
                    result[index + offset] = (result[index + offset]
                                              + first * second) % modulus
        return tuple(result)

    return Ring(elements, add, multiply, "F%d[x]/x^%d" % (modulus, degree))
