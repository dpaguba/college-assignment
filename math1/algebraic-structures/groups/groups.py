"""Finite groups, built from an operation and checked against the axioms.

A group is a monoid in which every element has an inverse, and that one extra
condition is what makes the whole theory work: it gives cancellation, it makes
every row of the table a permutation, and it forces the order of an element to
divide the order of the group.

The groups here are constructed rather than searched for. Of the five groups
of order eight, three are abelian and two are not, and the classification
function separates them by testing every bijection for being a homomorphism.
"""

import itertools


class Group:
    """A finite set with an operation, an identity and inverses."""

    def __init__(self, elements, operation, name=""):
        """A group given by its elements and an operation on them."""
        self.elements = list(elements)
        self.operation = operation
        self.name = name

    def apply(self, left, right):
        """The product of two elements."""
        return self.operation(left, right)

    def is_closed(self):
        """Whether products stay inside the set."""
        return all(self.apply(left, right) in self.elements
                   for left in self.elements for right in self.elements)

    def is_associative(self):
        """Whether the bracketing never matters."""
        for left in self.elements:
            for middle in self.elements:
                for right in self.elements:
                    if self.apply(self.apply(left, middle), right) != \
                            self.apply(left, self.apply(middle, right)):
                        return False
        return True

    def identity(self):
        """The neutral element, or nothing."""
        for candidate in self.elements:
            if all(self.apply(candidate, other) == other
                   and self.apply(other, candidate) == other
                   for other in self.elements):
                return candidate
        return None

    def inverse(self, element):
        """The inverse of an element, or nothing."""
        unit = self.identity()
        for candidate in self.elements:
            if self.apply(element, candidate) == unit \
                    and self.apply(candidate, element) == unit:
                return candidate
        return None

    def is_group(self):
        """Whether all four axioms hold."""
        if not self.is_closed() or not self.is_associative():
            return False
        if self.identity() is None:
            return False
        return all(self.inverse(element) is not None for element in self.elements)

    def is_abelian(self):
        """Whether the operation commutes."""
        return all(self.apply(left, right) == self.apply(right, left)
                   for left in self.elements for right in self.elements)

    def order_of(self, element):
        """How often an element must be applied to itself to reach the identity."""
        unit = self.identity()
        current = element
        order = 1
        while current != unit:
            current = self.apply(current, element)
            order += 1
            if order > len(self.elements):
                raise ValueError("the element has no finite order")
        return order

    def generated_by(self, element):
        """The subgroup a single element generates."""
        unit = self.identity()
        found = [unit]
        current = element
        while current != unit:
            found.append(current)
            current = self.apply(current, element)
        return found

    def is_cyclic(self):
        """Whether some element generates the whole group."""
        return any(len(self.generated_by(element)) == len(self.elements)
                   for element in self.elements)

    def table(self):
        """The Cayley table as a dictionary."""
        return {(left, right): self.apply(left, right)
                for left in self.elements for right in self.elements}


def cyclic(order):
    """Addition modulo the order."""
    return Group(list(range(order)), lambda a, b: (a + b) % order,
                 "Z%d" % order)


def units(modulus):
    """The invertible residues under multiplication."""
    def coprime(value):
        """Whether the value shares no factor with the modulus."""
        first, second = value, modulus
        while second:
            first, second = second, first % second
        return first == 1

    elements = [value for value in range(modulus) if coprime(value)]
    return Group(elements, lambda a, b: (a * b) % modulus, "U%d" % modulus)


def symmetric(degree):
    """The permutations of the given number of points, written as tuples."""
    elements = list(itertools.permutations(range(degree)))
    return Group(elements,
                 lambda a, b: tuple(a[b[index]] for index in range(degree)),
                 "S%d" % degree)


def dihedral(sides):
    """The symmetries of a regular polygon, as pairs of a rotation and a flip."""
    elements = [(rotation, flip) for rotation in range(sides) for flip in (0, 1)]

    def compose(left, right):
        """The composition of two symmetries."""
        rotation, flip = left
        other_rotation, other_flip = right
        if flip == 0:
            return ((rotation + other_rotation) % sides, other_flip)
        return ((rotation - other_rotation) % sides, (1 + other_flip) % 2)

    return Group(elements, compose, "D%d" % sides)


def klein_four():
    """The product of two copies of the two-element group."""
    return direct_product(cyclic(2), cyclic(2))


def quaternion():
    """The quaternion group of order eight."""
    elements = ["1", "-1", "i", "-i", "j", "-j", "k", "-k"]
    products = {("i", "j"): "k", ("j", "k"): "i", ("k", "i"): "j",
                ("j", "i"): "-k", ("k", "j"): "-i", ("i", "k"): "-j",
                ("i", "i"): "-1", ("j", "j"): "-1", ("k", "k"): "-1"}

    def sign_and_letter(value):
        """The sign and the letter of an element."""
        return (-1 if value.startswith("-") else 1, value.lstrip("-"))

    def compose(left, right):
        """The product in the quaternion group."""
        left_sign, left_letter = sign_and_letter(left)
        right_sign, right_letter = sign_and_letter(right)
        sign = left_sign * right_sign
        if left_letter == "1":
            letter, extra = right_letter, 1
        elif right_letter == "1":
            letter, extra = left_letter, 1
        else:
            product = products[(left_letter, right_letter)]
            extra_sign, letter = sign_and_letter(product)
            extra = extra_sign
        sign *= extra
        return ("-" if sign < 0 else "") + letter

    return Group(elements, compose, "Q8")


def direct_product(first, second):
    """The product group, with the operation applied in each component."""
    elements = [(left, right) for left in first.elements
                for right in second.elements]
    return Group(elements,
                 lambda a, b: (first.apply(a[0], b[0]), second.apply(a[1], b[1])),
                 "%s x %s" % (first.name, second.name))


def isomorphism(first, second):
    """A bijection preserving the operation, or nothing.

    Searched over every bijection, which is why the groups here stay small.
    The search is what makes the classification a result rather than a claim:
    two groups are declared different only after every candidate has failed.
    """
    if len(first.elements) != len(second.elements):
        return None
    for values in itertools.permutations(second.elements):
        mapping = dict(zip(first.elements, values))
        if all(mapping[first.apply(left, right)]
               == second.apply(mapping[left], mapping[right])
               for left in first.elements for right in first.elements):
            return mapping
    return None


def classify(candidates):
    """The candidates grouped into isomorphism classes."""
    classes = []
    for group in candidates:
        for existing in classes:
            if isomorphism(group, existing[0]) is not None:
                existing.append(group)
                break
        else:
            classes.append([group])
    return classes
