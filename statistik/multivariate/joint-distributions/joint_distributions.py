"""Joint distributions, margins, and what the margins forget.

A joint distribution assigns a probability to each pair. Summing over one
variable gives the marginal distribution of the other, and the margins alone
do not determine the joint distribution: the product of the margins is one
distribution with those margins, and there are others.
"""


def margins(joint):
    """The two marginal distributions."""
    first, second = {}, {}
    for (left, right), weight in joint.items():
        first[left] = first.get(left, 0.0) + weight
        second[right] = second.get(right, 0.0) + weight
    return first, second


def product_of_margins(joint):
    """The distribution in which the two variables are independent."""
    first, second = margins(joint)
    return {(left, right): first[left] * second[right]
            for left in first for right in second}


def is_independent(joint, tolerance=1e-9):
    """Whether the joint distribution is the product of its margins."""
    product = product_of_margins(joint)
    keys = set(joint) | set(product)
    return all(abs(joint.get(key, 0.0) - product.get(key, 0.0)) < tolerance
               for key in keys)


def conditional(joint, first=None, second=None):
    """The distribution of one variable given a value of the other."""
    if (first is None) == (second is None):
        raise ValueError("condition on exactly one of the two variables")
    if first is not None:
        weight = sum(value for (left, _), value in joint.items() if left == first)
        if weight == 0:
            raise ValueError("that value has probability zero")
        return {right: value / weight for (left, right), value in joint.items()
                if left == first}
    weight = sum(value for (_, right), value in joint.items() if right == second)
    if weight == 0:
        raise ValueError("that value has probability zero")
    return {left: value / weight for (left, right), value in joint.items()
            if right == second}
