"""Red-black tree: a search tree balanced by colours instead of by height."""

from __future__ import annotations

RED, BLACK = True, False

class Node:
    """One node: a key, its value, both children, its parent, and its colour."""
    __slots__ = ("key", "value", "colour", "left", "right", "parent")

    def __init__(self, key, value, colour=RED):
        """A node holding its own value and its links."""
        self.key = key
        self.value = value
        self.colour = colour
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    """A search tree with O(log n) guaranteed, and fewer rotations than AVL.

    Four rules do the work. The root is black; a red node has no red child; and
    every path from a node down to a missing child passes the same number of
    black nodes. From the last two it follows that the longest path is at most
    twice the shortest, so the height stays within 2·log₂(n+1).

    That bound is weaker than AVL's 1.44·log₂(n), and deliberately so. A
    looser invariant is violated less often, so an insert or delete needs at
    most three rotations instead of a rebalance that can propagate to the root.
    Reads are marginally slower, writes markedly faster.

    That trade is why this is the tree in the standard libraries: `std::map`
    and `std::set` in C++, `TreeMap` and `TreeSet` in Java, and the Linux
    kernel's scheduler and virtual memory areas.

    A single black sentinel stands in for every missing child, which removes
    the null checks that make the delete case analysis unreadable.
    """

    def __init__(self):
        """An empty tree, whose leaves are the shared sentinel."""
        self._nil = Node(None, None, BLACK)
        self._root = self._nil
        self._count = 0

    def _rotate_left(self, node):
        """The left rotation, which lifts the right child."""
        pivot = node.right
        node.right = pivot.left
        if pivot.left is not self._nil:
            pivot.left.parent = node
        pivot.parent = node.parent
        if node.parent is self._nil:
            self._root = pivot
        elif node is node.parent.left:
            node.parent.left = pivot
        else:
            node.parent.right = pivot
        pivot.left = node
        node.parent = pivot

    def _rotate_right(self, node):
        """The right rotation, which lifts the left child."""
        pivot = node.left
        node.left = pivot.right
        if pivot.right is not self._nil:
            pivot.right.parent = node
        pivot.parent = node.parent
        if node.parent is self._nil:
            self._root = pivot
        elif node is node.parent.right:
            node.parent.right = pivot
        else:
            node.parent.left = pivot
        pivot.right = node
        node.parent = pivot

    def insert(self, key, value=None):
        """Store a value under a key, then repair the colouring.

        At most two rotations, where AVL insertion can also need two but
        rebalances more often.
        """
        parent, node = self._nil, self._root
        while node is not self._nil:
            parent = node
            if key == node.key:
                node.value = value
                return
            node = node.left if key < node.key else node.right

        fresh = Node(key, value)
        fresh.left = fresh.right = self._nil
        fresh.parent = parent
        if parent is self._nil:
            self._root = fresh
        elif key < parent.key:
            parent.left = fresh
        else:
            parent.right = fresh
        self._count += 1
        self._fix_insert(fresh)

    def _fix_insert(self, node):
        """Restores the colour conditions after an insertion."""
        while node.parent.colour is RED:
            grandparent = node.parent.parent
            if node.parent is grandparent.left:
                uncle = grandparent.right
                if uncle.colour is RED:
                    node.parent.colour = uncle.colour = BLACK
                    grandparent.colour = RED
                    node = grandparent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self._rotate_left(node)
                    node.parent.colour = BLACK
                    grandparent.colour = RED
                    self._rotate_right(grandparent)
            else:
                uncle = grandparent.left
                if uncle.colour is RED:
                    node.parent.colour = uncle.colour = BLACK
                    grandparent.colour = RED
                    node = grandparent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self._rotate_right(node)
                    node.parent.colour = BLACK
                    grandparent.colour = RED
                    self._rotate_left(grandparent)
        self._root.colour = BLACK

    def _find(self, key):
        """The node holding the key, or nothing when it is absent."""
        node = self._root
        while node is not self._nil and node.key != key:
            node = node.left if key < node.key else node.right
        return node

    def search(self, key):
        """Value stored under the key, or None.

        O(log n): the longest path is at most twice the shortest.
        """
        node = self._find(key)
        return None if node is self._nil else node.value

    def _transplant(self, target, replacement):
        """Replaces one subtree by another in its parent."""
        if target.parent is self._nil:
            self._root = replacement
        elif target is target.parent.left:
            target.parent.left = replacement
        else:
            target.parent.right = replacement
        replacement.parent = target.parent

    def delete(self, key):
        """Remove a key, then repair the colouring.

        At most three rotations, which is why this tree is preferred where
        deletions are frequent.
        """
        node = self._find(key)
        if node is self._nil:
            return False

        removed_colour = node.colour
        if node.left is self._nil:
            moved = node.right
            self._transplant(node, node.right)
        elif node.right is self._nil:
            moved = node.left
            self._transplant(node, node.left)
        else:
            successor = node.right
            while successor.left is not self._nil:
                successor = successor.left
            removed_colour = successor.colour
            moved = successor.right
            if successor.parent is node:
                moved.parent = successor
            else:
                self._transplant(successor, successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self._transplant(node, successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.colour = node.colour

        self._count -= 1
        if removed_colour is BLACK:
            self._fix_delete(moved)
        return True

    def _fix_delete(self, node):
        """Restores the colour conditions after a deletion."""
        while node is not self._root and node.colour is BLACK:
            if node is node.parent.left:
                sibling = node.parent.right
                if sibling.colour is RED:
                    sibling.colour = BLACK
                    node.parent.colour = RED
                    self._rotate_left(node.parent)
                    sibling = node.parent.right
                if sibling.left.colour is BLACK and sibling.right.colour is BLACK:
                    sibling.colour = RED
                    node = node.parent
                else:
                    if sibling.right.colour is BLACK:
                        sibling.left.colour = BLACK
                        sibling.colour = RED
                        self._rotate_right(sibling)
                        sibling = node.parent.right
                    sibling.colour = node.parent.colour
                    node.parent.colour = BLACK
                    sibling.right.colour = BLACK
                    self._rotate_left(node.parent)
                    node = self._root
            else:
                sibling = node.parent.left
                if sibling.colour is RED:
                    sibling.colour = BLACK
                    node.parent.colour = RED
                    self._rotate_right(node.parent)
                    sibling = node.parent.left
                if sibling.right.colour is BLACK and sibling.left.colour is BLACK:
                    sibling.colour = RED
                    node = node.parent
                else:
                    if sibling.left.colour is BLACK:
                        sibling.right.colour = BLACK
                        sibling.colour = RED
                        self._rotate_left(sibling)
                        sibling = node.parent.left
                    sibling.colour = node.parent.colour
                    node.parent.colour = BLACK
                    sibling.left.colour = BLACK
                    self._rotate_right(node.parent)
                    node = self._root
        node.colour = BLACK

    def items(self):
        """Every pair in ascending key order."""
        stack, node = [], self._root
        while stack or node is not self._nil:
            while node is not self._nil:
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
        """Height in nodes, bounded by 2 log(n+1)."""
        tallest = 0
        stack = [(self._root, 1)]
        while stack:
            node, depth = stack.pop()
            if node is self._nil:
                continue
            tallest = max(tallest, depth)
            stack.append((node.left, depth + 1))
            stack.append((node.right, depth + 1))
        return tallest

    def obeys_the_rules(self):
        """Check the four invariants, which is the only way to trust the colours."""
        if self._root.colour is not BLACK:
            return False

        def check(node):
            """Return the black height, or None if a rule is broken."""
            if node is self._nil:
                return 1
            if node.colour is RED and (node.left.colour is RED or node.right.colour is RED):
                return None
            left, right = check(node.left), check(node.right)
            if left is None or right is None or left != right:
                return None
            return left + (0 if node.colour is RED else 1)

        return check(self._root) is not None

    def __contains__(self, key):
        """Whether the key is stored."""
        return self._find(key) is not self._nil

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
