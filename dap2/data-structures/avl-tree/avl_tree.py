"""AVL tree: a binary search tree that rebalances itself after every change."""

from __future__ import annotations


class Node:
    """One node: a key, its value, both children, and the cached subtree height."""
    __slots__ = ("key", "value", "left", "right", "height")

    def __init__(self, key, value):
        """An empty tree."""
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


def height(node):
    """Height of a subtree, with 0 for an absent one, read from the cached field."""
    return 0 if node is None else node.height


def balance(node):
    """Left height minus right height. AVL keeps this within [-1, 1]."""
    return 0 if node is None else height(node.left) - height(node.right)


class AVLTree:
    """A search tree with a guaranteed logarithmic height.

    Adelson-Velsky and Landis, 1962, the first self-balancing tree. The
    invariant is deliberately strict: at every node the two subtree heights
    differ by at most one. That forces the height to stay within about
    1.44·log₂(n), so search, insert and delete are O(log n) on every input,
    including the sorted one that turns a plain BST into a list.

    Restoring the invariant needs only rotations, local rearrangements that
    move one node up and another down while preserving the ordering. There are
    four cases, and they are really two: left-left and right-right need one
    rotation, left-right and right-left need two, because the inner subtree has
    to be straightened before it can be lifted.

    The strictness cuts both ways. AVL trees are shallower than red-black
    trees, so lookups are faster, and they rebalance more often, so writes are
    slower. Read-heavy workloads take AVL; write-heavy ones take red-black,
    which is why the C++ and Java standard libraries chose the latter.
    """

    def __init__(self):
        """An empty tree."""
        self._root = None
        self._count = 0

    @staticmethod
    def _update(node):
        """Recomputes the stored height of a node."""
        node.height = 1 + max(height(node.left), height(node.right))

    def _rotate_right(self, node):
        """The right rotation, which lifts the left child."""
        pivot = node.left
        node.left = pivot.right
        pivot.right = node
        self._update(node)
        self._update(pivot)
        return pivot

    def _rotate_left(self, node):
        """The left rotation, which lifts the right child."""
        pivot = node.right
        node.right = pivot.left
        pivot.left = node
        self._update(node)
        self._update(pivot)
        return pivot

    def _rebalance(self, node):
        """Restores the balance condition with one or two rotations."""
        self._update(node)
        factor = balance(node)

        if factor > 1:
            if balance(node.left) < 0:
                node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if factor < -1:
            if balance(node.right) > 0:
                node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def insert(self, key, value=None):
        """Store a value under a key, rebalancing on the way back up. O(log n)."""
        def place(node):
            """Inserts below the node and rebalances on the way back."""
            if node is None:
                self._count += 1
                return Node(key, value)
            if key == node.key:
                node.value = value
                return node
            if key < node.key:
                node.left = place(node.left)
            else:
                node.right = place(node.right)
            return self._rebalance(node)

        self._root = place(self._root)

    def delete(self, key):
        """Remove a key, rebalancing on the way back up.

        O(log n). Deletion can need rotations at every level on the path, where
        insertion needs at most two.
        """
        removed = False

        def remove(node, key):
            """Deletes below the node and rebalances on the way back."""
            nonlocal removed
            if node is None:
                return None
            if key < node.key:
                node.left = remove(node.left, key)
            elif key > node.key:
                node.right = remove(node.right, key)
            else:
                removed = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key, node.value = successor.key, successor.value
                node.right = remove(node.right, successor.key)
            return self._rebalance(node)

        self._root = remove(self._root, key)
        if removed:
            self._count -= 1
        return removed

    def _find(self, key):
        """The node holding the key, or nothing when it is absent."""
        node = self._root
        while node is not None and node.key != key:
            node = node.left if key < node.key else node.right
        return node

    def search(self, key):
        """Value stored under the key, or None.

        O(log n), guaranteed by the balance invariant.
        """
        node = self._find(key)
        return None if node is None else node.value

    def items(self):
        """Every pair in ascending key order, by in-order walk."""
        stack, node = [], self._root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key, node.value
            node = node.right

    def keys(self):
        """Every key in ascending order."""
        for key, _ in self.items():
            yield key

    def height(self):
        """Height of the whole tree, at most about 1.44 log n by the AVL invariant..
        """
        return height(self._root)

    def is_balanced(self):
        """Every node's subtrees differ in height by at most one."""

        def check(node):
            """Whether every node below this one is balanced."""
            if node is None:
                return True
            return abs(balance(node)) <= 1 and check(node.left) and check(node.right)

        return check(self._root)

    def __contains__(self, key):
        """Whether the key is stored."""
        return self._find(key) is not None

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
