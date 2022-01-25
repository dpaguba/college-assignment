# Trie

A tree where the path spells the key, so the key is never stored.

| Operation | Cost |
|---|---|
| Insert | O(m), m is the key length |
| Search | O(m) |
| Delete | O(m) |
| Every word with a prefix | O(size of the answer) |

| | |
|---|---|
| Memory | O(total characters), which is a great deal |
| Ordered | yes, lexicographically |

## The idea

Every other structure here compares whole keys. A trie walks one character at a
time, and the path from the root spells the word, so the key itself is never stored
in any node.

Looking up a word of length m costs m steps whether the trie holds ten words or ten
million. The size of the dictionary does not appear in the complexity at all, which
no comparison structure can claim.

Two things follow that a hash table cannot offer. Prefix queries are free, because a
prefix is simply a node and everything below it is the answer, which is how
autocomplete works. And the keys come out in lexicographic order.

## How it works

A node holds a map from character to child, a flag saying whether a word ends here,
and the value if it does. The flag matters: "ban" being on the path to "banana" does
not make it a stored word, which is what `starts_with` and `in` distinguish.

Deletion walks back up the path pruning nodes that no longer lead anywhere, so a
trie that has had everything removed is empty rather than a skeleton.

## The trade

A node per character per distinct prefix is expensive. Radix trees, which merge single-child chains into one edge, and burstsort, which keeps small buckets flat, are both fixes for exactly that cost.

## Where it is used

Autocomplete, spell checkers, IP routing tables (as a radix trie on the address bits), and the dictionary inside every word game solver.
