"""Doubly linked list: every node knows both neighbours, so removal is local."""

from __future__ import annotations


class Node:
    """One node: a value and links to both neighbours."""
    __slots__ = ("value", "previous", "next")

    def __init__(self, value):
        """A node holding its own value and its links."""
        self.value = value
        self.previous = None
        self.next = None


class DoublyLinkedList:
    """A sequence where inserting and removing cost O(1) if you hold the node.

    An array stores elements next to each other, so removing from the middle
    shifts everything after it. A linked list stores a pointer instead, so
    removal is three assignments and no movement at all.

    The catch is the other half of the trade. An array can reach element
    1000 by arithmetic; a list has to walk a thousand pointers, and each of
    them is likely a cache miss. Which is why arrays win in practice far more
    often than the complexity table suggests.

    The second pointer, backwards, is what makes removal O(1). With only a
    forward pointer you must first find the previous node, which costs a scan,
    and that difference is the entire reason doubly linked lists exist.

    The pattern shows up wherever something must be unlinked from a position
    it already holds: an LRU cache moving an entry to the front, a scheduler's
    run queue, an editor's undo history.

    A pair of sentinel nodes stands at both ends, so no operation ever needs to
    ask whether it is at the boundary.
    """

    def __init__(self, values=None):
        """An empty list with its two sentinel nodes."""
        self._head = Node(None)
        self._tail = Node(None)
        self._head.next = self._tail
        self._tail.previous = self._head
        self._count = 0
        for value in values or ():
            self.push_back(value)

    def _insert_between(self, value, left, right):
        """Links a new node between two existing ones."""
        node = Node(value)
        node.previous, node.next = left, right
        left.next = right.previous = node
        self._count += 1
        return node

    def push_front(self, value):
        """Add at the front.

        O(1), which is the whole reason to prefer this over an array.
        """
        return self._insert_between(value, self._head, self._head.next)

    def push_back(self, value):
        """Add at the back. O(1), thanks to the tail pointer."""
        return self._insert_between(value, self._tail.previous, self._tail)

    def remove(self, node):
        """Unlink a node that is already in hand. This is the O(1) operation."""
        if node is self._head or node is self._tail:
            raise ValueError("the sentinels are not part of the list")
        node.previous.next = node.next
        node.next.previous = node.previous
        node.previous = node.next = None
        self._count -= 1
        return node.value

    def pop_front(self):
        """Remove and return the first value. O(1)."""
        if self._count == 0:
            raise IndexError("pop from an empty list")
        return self.remove(self._head.next)

    def pop_back(self):
        """Remove and return the last value.

        O(1), where a singly linked list would need O(n) to find the new tail.
        """
        if self._count == 0:
            raise IndexError("pop from an empty list")
        return self.remove(self._tail.previous)

    def find(self, value):
        """The node holding this value, or None. This is the O(n) operation."""
        node = self._head.next
        while node is not self._tail:
            if node.value == value:
                return node
            node = node.next
        return None

    def __iter__(self):
        """The values, in order."""
        node = self._head.next
        while node is not self._tail:
            yield node.value
            node = node.next

    def reversed(self):
        """Walk the values from back to front, following the backward links."""
        node = self._tail.previous
        while node is not self._head:
            yield node.value
            node = node.previous

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
