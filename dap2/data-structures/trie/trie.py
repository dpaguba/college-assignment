"""Trie: a tree where the path spells the key, so the key is never stored."""

from __future__ import annotations

MISSING = object()

class Node:
    """One node: its children by character, and whether a word ends here."""
    __slots__ = ("children", "value", "is_word")

    def __init__(self):
        """A node holding its own value and its links."""
        self.children: dict[str, "Node"] = {}
        self.value = None
        self.is_word = False

class Trie:
    """A dictionary for strings whose lookup cost ignores how many keys there are.

    Every other structure here compares whole keys. A trie walks one character
    at a time, and the path from the root spells the word, so the key itself is
    never stored in any node. Looking up a word of length m costs m steps
    whether the trie holds ten words or ten million: the size of the dictionary
    does not appear in the complexity at all.

    Two things follow that no hash table can offer. Prefix queries are free,
    because a prefix is simply a node, and everything below it is the answer,
    which is how autocomplete works. And the keys come out in lexicographic
    order if the children are visited in order.

    The cost is memory. A node per character per distinct prefix is expensive,
    which is what radix trees, which merge single-child chains, and burstsort,
    which keeps small buckets flat, are both trying to fix.
    """

    def __init__(self):
        """An empty trie."""
        self._root = Node()
        self._count = 0

    def _walk(self, word):
        """The node reached by following the word, or nothing."""
        node = self._root
        for character in word:
            node = node.children.get(character)
            if node is None:
                return None
        return node

    def insert(self, word, value=None):
        """Store a value under a word.

        O(length of the word), independent of how many words are already
        stored.
        """
        node = self._root
        for character in word:
            node = node.children.setdefault(character, Node())
        if not node.is_word:
            self._count += 1
        node.is_word = True
        node.value = value

    def search(self, word):
        """Value stored under the word, or None.

        Membership is the in operator, since a word may legitimately hold the
        value None.
        """
        node = self._walk(word)
        return node.value if node is not None and node.is_word else None

    def delete(self, word):
        """Remove a word.

        The path is collected on the way down so that nodes left empty can be
        pruned on the way back up; without the pruning a trie only ever grows.
        """
        path = [self._root]
        node = self._root
        for character in word:
            node = node.children.get(character)
            if node is None:
                return False
            path.append(node)
        if not node.is_word:
            return False

        node.is_word = False
        node.value = None
        self._count -= 1

        for index in range(len(path) - 1, 0, -1):
            child = path[index]
            if child.children or child.is_word:
                break
            del path[index - 1].children[word[index - 1]]
        return True

    def starts_with(self, prefix):
        """True when any stored word begins with this prefix."""
        return self._walk(prefix) is not None

    def with_prefix(self, prefix):
        """Every stored word beginning with this prefix, in order."""
        node = self._walk(prefix)
        if node is None:
            return []

        found: list[str] = []
        stack = [(node, prefix)]
        while stack:
            current, text = stack.pop()
            if current.is_word:
                found.append(text)
            for character in sorted(current.children, reverse=True):
                stack.append((current.children[character], text + character))
        return sorted(found)

    def keys(self):
        """Every stored word in alphabetical order."""
        return iter(self.with_prefix(""))

    def items(self):
        """Every word and its value, in alphabetical order."""
        for word in self.with_prefix(""):
            yield word, self.search(word)

    def __contains__(self, word):
        """Whether the key is stored."""
        node = self._walk(word)
        return node is not None and node.is_word

    def __len__(self):
        """How many entries the structure holds."""
        return self._count
