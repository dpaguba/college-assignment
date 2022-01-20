"""Binary search tree: smaller keys left, larger keys right, all the way down."""

from __future__ import annotations

class Node:
    """One node: a key, its value, and both children."""
    __slots__ = ("key", "value", "left", "right")

    def __init__(self, key, value):
        """A node holding its own value and its links."""
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class BinarySearchTree:
    """A dictionary that also keeps its keys in order.

    The invariant is one sentence: everything in a node's left subtree is
    smaller than the node, everything right is larger. From it follows both
    the search, compare and descend, and the ordered traversal, left then node
    then right.

    That ordering is what a hash table cannot give. A hash table answers "is
    this key here" faster; it cannot answer "what is the next key after this
    one", or "give me everything between 10 and 20", because hashing destroys
    order on purpose.

    The cost is the shape. Inserting sorted keys produces one long chain and
    every operation becomes O(n), which is exactly the case AVL and red-black
    trees exist to prevent. Deleting a node with two children is the other
    awkward part, and the standard answer is below: replace it with its
    in-order successor, the smallest key in the right subtree, which is the
    only key that can take its place without breaking the invariant.
    """

    def __init__(self):
        """An empty tree."""
        self._root = None
        self._count = 0

    def insert(self, key, value=None):
        """Store a value under a key.

        O(h), which is O(log n) on mixed input and O(n) on sorted input, since
        nothing here rebalances.
        """
        if self._root is None:
            self._root = Node(key, value)
            self._count = 1
            return

        node = self._root
        while True:
            if key == node.key:
                node.value = value
                return
            side = "left" if key < node.key else "right"
            child = getattr(node, side)
            if child is None:
                setattr(node, side, Node(key, value))
                self._count += 1
                return
            node = child

    def _find(self, key):
        """The node holding the key, or nothing when it is absent."""
        node = self._root
        while node is not None and node.key != key:
            node = node.left if key < node.key else node.right
        return node

    def search(self, key):
        """Value stored under the key, or None. O(h)."""
        node = self._find(key)
        return None if node is None else node.value

    def delete(self, key):
        """Remove a key.

        The two-child case takes the in-order successor, which by construction
        has no left child, so replacing the node with it cannot break the
        ordering.
        """
        parent, node = None, self._root
        while node is not None and node.key != key:
            parent, node = node, (node.left if key < node.key else node.right)
        if node is None:
            return False

        if node.left is not None and node.right is not None:
            successor_parent, successor = node, node.right
            while successor.left is not None:
                successor_parent, successor = successor, successor.left
            node.key, node.value = successor.key, successor.value
            parent, node = successor_parent, successor

        child = node.left if node.left is not None else node.right
        if parent is None:
            self._root = child
        elif parent.left is node:
            parent.left = child
        else:
            parent.right = child

        self._count -= 1
        return True

    def items(self):
        """In-order traversal, which visits the keys in ascending order."""
        stack, node = [], self._root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key, node.value
            node = node.right

    def keys(self):
        """Every key in ascending order, by in-order walk."""
        for key, _ in self.items():
            yield key

    def height(self):
        """The longest path to a leaf, which is what balancing is about.

        Walked with an explicit stack rather than by recursion. A tree built
        from sorted keys is one chain n nodes deep, and recursing down it
        overflows the interpreter stack: the structure would fail on exactly
        the input that demonstrates its weakness.
        """
        tallest = 0
        stack = [(self._root, 1)]
        while stack:
            node, depth = stack.pop()
            if node is None:
                continue
            tallest = max(tallest, depth)
            stack.append((node.left, depth + 1))
            stack.append((node.right, depth + 1))
        return tallest

    def __contains__(self, key):
        """Whether the key is stored."""
        return self._find(key) is not None

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
