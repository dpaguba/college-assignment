# DAP 1

Twenty-one modules in eight blocks, in Java, following the nineteen chapters
of the lecture and the twelve exercise sheets.

| Block | |
|---|---|
| [foundations](foundations/) | syntax diagrams, integer arithmetic, arrays |
| [searching](searching/) | linear against binary, and the two stacks of exam papers |
| [sorting](sorting/) | selection, insertion, bubble, counting, quicksort |
| [recursion](recursion/) | the pots, the stairs, the ship, expressions |
| [object-design](object-design/) | fractions, inheritance, generics, lambdas |
| [data-structures](data-structures/) | list, ring buffer, tree, hash table, heap |
| [patterns](patterns/) | iterator and strategy |
| [compression](compression/) | Huffman coding |

## The published solution, reproduced

The course publishes one solution, to the first sheet, and both of its
checkable parts come out. The five integer methods are reproduced exactly and
verified against Java's own operators over 720 pairs of arguments, with the
constraint of the exercise (a single `return` and only `+ - * /`) checked by
reading the source rather than asserted in prose.

The syntax diagram for expressions is verified in a way the solution only
gestures at. It says the diagram is clearer than the nine rules of prose it
replaces; counting derivations shows it is also unambiguous, giving one parse
tree for `u+v+w` where the obvious grammar gives two, and one for `u+v*w+x`
where the obvious grammar gives five.

## Numbers worth keeping

| | |
|---|---:|
| binary search on 1024 values, worst case | 11 comparisons |
| two piles of 500, unsorted against sorted | 194 389 against 666 |
| selection sort on 200 values, any input | 19 900 comparisons |
| insertion sort, sorted against reversed | 199 against 19 900 |
| quicksort with the last-element pivot, sorted input | 19 900 |
| the same with a middle pivot | 1 153 |
| search tree of 1023 values: balanced, random, sorted insertion | depth 10, 23, 1023 |
| hash table, 500 keys: fixed 16 buckets against growing | longest bucket 42 against 4 |
| heapify 63 values: sift down against insert | 57 against 258 exchanges |
| Huffman on 126 characters of German prose | 48.4 percent saved |
| twenty stairs, steps of one or two | 10 946 ways |

## Four results that argue with the material

**The improved insertion sort is worse where it matters most.** The fourth
sheet asks for insertion sort with the insertion point found by binary search.
On reversed input it is seventeen times cheaper in comparisons. On sorted
input it is nearly seven times more expensive, because the linear scan it
replaces was stopping after one comparison. It also performs exactly the same
number of moves, so on an array whose cost is dominated by shifting, halving
the comparisons buys less than the count suggests.

**The better pivot is the slower one on ordinary input.** Quicksort's
middle-element pivot turns the 19 900 comparisons of sorted input into 1 153,
and costs five percent more than the last-element pivot on random input. The
rule that removes the disaster is slightly worse whenever there is no disaster.

**A search tree is a linked list on the most ordinary input there is.**
Inserting 1023 values in ascending order gives depth 1023 rather than 10. The
structure whose whole claim is logarithmic behaviour is linear on data that
arrives sorted, which is exactly the data most likely to be lying around.

**Building a heap is linear, and inserting into one is not.** Heapifying 63
descending values takes 57 exchanges by sifting down and 258 by inserting one
at a time. Half the nodes are leaves and cost nothing in the first version,
while every value has to climb the full height in the second.

## Verification

There are no published solutions past the first sheet, so every module is
checked against something independent: the sorts against `Arrays.sort`, the
list against `ArrayList`, the tree against `TreeMap`, the hash table against
`HashMap`, the backtracking searches against brute force over every sign
pattern, and the two searches against each other on 200 random targets. The
exam tasks from the extra sheets are implemented against the class signatures
the appendix prints, so they sit on the course's own API rather than a
convenient one.
