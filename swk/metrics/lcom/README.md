# LCOM

Lack of cohesion in methods: how loosely a class holds together.

```
LCOM = ((1/a) * sum of n(Ai) - m) / (1 - m)
```

for a class with `a` fields and `m` methods, where `n(Ai)` counts the methods
touching field `Ai`. The value runs from 0 to 1.

## The three published examples, reproduced

| Class | Computed | Source |
|---|---|---|
| exercise sheet 2 | **2/3** | the marked solution says 2/3 |
| Dreieck | **0** | the lecture slide |
| Figur (triangle + circle merged) | **4/7** | the lecture slide |

Zero means every method uses every field. The merged class scores 4/7 because
half its methods never touch the other half's data, which is the lecture's way
of showing that gluing two classes together is visible in the number.

## What it actually measures

Cohesion is inferred from **shared data access**. That is a proxy: two methods
touching the same field probably belong together, and two methods that share
nothing probably do not. It says nothing about whether the responsibilities
make sense, only about whether the data is shared.

## Three other variants, and why LCOM4 is the useful one

| Variant | Definition | Problem |
|---|---|---|
| LCOM1 | pairs of methods sharing no field | unbounded, grows with class size |
| LCOM2 | disjoint pairs minus sharing pairs | collapses to 0 for most classes |
| the lecture's | normalised to [0, 1] | comparable, but not actionable |
| LCOM4 | connected components of the method graph | says what to extract |

LCOM4 is the one worth acting on: it counts the independent groups of methods,
so a class scoring 3 is three classes waiting to be split, and `components`
names which methods go where.

Running it on this repository's own data structures shows the effect: `BTree`
scores 7 components, because search, insert, delete and traversal touch
different parts of the node representation. That is not necessarily wrong for a
data structure, which is the caveat that applies to every metric here.
