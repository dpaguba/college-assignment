# Recursion

| Topic | |
|---|---|
| [recursive-algorithms](recursive-algorithms/) | the pots, the stairs, the ship |
| [expression-evaluation](expression-evaluation/) | plus and minus, until it sums to zero |

Chapter five and the fifth sheet. The examples are chosen so that recursion
produces three different kinds of thing: a sequence of moves, a count, and a
decision with a witness.

Both modules are verified against brute force, because backtracking is where
these algorithms go wrong. A branch pruned by a condition that is slightly too
strong produces an answer that looks entirely reasonable and is false, and no
amount of reading the code makes that visible. The ship's tolerance is the
example: the smallest workable value is four rather than two, and the reason
is that the check applies after every container rather than only at the end.
