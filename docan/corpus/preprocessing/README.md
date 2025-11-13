# Preprocessing

Stopwords out, then the Porter stemmer. The order matters: stemming first
would turn a stopword into a stem that is no longer in the list, and the word
would survive.

The stemmer is the full five-step algorithm, checked against 42 of the word
pairs published with it: `caresses → caress`, `ponies → poni`, `ties → ti`,
`feed → feed`, `agreed → agre`, `sensibiliti → sensibl`, `relational → relat`.

## One detail decides several of those

Within a step, the rule with the longest matching suffix is selected, and if
its condition fails, the word is left alone: no shorter rule is tried
afterwards. That single rule is why `feed` stays `feed` while `agreed` loses
its ending. Both end in a match; only one has the length to spend.

## The two ways it goes wrong

**Over-stemming**, unrelated words collapsing into one stem, measured on this
implementation:

| | | stem |
|---|---|---|
| general | generous | `gener` |
| news | new | `new` |
| experiment | experience | `experi` |

**Under-stemming**, related forms staying apart: `mouse` and `mice`, `run` and
`ran`. The algorithm reads endings and knows no words, so an irregular form is
out of reach in principle.

The interesting case is `relative → rel` against `relate → relat`: two forms
of one root separated by the algorithm's own steps, because one ending is
replaced in step two and the other falls in step four. Over- and
under-stemming are not opposite failures of care; they are the same mechanism
seen from two sides.

## What it is good enough for

Retrieval, where all that matters is that related forms land on the same key.
Not for anything that reads the stem itself: `poni` and `sensibl` are not
words and were never meant to be.
