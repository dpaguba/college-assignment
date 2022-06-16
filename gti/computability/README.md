# Computability

Seven modules for the third block of GTI: lectures 12 to 16, exercise sheets 8
to 11.

| Folder | What it does |
|---|---|
| [turing-machines](turing-machines/) | the model, with a trace |
| [tm-variants](tm-variants/) | many tapes, nondeterminism, a queue |
| [goto-while-programs](goto-while-programs/) | LOOP, WHILE, GOTO and the conversions |
| [decidability](decidability/) | bounded questions, dovetailing, the diagonal |
| [reductions](reductions/) | executable many-one reductions |
| [rice-theorem](rice-theorem/) | semantic against syntactic properties |
| [post-correspondence](post-correspondence/) | the puzzle that proves things undecidable |

## The one idea

Everything in this block is the same move: **a machine is data**. Once a
machine can be written down, another machine can read it, transform it, and run
it, and then questions about machines become questions about strings.

That is what makes the halting problem possible to state, what makes reductions
possible to build, and what Rice's theorem generalises in one line.

## What can and cannot be run

Bounded questions run. Unbounded ones do not, and the modules say which is
which rather than pretending: `run` reports `limit` as a third outcome,
`semi_decide` returns `None` for "still going", `solve` for PCP stops at a
depth, and the diagonal machine of the halting proof is described and not
implemented, because its non-existence is the theorem.

## What the verification found

Four real bugs, all caught by checking against expected languages rather than
by reading the code:

- both example Turing machines accepted **too much**, because the scan phase
  had no verification pass
- the reduction put the head one cell off, so the simulated machine read its
  own input from the second symbol
- the queue automaton did not match the course's definition, which starts with
  an **empty** queue
- the Rice sample could not distinguish syntactic from semantic properties,
  which made the classifier report a state count as undecidable
