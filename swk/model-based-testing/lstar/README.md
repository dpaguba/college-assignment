# L*

Learning a Mealy machine from queries alone. Angluin, 1987.

The learner sees no code and no states. It asks two kinds of question:

- **membership**: run this word, what comes back?
- **equivalence**: is this hypothesis right, and if not, where does it differ?

Fill the table, close it, make it consistent, build the hypothesis, ask, and
on a counterexample refine and repeat. Each round adds at least one state and
the target has finitely many, so it terminates.

## Handling a counterexample

Two strategies are implemented:

| strategy | columns added per counterexample | queries on M1 / M3 |
|---|---|---|
| all suffixes | up to its length | 28 / 35 |
| Rivest-Schapire | exactly one, found by binary search | 21 / 21 |

Rivest-Schapire works because the hypothesis and the system agree at the start
of the counterexample and disagree at the end, so a binary search over the
split point finds the position where the prediction breaks, in log(n) queries
instead of adding n columns.

## The equivalence query is the real problem

No real system answers it. `perfect_oracle` does, and exists so the learner can
be studied against a known machine. `testing_oracle` is what reality looks
like: a finite test suite standing in for the query.

The difference is visible in the module's own output. Learning `M3` with the
weak suite `{a, b, aa, ab}` returns a **two**-state machine and reports success,
because nothing in the suite reaches the difference. The learned model is only
as good as the tests approximating the oracle, which is exactly why the
[test generation](../test-suites/) folder matters, and why practical learning
tools spend most of their time there rather than in the learner.

## Verification

`M1` and `M3` are both learned exactly, under both strategies, with the result
checked against the target by the product construction rather than by
inspection. The counterexample found while learning `M3` from a two-state
hypothesis is `abaa`, the same word the exercise asks for.
