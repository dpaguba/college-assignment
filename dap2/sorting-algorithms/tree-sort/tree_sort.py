"""Tree sort: insert everything into a binary search tree, then read it out."""

from __future__ import annotations


class Node:
    """One node, holding every value that shares its key in arrival order."""

    __slots__ = ("key", "values", "left", "right")

    def __init__(self, key, value):
        """A node holding one key and the values stored under it."""
        self.key = key
        self.values = [value]
        self.left = None
        self.right = None


def tree_sort(items, key=None):
    """Return a sorted copy of `items`.

    An in-order walk of a binary search tree visits keys in ascending order, so
    sorting is just building the tree and then walking it. Equal keys are kept
    in one node in arrival order, which is what makes this implementation
    stable.

    Unbalanced input is the catch: feeding it an already sorted list builds a
    tree that is one long chain, and the sort degrades to n². An AVL or
    red-black tree fixes that and turns this into a guaranteed n log n sort.
    """
    of = key or (lambda item: item)
    root = None

    for value in items:
        node_key = of(value)
        if root is None:
            root = Node(node_key, value)
            continue
        node = root
        while True:
            if node_key == node.key:
                node.values.append(value)
                break
            side = "left" if node_key < node.key else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(node_key, value))
                break
            node = child

    ordered = []
    stack, node = [], root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        ordered.extend(node.values)
        node = node.right

    return ordered
