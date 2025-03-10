# Control flow graph

The graph the analyses run on: nodes are labels, edges are `flow`.

```
entry: 1, exits: [6]
  [y := x]1 -> [2]
  [z := 1]2 -> [3]
  [(y > 1)]3 -> [4, 6]
  [z := (x * y)]4 -> [5]
  [y := (y - 1)]5 -> [3]
  [y := 0]6 -> exit
```

## What it adds over the flow relation

Predecessors and successors in both directions, reachability, connected
components, and a Graphviz export. None of it is deep; all of it is needed by
something downstream.

**Reachability** is the first real analysis: a label the entry cannot reach is
dead code. Note what it does *not* do. `if [false]2 then ... else ...` still
has edges into both branches, because `flow` is syntactic and never evaluates
a condition. Catching that needs the constant-condition rule in
[ast-analysis](../ast-analysis/), and catching the general case needs
something that reasons about values.

**Components** is the `p` of the cyclomatic complexity formula. A single While
program always has one; the count matters when several procedures are measured
as one graph.

## Graphs without a program

`ControlFlowGraph.from_parts` builds a graph from blocks and edges directly.
The exercise sheets sometimes draw a CFG with no program attached, and the
analyses run on the graph, so they do not care which of the two it came from.
That constructor is what let the reaching definitions folder reproduce the
graded solution of exercise sheet 6.
