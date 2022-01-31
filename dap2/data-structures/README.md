# Data structures

Thirteen structures, one folder each, in plain Python with no dependencies.
Every folder holds the implementation and a README explaining the idea, how it
works, what it costs and what it gives up.

Sorting and searching are algorithms over data somebody else arranged. These
are the arrangements, and most of the complexity in the other two folders is a
consequence of which one was chosen.

## Sequences

| Structure | Index | Insert at the end | Insert in the middle | Memory |
|---|---|---|---|---|
| [dynamic-array](dynamic-array/) | O(1) | O(1) amortised | O(n) | contiguous |
| [doubly-linked-list](doubly-linked-list/) | O(n) | O(1) | O(1) with the node | two pointers per element |

## Dictionaries without order

| Structure | Search | Insert | Delete | Note |
|---|---|---|---|---|
| [hash-table-chaining](hash-table-chaining/) | O(1) average | O(1) average | O(1) average | a list per bucket |
| [hash-table-open-addressing](hash-table-open-addressing/) | O(1) average | O(1) average | leaves a tombstone | one flat array |
| [bloom-filter](bloom-filter/) | O(k) | O(k) | impossible | stores nothing, answers probably |

## Dictionaries that keep order

| Structure | Search | Insert | Delete | Height on 1000 sorted keys |
|---|---|---|---|---|
| [binary-search-tree](binary-search-tree/) | O(n) worst | O(n) worst | O(n) worst | **1000** |
| [avl-tree](avl-tree/) | O(log n) | O(log n) | O(log n) | 10 |
| [red-black-tree](red-black-tree/) | O(log n) | O(log n) | O(log n) | 17 |
| [b-tree](b-tree/) | O(log_t n) | O(log_t n) | O(log_t n) | 3 at degree 50 |
| [skip-list](skip-list/) | O(log n) expected | O(log n) expected | O(log n) expected | about 10 |
| [trie](trie/) | O(m) | O(m) | O(m) | depends on the key, not the count |
| [van-emde-boas-tree](van-emde-boas-tree/) | O(log log u) | O(log log u) | O(log log u) | 5 over 32-bit keys |

## One question only

| Structure | What it answers | Cost |
|---|---|---|
| [binary-heap](binary-heap/) | what is the smallest | O(1) to look, O(log n) to remove |

## Choosing one

**Do you need the keys in order?** If not, take a hash table: it is faster at
the only thing it does. If yes, no hash table will help, because hashing
destroys order deliberately.

**Where does the data live?** In memory, a balanced binary tree. On disk or
behind a page cache, a B-tree, because the count that matters is pages
touched, not comparisons made.

**Reads or writes?** AVL is shallower and rebalances more; red-black is
deeper and rebalances less. Read-heavy takes the first, write-heavy the
second, which is why the standard libraries all chose red-black.

**Are the keys strings?** A trie, and prefix queries come free.

**Are the keys small integers and you need the next one?** van Emde Boas, if
you can pay O(u) memory. Otherwise a balanced tree.

**Is a wrong yes acceptable?** A Bloom filter, and the memory drops by orders
of magnitude.

**Do you only ever want the smallest?** A heap. Anything else is doing work
you are not using.

## How this was built

Test first. Each structure got a test file before it had an implementation,
run to watch it fail for the right reason, then the code, then the run again.
A shared contract ran random sequences of insert, search, delete and contains
against a plain Python dict and demanded agreement at every step, which is how
the awkward cases get covered without anyone thinking of them.

The structures with an invariant got a second test that checks the invariant
itself, because the dictionary contract cannot tell a balanced tree from an
unbalanced one that happens to answer correctly. The AVL test asserts the
balance factor after every insert; the red-black test checks all four colour
rules after every one of 600 random operations; the B-tree test checks that
every leaf stays at the same depth.

Those tests earned their place three times: the B-tree deleted the wrong
subtree after a merge, because the child it was chasing had shifted one place
left; the binary search tree overflowed the interpreter stack computing its own
height on 1000 sorted keys, which is both a bug and a demonstration; and the
balance test was verified to fail on the unbalanced tree before being trusted
on the balanced one.

The tests were removed once all 55 passed, so what remains is the library and
the explanations.
