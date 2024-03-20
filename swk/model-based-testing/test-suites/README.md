# Test generation from a model

A model gives two things: inputs worth running, and a prediction for each.
The prediction is what makes the tests automatic; without a model, someone has
to say what the right answer is.

## The covers, weakest first

| Cover | Idea | Size on M1 |
|---|---|---|
| state | reach every state | 3 |
| transition | take every transition | 6 |
| transition-switch | take every executable **pair** of transitions | 12 |
| W-method | transition cover + distinguishing set | 10 |

**Transition-switch** is the exercise's cover. A pair is `(state, first
symbol, second symbol)`, so a machine with n states over k symbols has exactly
n·k·k of them: for `M1`, 3 · 2 · 2 = **12**, which is the answer sheet 5 asks
for. The suite is built from access sequences, `access(q) + x + y`, giving

```
{aa, ab, ba, bb} u {aaa, aab, aba, abb} u {baa, bab, bba, bbb}
```

which is the marked solution's suite, and `covered_pairs` confirms all 12
pairs are executed.

## The W-method is the only complete one

Transition cover followed by a distinguishing set is complete **under an
assumption**: that the implementation has no more states than the model, plus
however many extra states are allowed for. Under that assumption, passing the
suite proves equivalence, which is a rare thing for a finite suite to claim.

The size is the price. Allowing extra states multiplies the suite by the
alphabet raised to that power, which is why the assumption is kept small in
practice.

## Oracles

`oracle` compares one run against the model's prediction. Sheet 5's task is
exactly that: the system claims `1010` for `abba`, the model says `0010`, so
the claim is rejected. Both claims in the exercise are rejected, with the
expected outputs the solution gives.

## What a stronger cover buys

Against a machine with one broken transition, the switch cover catches it with
2 failing tests and the W-method with 4 out of 10. Both catch it; the point is
that neither is guaranteed to unless the fault model matches the assumption
the suite was built under.
