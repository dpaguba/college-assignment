# Optimisation and program analysis

Every optimisation here is an analysis plus a transformation, and the analyses
are four instances of one framework.

| Topic | |
|---|---|
| [liveness-analysis](liveness-analysis/) | which values are still needed |
| [dead-code-elimination](dead-code-elimination/) | removing what is not, repeatedly |
| [available-expressions](available-expressions/) | which computations do not need repeating |
| [constant-propagation](constant-propagation/) | which values are known at compile time |
| [loop-optimisation](loop-optimisation/) | where the work is worth moving |

## The framework

| | may (union at joins) | must (intersection at joins) |
|---|---|---|
| forwards | reaching definitions | available expressions |
| backwards | live variables | very busy expressions |

The direction says whether a fact is about the past or the future of a point;
the operator says whether it must hold on all paths or may hold on one. Getting
either wrong produces an analysis that runs, terminates, and is unsound.

Constant propagation sits slightly outside: its values form a lattice rather
than a set, so the joins take a meet rather than a union or an intersection,
and termination comes from the lattice having finite height.

## Related

The theory of the monotone framework, including why the least fixed point is
the sound one, is in
[swk/program-analysis](../../swk/program-analysis/). This block is the same
machinery applied inside a compiler, on the exercise sheets' own graphs.
