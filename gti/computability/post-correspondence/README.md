# The Post correspondence problem

Given pairs of strings, is there a non-empty sequence of indices spelling the
same word on both sides?

```
(a/baa) (ab/aa) (bba/bb)     solution [2,1,2,0]:  bbaabbbaa = bbaabbbaa
```

It looks like a puzzle and it is **undecidable**, which is what makes it
useful: reducing from PCP is usually easier than reducing from halting, so it
is the standard source for undecidability proofs one step removed from the
machine model.

## Why it is undecidable

By reduction from halting. The dominoes are built so that the only way to match
is to spell out an accepting computation of a machine, configuration by
configuration. Solving the puzzle would decide halting.

That reduction produces a **modified** instance, where a designated domino must
come first. `modified_to_standard` performs the padding construction that turns
one into the other, and it is the one step of the proof that can be run rather
than described.

## The search is bounded on purpose

There is no other option. An unbounded search would be a decision procedure for
an undecidable problem, so `solve` returns None when the bound is reached, and
that is not the same as "there is no solution".

The state of the search is the **overhang**, the part one side has written that
the other has not caught up with. Two partial solutions with the same overhang
behave identically from then on, which is what keeps the search from
re-exploring.
