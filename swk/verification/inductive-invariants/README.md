# Inductive invariants

The proof that covers every step, not just the first k.

```
base:  I |= P
step:  P and G |= P[s'/s]
```

Two entailment checks. If both hold, P is true in every reachable state, by
induction over the length of the run, and no bound is needed anywhere.

## Why most true properties fail the step check

The step check starts from **any** state satisfying P, including states no
execution can produce. Those can step outside P.

The example in the module: `x' = x + 2` from `x = 0`, with `P = (x != 5)`.
Every reachable state is even, so P is true forever. The step check still
fails, and the tool prints why:

```
step fails: not inductive, {'x': 3, "x'": 5} satisfies it and its successor does not
```

`x = 3` is unreachable. The check does not know that, and cannot: reachability
is the thing it was supposed to establish.

## Strengthening

Find a stronger Q that implies P and is inductive. Here, adding "x is even"
does it, and `strengthen` finds that by trying candidate conjuncts.

That toy search is where the real difficulty shows. IC3 and PDR build such
strengthenings automatically, one blocked counterexample at a time, and they
are hard precisely because the search space is the space of all formulas.

## The three outcomes

`explain` separates them by running bounded model checking alongside:

| verdict | means |
|---|---|
| inductive | proved, holds in every reachable state |
| true but not inductive | no counterexample within the bound, needs strengthening |
| violated | bounded model checking found a real counterexample |

That combination is the practical workflow: bounded checking hunts for bugs,
induction proves the survivors.
