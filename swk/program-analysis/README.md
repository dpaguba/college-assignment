# Program analysis

Ten modules built on one tiny language. Lecture SWK-4 and the analysis half of
the quality lecture.

Everything here answers questions about a program **without running it**, which
is what static analysis means, and every one of them is an approximation:
the exact questions are undecidable, so each analysis errs deliberately in the
direction that is safe for its purpose.

## The chain

| Folder | What it produces |
|---|---|
| [while-language](while-language/) | syntax, labels, `init`, `final`, `flow` |
| [control-flow-graph](control-flow-graph/) | the graph the analyses run on |
| [cyclomatic-complexity](cyclomatic-complexity/) | `CC = e - n + 2p` |
| [operational-semantics](operational-semantics/) | what the program does, rule by rule |
| [monotone-framework](monotone-framework/) | one worklist algorithm |
| [reaching-definitions](reaching-definitions/) | forward, may |
| [live-variables](live-variables/) | backward, may |
| [available-expressions](available-expressions/) | forward, must |
| [very-busy-expressions](very-busy-expressions/) | backward, must |
| [ast-analysis](ast-analysis/) | rules over the syntax tree |

Each folder imports the ones above it. Nothing imports downwards.

## The two-by-two square

The four classical dataflow analyses are the same algorithm with two switches
flipped:

| | may (union) | must (intersection) |
|---|---|---|
| **forward** | reaching definitions | available expressions |
| **backward** | live variables | very busy expressions |

Writing the framework once and instantiating it four times is the point.

## Three representations, three kinds of question

The lecture is explicit that analysis happens on one of three things, and the
folders follow it:

- the **syntax tree**: naming, shape, patterns. Cheap and blind to execution
- the **control flow graph**: reachability, complexity, dataflow. Sees paths,
  ignores values
- the **semantics**: operational rules and symbolic execution. Sees values, at
  the price of not terminating in general

## How it was checked

Every result that the course publishes an answer for was reproduced:

- `flow` and the CFG of the lecture's example, edge for edge
- `CC = 2` on that example
- the operational semantics trace, against the derivation on the slides
- reaching definitions on exercise sheet 6, all six rows of the marked
  solution, including the back edge that the drawing leaves ambiguous
- available and very busy expressions against the textbook tables in Nielson,
  Nielson and Hankin
