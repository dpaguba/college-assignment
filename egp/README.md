# Elektronische Geschäftsprozesse

The name is misleading: this is a course on concurrency theory. Four parts
across thirteen lectures, of which the middle two are the substance.

| Block | Modules | What it holds |
|---|---:|---|
| [ccs](ccs/) | 5 | the calculus, its semantics, graphs, bisimulation |
| [pi-calculus](pi-calculus/) | 4 | names that travel, reduction, data, actors |
| [actors](actors/) | 4 | the model, two exercises, what it guarantees |
| [petri](petri/) | 3 | nets as triples, condition/event nets, reachability |
| [concurrency](concurrency/) | 2 | interleavings and the classical problems |

Petri nets are covered at length in `mnp`, BPMN in `bpm`, transactions and
serialisability in `is`. The weight here therefore sits where those do not
reach: CCS, bisimulation, the π-calculus and the actor model, which are also
lectures 4 to 10 out of 13.

## Ground truth

Exercise sheet 4 comes with a worked solution, and the CCS engine reproduces
all five of its τ-chains exactly:

| Term | Chain |
|---|---|
| a.b.0 \| ā.0 | → b.0 |
| a.0 \| b̄.0 \| b.ā.0 | → a.0 \| ā.0 → 0 |
| (a.b.0 + b.ā.0) \| ā.a.0 | → b.0 \| a.0, then stuck |
| A⟨a⟩ \| A⟨b⟩ \| ā.b̄.b̄.ā.0 | four steps → A⟨a⟩ \| A⟨b⟩ |
| ((νa)a.b.0 + c.0) \| (ā.0 + b̄.0 + c̄.0) | → 0 |

## Two findings

**The obvious answer to exercise 6b is wrong.** Asked for a process without
parallelism behaving like `a.0 | b.0 | c.0`, the natural answer is the sum of
the six orderings. It has the same traces and is not bisimilar: after the
first `a` the parallel composition still offers both `b` and `c`, while the
flat sum has already committed to one. The correct answer nests the choices,
`a.(b.c.0 + c.b.0) + b.(a.c.0 + c.a.0) + c.(a.b.0 + b.a.0)`, and that one is
bisimilar. It is the same mistake as `a.b.0 + a.c.0` against `a.(b.0 + c.0)`,
one level up.

**Scope extrusion has a side condition, and forgetting it changes the
answer.** Pulling `(νx)` outward over a parallel composition is only sound
when `x` is not free in the parts it is pulled over. Without the check,
`(νx)x̄⟨z⟩.0 | x(y).0` reacts, which is exactly what the restriction exists to
prevent. With it, the bound name is renamed first and the two sides stay
apart. The list encoding of exercise 9 needs the extrusion to work at all,
and the restriction example needs it not to fire, so both cases are tested.
