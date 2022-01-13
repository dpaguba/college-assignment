# Compression

| Topic | |
|---|---|
| [huffman](huffman/) | frequencies into a prefix-free code |

Chapter six, which is where the course's first four chapters meet. The
frequencies are counted with an array, the tree is built by repeatedly taking
two minima, which is what the priority queue of chapter nineteen is for, and
the tree itself is the binary tree of chapter seven used for something other
than searching.

The result on German prose is a saving of 48 percent, and the reason is that
letter frequencies are uneven. That is worth stating as a limit rather than as
a headline: the algorithm is optimal among codes that give each character a
whole number of bits, and it saves nothing at all on data whose symbols occur
equally often.
