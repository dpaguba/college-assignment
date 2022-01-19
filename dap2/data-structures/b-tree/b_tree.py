"""B-tree: a search tree with many keys per node, shaped for disks and caches.

The minimum degree fixes how much a node holds: between t-1 and 2t-1 keys, so
the branching factor is between t and 2t. Real databases pick it so that one
node fills one disk page, which is where the whole design comes from.
"""

from __future__ import annotations

MIN_DEGREE = 3

class Node:
    """One node: its keys, their values, its children, and whether it is a leaf."""
    __slots__ = ("keys", "values", "children", "leaf")

    def __init__(self, leaf=True):
        """A node holding its own value and its links."""
        self.keys: list = []
        self.values: list = []
        self.children: list[Node] = []
        self.leaf = leaf

class BTree:
    """A search tree that minimises the number of nodes visited, not comparisons.

    A binary tree over a million keys is twenty levels deep, and if each level
    is a separate disk page that is twenty seeks. A B-tree of degree 100 holds
    the same million keys in three levels, so the same lookup costs three
    reads. The comparison count barely changes; the number of pages touched
    collapses, and that is the number that decides how long a query takes.

    This is why every relational database index, every filesystem directory
    (NTFS, HFS+, ext4, btrfs) and most key-value stores are B-trees or B+
    trees rather than binary trees.

    Balance is maintained differently from a binary tree. Nothing rotates.
    A node that overflows splits in two and pushes its middle key up, and a
    node that underflows borrows from a sibling or merges with one. Because
    growth happens at the root rather than the leaves, every leaf is at the
    same depth by construction.
    """

    def __init__(self, degree=MIN_DEGREE):
        """An empty tree of the given degree."""
        self._t = degree
        self._root = Node(leaf=True)
        self._count = 0

    def _search_node(self, node, key):
        """The node and position holding the key, or nothing."""
        position = 0
        while position < len(node.keys) and key > node.keys[position]:
            position += 1
        if position < len(node.keys) and node.keys[position] == key:
            return node, position
        if node.leaf:
            return None, None
        return self._search_node(node.children[position], key)

    def search(self, key):
        """Value stored under the key, or None.

        O(log n) comparisons but far fewer node visits than a binary tree,
        which is the point on disk.
        """
        node, position = self._search_node(self._root, key)
        return None if node is None else node.values[position]

    def _split_child(self, parent, index):
        """Split a full child in two and lift its middle key into the parent."""
        t = self._t
        full = parent.children[index]
        fresh = Node(leaf=full.leaf)

        middle_key = full.keys[t - 1]
        middle_value = full.values[t - 1]

        fresh.keys = full.keys[t:]
        fresh.values = full.values[t:]
        full.keys = full.keys[: t - 1]
        full.values = full.values[: t - 1]

        if not full.leaf:
            fresh.children = full.children[t:]
            full.children = full.children[:t]

        parent.keys.insert(index, middle_key)
        parent.values.insert(index, middle_value)
        parent.children.insert(index + 1, fresh)

    def insert(self, key, value=None):
        """Store a value under a key, splitting full nodes on the way down.
        Splitting eagerly means the descent never has to back up.
        """
        node, position = self._search_node(self._root, key)
        if node is not None:
            node.values[position] = value
            return

        root = self._root
        if len(root.keys) == 2 * self._t - 1:
            fresh = Node(leaf=False)
            fresh.children.append(root)
            self._split_child(fresh, 0)
            self._root = fresh

        self._insert_non_full(self._root, key, value)
        self._count += 1

    def _insert_non_full(self, node, key, value):
        """Inserts into a node that has room, splitting children as needed."""
        position = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while position >= 0 and key < node.keys[position]:
                node.keys[position + 1] = node.keys[position]
                node.values[position + 1] = node.values[position]
                position -= 1
            node.keys[position + 1] = key
            node.values[position + 1] = value
            return

        while position >= 0 and key < node.keys[position]:
            position -= 1
        position += 1
        if len(node.children[position].keys) == 2 * self._t - 1:
            self._split_child(node, position)
            if key > node.keys[position]:
                position += 1
        self._insert_non_full(node.children[position], key, value)

    def delete(self, key):
        """Remove a key, refilling thin children on the way down.

        One trap: filling a child may merge it into its left sibling, and the
        key being chased is then one position further left. Ignoring that
        deletes from the wrong subtree.
        """
        if self.search(key) is None and key not in self:
            return False
        self._delete(self._root, key)
        if not self._root.keys and not self._root.leaf:
            self._root = self._root.children[0]
        self._count -= 1
        return True

    def _delete(self, node, key):
        """Deletes the key from the subtree, keeping every node full enough."""
        t = self._t
        position = 0
        while position < len(node.keys) and key > node.keys[position]:
            position += 1

        if position < len(node.keys) and node.keys[position] == key:
            if node.leaf:
                node.keys.pop(position)
                node.values.pop(position)
                return
            left, right = node.children[position], node.children[position + 1]
            if len(left.keys) >= t:
                key_p, value_p = self._largest(left)
                node.keys[position], node.values[position] = key_p, value_p
                self._delete(left, key_p)
            elif len(right.keys) >= t:
                key_s, value_s = self._smallest(right)
                node.keys[position], node.values[position] = key_s, value_s
                self._delete(right, key_s)
            else:
                self._merge(node, position)
                self._delete(left, key)
            return

        if node.leaf:
            return

        if len(node.children[position].keys) < t:
            position = self._fill(node, position)
        self._delete(node.children[position], key)

    @staticmethod
    def _largest(node):
        """The largest entry of the subtree."""
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1], node.values[-1]

    @staticmethod
    def _smallest(node):
        """The smallest entry of the subtree."""
        while not node.leaf:
            node = node.children[0]
        return node.keys[0], node.values[0]

    def _fill(self, parent, index):
        """Make a thin child fat enough to delete from, and say where it ended up.

        Borrowing leaves the child where it was. Merging with the left sibling
        moves it one place left, and the caller has to follow it.
        """
        t = self._t
        if index > 0 and len(parent.children[index - 1].keys) >= t:
            self._borrow_from_left(parent, index)
            return index
        if index < len(parent.children) - 1 and len(parent.children[index + 1].keys) >= t:
            self._borrow_from_right(parent, index)
            return index
        if index > 0:
            self._merge(parent, index - 1)
            return index - 1
        self._merge(parent, index)
        return index

    def _borrow_from_left(self, parent, index):
        """Moves one entry from the left sibling through the parent."""
        child, sibling = parent.children[index], parent.children[index - 1]
        child.keys.insert(0, parent.keys[index - 1])
        child.values.insert(0, parent.values[index - 1])
        parent.keys[index - 1] = sibling.keys.pop()
        parent.values[index - 1] = sibling.values.pop()
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_right(self, parent, index):
        """Moves one entry from the right sibling through the parent."""
        child, sibling = parent.children[index], parent.children[index + 1]
        child.keys.append(parent.keys[index])
        child.values.append(parent.values[index])
        parent.keys[index] = sibling.keys.pop(0)
        parent.values[index] = sibling.values.pop(0)
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def _merge(self, parent, index):
        """Joins two children and the separating key into one node."""
        left, right = parent.children[index], parent.children[index + 1]
        left.keys.append(parent.keys.pop(index))
        left.values.append(parent.values.pop(index))
        left.keys.extend(right.keys)
        left.values.extend(right.values)
        if not left.leaf:
            left.children.extend(right.children)
        parent.children.pop(index + 1)

    def items(self):
        """Every pair in ascending key order."""
        def walk(node):
            """The entries of the subtree, in order."""
            for position, key in enumerate(node.keys):
                if not node.leaf:
                    yield from walk(node.children[position])
                yield key, node.values[position]
            if not node.leaf:
                yield from walk(node.children[-1])

        yield from walk(self._root)

    def keys(self):
        """Every key in ascending order."""
        for key, _ in self.items():
            yield key

    def height(self):
        """Height in nodes.

        It falls with the degree: 10000 keys need 14 levels at degree 2 and 2
        at degree 100.
        """
        depth, node = 1, self._root
        while not node.leaf:
            depth, node = depth + 1, node.children[0]
        return depth

    def obeys_the_rules(self):
        """Every leaf at the same depth, and no node outside its key limits."""
        t = self._t
        depths = set()

        def check(node, depth, is_root):
            """Whether the subtree obeys the degree and depth conditions."""
            if node.leaf:
                depths.add(depth)
            if not is_root and not (t - 1 <= len(node.keys) <= 2 * t - 1):
                return False
            if node.keys != sorted(node.keys):
                return False
            if not node.leaf and len(node.children) != len(node.keys) + 1:
                return False
            return all(check(child, depth + 1, False) for child in node.children)

        return check(self._root, 1, True) and len(depths) == 1

    def __contains__(self, key):
        """Whether the key is stored."""
        node, _ = self._search_node(self._root, key)
        return node is not None

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
