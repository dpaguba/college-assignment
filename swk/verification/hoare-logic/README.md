# Hoare logic

Proving what a program computes, by working backwards from what should hold at
the end.

A triple `{P} S {Q}` claims: if P holds and S terminates, Q holds afterwards.
**Partial** correctness, since the loop rule says nothing about termination.

```
{Q} skip {Q}
{Q[a/x]} x := a {Q}
{P} S1 {R}, {R} S2 {Q}                    =>  {P} S1;S2 {Q}
{P and b} S1 {Q}, {P and not b} S2 {Q}    =>  {P} if b then S1 else S2 {Q}
{I and b} S {I}                           =>  {I} while b do S {I and not b}
```

## The assignment rule runs backwards

To know what must hold before `x := a` so that Q holds after, substitute `a`
for `x` in Q. Forwards it would be a guess; backwards it is an equality, and
that is why weakest preconditions are computed from the postcondition rather
than the other way round.

## The loop is the only place with real work

Every other rule is mechanical, and `weakest_precondition` computes them
without help. A loop needs an **invariant**, which no rule provides, and
supplying it leaves two obligations behind:

- the body preserves it: `I and b -> wp(body, I)`
- leaving the loop gives the postcondition: `I and not b -> Q`

Finding invariants is the part that does not automate away, and it is why
tools like Dafny and Why3 ask the programmer to write them.

## Verification conditions

`verify` collects `P -> wp(S, Q)` plus the loop obligations and discharges
each one with the [bounded arithmetic solver](../linear-arithmetic/). That is
exactly the architecture of a modern verifier: a front end that generates
conditions, a solver that decides them.

## Verification

Exercise 6.2 from sheet 6:

```
{ true }
if (a >= b) { while (a != b) a := a - 1 }
else        { while (a != b) a := a + 1 }
{ a = b }
```

With the invariants `a >= b` and `a <= b`, all five conditions hold. With a
wrong invariant, `a > b`, the tool fails two of them and prints the states
that break them, which is the useful half of a failed proof.

The bounds are the real limitation: conditions are checked over a finite
range of integers, so this is a check, not a proof. The failures it reports are
real; the successes are real only inside the range.
