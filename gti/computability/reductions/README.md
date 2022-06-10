# Reductions

```
A <=m B     when a computable f exists with   x in A  <=>  f(x) in B
```

If A reduces to B and B were decidable, A would be too. So a reduction **from**
a known undecidable problem proves the new one undecidable, and every result
after the halting problem is obtained this way.

## The direction

To show B is hard, reduce the hard problem **to** B. Reducing B to A shows
nothing about B. That is the error the exercises are built to catch, and the
`verify` function here catches it too: a reversed reduction fails on the first
sample where the two answers differ.

## Executable, not described

`prefix_writer` builds a real machine that writes a fixed word and then behaves
like a given one. It is the workhorse: "hard-code the input into the machine"
is a transformation of machines, and with it the two standard reductions run
and can be checked.

| From | To | By |
|---|---|---|
| HALT | accepts the empty word | hard-code w, ignore the input |
| HALT | language is non-empty | the same machine, which accepts all or nothing |

## What the sample check found

The first version put the head on cell **1** after writing the word, because
the handover moved right once too often. The simulated machine then read its
own input starting from the second symbol, which accepted some words and
rejected others, so the reduction looked plausible and was broken.

Four of five samples disagreed, and the fix was one direction constant. That is
the argument for verifying reductions on instances where both sides are known,
even though the general claim is unverifiable by construction.
