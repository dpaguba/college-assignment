# Decidable and semi-decidable

```
decidable        some machine always halts with yes or no
semi-decidable   some machine says yes on the language and may loop otherwise
```

The halting problem sits in the gap: semi-decidable, because running and
waiting says yes when the answer is yes, and not decidable, because no machine
can always say no.

## What is implemented and what cannot be

The **bounded** questions are decidable and trivially so: `halts_within` runs
the machine that many steps and looks. The unbounded one is the whole
difficulty, and the difference between them is one parameter.

`semi_decide` returns True or never returns, approximated here by a budget and
a `None`. That `None` is the accurate representation of "still running", and it
is what a real semi-decision procedure would do for ever.

The diagonal machine D of the halting proof is **not** implemented, because it
cannot be: the contradiction is the proof that it does not exist.
`diagonal_argument` shows the shape of the argument on a finite list of
deciders, where the diagonal really can be built and really does disagree with
every one of them.

## Dovetailing

`enumerate_language` runs every word a little, then a little more, instead of
running each to completion. Running to completion would hang on the first word
the machine loops on, and every later word would never be reached.

That construction is exactly why semi-decidable and recursively enumerable are
the same class.

## The two-sided theorem

`decide_by_both` runs a machine and one for the complement in parallel and
stops when either accepts. One of them must, so it always halts. Four lines,
and it is the proof that a language is decidable exactly when it and its
complement are both semi-decidable.
