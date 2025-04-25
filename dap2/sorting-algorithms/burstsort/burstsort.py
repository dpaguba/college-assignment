"""Burstsort: a trie whose leaves are buckets that burst when they fill up.

A bucket bursts into a trie node once it holds more than the limit. Larger
buckets mean fewer nodes and worse cache behaviour; the papers settle around
this range.
"""

from __future__ import annotations

BURST_THRESHOLD = 32

class Trie:
    """One trie node: a child per first character, plus a bucket per branch."""

    __slots__ = ("children", "buckets", "terminal")

    def __init__(self):
        """A node with no children and empty buckets."""
        self.children: dict[str, "Trie"] = {}
        self.buckets: dict[str, list[str]] = {}
        self.terminal: list[str] = []

def burstsort(strings, threshold=BURST_THRESHOLD):
    """Return a sorted copy of `strings`.

    Radix sort for strings, arranged for the cache. A plain MSD radix sort
    creates a trie node per distinct prefix, and walking those nodes misses the
    cache on nearly every step. Burstsort keeps strings in flat buckets and
    only turns a bucket into a trie node when it grows past a threshold, so the
    structure stays shallow and the strings that share a prefix stay next to
    each other in memory.

    That is why it beat the previous string sorts in the early 2000s: the
    comparison count barely changed, the cache misses collapsed.
    """
    values = list(strings)
    if len(values) < 2:
        return values

    root = Trie()

    def insert(node, text, depth):
        """Adds a word, bursting a bucket that has grown too large."""
        while True:
            if depth == len(text):
                node.terminal.append(text)
                return
            head = text[depth]
            if head in node.children:
                node, depth = node.children[head], depth + 1
                continue
            bucket = node.buckets.setdefault(head, [])
            bucket.append(text)
            if len(bucket) > threshold:
                child = Trie()
                node.children[head] = child
                del node.buckets[head]
                for held in bucket:
                    insert(child, held, depth + 1)
            return

    for text in values:
        insert(root, text, 0)

    def collect(node, out):
        """Appends the words below the node in order."""
        out.extend(node.terminal)
        for head in sorted(set(node.children) | set(node.buckets)):
            if head in node.children:
                collect(node.children[head], out)
            else:
                out.extend(sorted(node.buckets[head]))

    ordered: list[str] = []
    collect(root, ordered)
    return ordered
