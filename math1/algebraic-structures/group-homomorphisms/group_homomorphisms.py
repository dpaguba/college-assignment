"""Homomorphisms, kernels, and the theorem that ties them together.

A homomorphism loses information, and the kernel says exactly how much: two
elements have the same image precisely when they differ by an element of the
kernel. The homomorphism theorem turns that into an isomorphism between the
quotient by the kernel and the image, and it is checked here by searching for
that isomorphism explicitly rather than by citing the proof.
"""

import itertools
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "groups"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "quotient-groups"))
import groups
import quotient_groups


def is_homomorphism(source, target, mapping):
    """Whether the map turns products into products."""
    for left in source.elements:
        for right in source.elements:
            if mapping[source.apply(left, right)] != target.apply(mapping[left],
                                                                 mapping[right]):
                return False
    return True


def kernel(source, target, mapping):
    """The elements sent to the identity, which form a normal subgroup."""
    unit = target.identity()
    elements = [element for element in source.elements if mapping[element] == unit]
    return groups.Group(elements, source.operation, "ker")


def image(source, target, mapping):
    """The elements that are hit, which form a subgroup of the target."""
    elements = []
    for element in source.elements:
        if mapping[element] not in elements:
            elements.append(mapping[element])
    return groups.Group(elements, target.operation, "im")


def all_homomorphisms(source, target):
    """Every homomorphism between the two groups."""
    found = []
    for values in itertools.product(target.elements, repeat=len(source.elements)):
        mapping = dict(zip(source.elements, values))
        if is_homomorphism(source, target, mapping):
            found.append(mapping)
    return found


def homomorphism_theorem(source, target, mapping):
    """Whether the quotient by the kernel is isomorphic to the image."""
    if not is_homomorphism(source, target, mapping):
        return False
    kernel_group = kernel(source, target, mapping)
    quotient = quotient_groups.quotient(source, kernel_group)
    return groups.isomorphism(quotient, image(source, target, mapping)) is not None
