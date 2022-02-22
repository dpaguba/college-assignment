"""Fields, and the two ways a ring can fail to be one.

A field is a commutative ring in which every non-zero element is invertible.
The residues modulo n are a field exactly when n is prime, and the reason is
visible in the failure: a composite modulus has zero divisors, and a zero
divisor can never be invertible.

The four-element field is the case that shows what "exactly when n is prime"
does not say. Fields of size four exist, and none of them is the residues
modulo four; the right construction is polynomials over the two-element field
modulo an irreducible quadratic.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rings"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "groups"))
import groups
import rings


def is_prime(value):
    """Whether the number has no divisor besides one and itself."""
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def is_integral_domain(ring):
    """A commutative ring with a one and no zero divisors."""
    return (ring.is_ring() and ring.is_commutative() and ring.one() is not None
            and not ring.zero_divisors())


def is_field(ring):
    """An integral domain in which every non-zero element is invertible."""
    if not is_integral_domain(ring):
        return False
    zero = ring.zero()
    units = set(map(str, ring.units()))
    return all(str(element) in units for element in ring.elements
               if element != zero)


def characteristic(ring):
    """How often the one has to be added to itself to reach zero."""
    one, zero = ring.one(), ring.zero()
    if one is None:
        return 0
    current = one
    count = 1
    while current != zero:
        current = ring.add(current, one)
        count += 1
        if count > len(ring.elements) + 1:
            return 0
    return count


def integers_are_a_domain_but_not_a_field():
    """Whether the integers show that the two notions differ.

    Checked on a range rather than asserted: the products of non-zero
    integers are non-zero, so there are no zero divisors, and two has no
    integer inverse, so it is not a field.
    """
    for left in range(-20, 21):
        for right in range(-20, 21):
            if left and right and left * right == 0:
                return False
    return not any(2 * candidate == 1 for candidate in range(-20, 21))


def gf4():
    """The field with four elements, as polynomials modulo x squared plus x plus one."""
    elements = [(0, 0), (1, 0), (0, 1), (1, 1)]

    def add(left, right):
        """Coefficientwise addition modulo two."""
        return ((left[0] + right[0]) % 2, (left[1] + right[1]) % 2)

    def multiply(left, right):
        """The product, reduced modulo the irreducible polynomial."""
        constant = left[0] * right[0]
        linear = left[0] * right[1] + left[1] * right[0]
        square = left[1] * right[1]
        constant += square
        linear += square
        return (constant % 2, linear % 2)

    return rings.Ring(elements, add, multiply, "GF(4)")


def multiplicative_group_is_cyclic(ring):
    """Whether the non-zero elements form a cyclic group under multiplication."""
    if not is_field(ring):
        return False
    zero = ring.zero()
    elements = [element for element in ring.elements if element != zero]
    group = groups.Group(elements, ring.multiply)
    return group.is_cyclic()
