# Shortest common superstring

A greedy heuristic. Practical sheet 5, task 5.2.

```
java ShortestCommonSuperstring AEIOU AAE IIAU UUAI
AEIOU AAE IIAU UUAI
Ersetze AAE und AEIOU durch AAEIOU
IIAU UUAI AAEIOU
Ersetze IIAU und UUAI durch IIAUUAI
AAEIOU IIAUUAI
Ersetze AAEIOU und IIAUUAI durch AAEIOUIIAUUAI
AAEIOUIIAUUAI
Superstring AAEIOUIIAUUAI mit Laenge 13 gefunden.
```

## The algorithm

Repeatedly merge the two strings with the largest overlap, in either order.
Each round costs O(k²·L) for k remaining strings of length up to L, and there
are k − 1 rounds.

## The two questions the sheet asks

**Which case is not handled?** A string already contained in another one. It is
never removed, so it gets concatenated as though it carried new letters, and
the result comes out longer than necessary. `AB AAB` shows it.

**Is it always optimal?** No. The shortest common superstring problem is
NP-hard, and this greedy rule is only known to stay within a constant factor.
It is also the standard textbook example of a greedy heuristic that is good
enough to be used in practice: genome assembly by overlap is this algorithm
with a lot of engineering on top.

## Ties

The largest overlap is updated only on a strictly greater value, so the earliest
pair wins a tie and the output is reproducible. When nothing overlaps at all,
the first two strings are concatenated, which keeps the loop making progress.

## Verification

The first example matches the sheet line for line, including the order of the
array after each replacement, which is what shows that the merged string is
appended at the end rather than replacing one of its parts in place.

The second example, `java ShortestCommonSuperstring 11`, produces a superstring
of **length 36**, which the sheet also gives, but a different one:
`EEIAAEEOEAOOIAUUIOOOIUAIAIUUIIAOUOUO` here against
`EAOOIAUUIOOOIUAIAIUUIIAAEEOEEIAOUOUO` on the sheet. Both were checked to
contain all eleven input strings, and four plausible tie-breaking variants were
tried against the sheet's string without reproducing it. The sheet does not
specify a tie-breaking rule, and the length, which is what the algorithm
optimises, agrees.

An assertion checks that the result really contains every input string.
