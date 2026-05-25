"""The exam's binary tree, its traversals, and its functor instance.

```haskell
data Baum a = Leer | Knoten a (Baum a) (Baum a)
```

Two constructors, so every function over the type is two equations, and the
recursion follows the shape of the data. The height counts the constructors
on the longest path with the empty tree at zero, which is the definition the
exam gives, and the three traversals differ only in where the root is
emitted.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..",
                                "haskell-core", "algebraic-data-types"))
import algebraic_data_types as adt

LEER = adt.construct("Leer")
"""The empty tree."""


def node(value, left, right):
    """An inner node with a value and two subtrees."""
    return adt.construct("Knoten", value, left, right)


def hoehe(tree):
    """The height: the number of nodes on the longest path from the root."""
    if adt.name_of(tree) == "Leer":
        return 0
    _, left, right = adt.arguments_of(tree)
    return 1 + max(hoehe(left), hoehe(right))


def preorder(tree):
    """The values with the root first, then the left and right subtrees."""
    if adt.name_of(tree) == "Leer":
        return []
    value, left, right = adt.arguments_of(tree)
    return [value] + preorder(left) + preorder(right)


def inorder(tree):
    """The values with the root between the two subtrees."""
    if adt.name_of(tree) == "Leer":
        return []
    value, left, right = adt.arguments_of(tree)
    return inorder(left) + [value] + inorder(right)


def postorder(tree):
    """The values with the root last."""
    if adt.name_of(tree) == "Leer":
        return []
    value, left, right = adt.arguments_of(tree)
    return postorder(left) + postorder(right) + [value]


def fmap(function, tree):
    """The functor instance the exam asks for.

    Applying the function to the values and leaving the shape alone is the
    only definition that satisfies the functor laws, which is why the
    instance is said to be forced by the type.
    """
    if adt.name_of(tree) == "Leer":
        return LEER
    value, left, right = adt.arguments_of(tree)
    return node(function(value), fmap(function, left), fmap(function, right))


def fold(empty, combine, tree):
    """The fold of the type: one value per constructor."""
    if adt.name_of(tree) == "Leer":
        return empty
    value, left, right = adt.arguments_of(tree)
    return combine(value, fold(empty, combine, left),
                   fold(empty, combine, right))


def count_nodes(tree):
    """How many inner nodes the tree has."""
    return fold(0, lambda value, left, right: 1 + left + right, tree)


def count_leaves(tree):
    """How many empty subtrees it has, which is one more than the nodes."""
    return fold(1, lambda value, left, right: left + right, tree)
