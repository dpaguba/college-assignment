# Bounded model checking

Unroll the system k steps, and ask a solver whether the property can break.

```
k-safety:  I[s0] and G(0,1) and ... and G(k-1,k)  |=  P0 and ... and Pk
test:      I[s0] and G(0,1) and ... and G(k-1,k) and (not P0 or ... or not Pk)
```

If the test has a model, that model **is** the counterexample, step by step.
If it has none, the system is k-safe and nothing is claimed beyond k.

## The algorithm

Start at k = 0. Test. On a model, stop and report. Otherwise increase k and
repeat. That is the lecture's definition, and the loop in `check`.

## What it cannot do

It never proves safety. The set of states reachable in i steps grows with i,
and there is no formula available that says when it has stopped growing, so
the search has no stopping criterion of its own. That gap is exactly what
[inductive invariants](../inductive-invariants/) fill, and why the two are
taught together.

What it is very good at is finding shallow bugs fast, with a concrete trace,
which is why it is the technique that actually shipped: CBMC and friends are
built on it.

## Verification

Exam task 5.2, in full. The system `<{s1}, s1 = 20, s1' = s1 / 2>` with
property `s1 mod 2 = 0`:

```
G(0,1): (s1@1 = (s1@0 / 2))
G(1,2): (s1@2 = (s1@1 / 2))
G(2,3): (s1@3 = (s1@2 / 2))

k=0: k-safe
k=1: k-safe
k=2: counterexample
  step 0: s1=20
  step 1: s1=10
  step 2: s1=5  <- violated here
```

The unrolled transitions match the ones the task asks to be written out, and
the counterexample is the one the halving produces.
