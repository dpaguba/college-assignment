# Softwarekonstruktion

The course worked through as running code. 33 modules in five topics, in
plain Python with no dependencies.

| Topic | Modules | What it covers |
|---|---|---|
| [program-analysis](program-analysis/) | 10 | the While language, control flow, dataflow, semantics |
| [verification](verification/) | 9 | SAT, SMT-style arithmetic, model checking, Hoare logic |
| [model-based-testing](model-based-testing/) | 4 | Mealy machines, L\*, conformance testing |
| [metrics](metrics/) | 5 | LCOM, coupling, size, coding standards |
| [estimation](estimation/) | 5 | PERT, velocity, planning poker, GQM, A/B tests |

Four semesters of material sit behind this: ss22, ws23-24, ws24-25 and
ws25-26. The lecture reorganised itself between them, and the formal content
is the part that stayed.

## What ties it together

One language, one graph, one question.

The **While language** is defined once and everything analyses it: the control
flow graph comes from its `flow` relation, the dataflow analyses run on that
graph, the operational semantics executes it, symbolic execution executes it on
symbols, and the Hoare rules prove things about it.

The **question** is always satisfiability. Entailment, k-safety, the inductive
step and every verification condition are the same check with different
formulas, which is why the SAT solver and the arithmetic solver sit under
everything else.

## How it was verified

The sheets and exams publish worked solutions, so most of this has a graded
answer to check against, and every one of them was reproduced:

- the control flow graph and `CC = 2` of the lecture's example
- reaching definitions on exercise sheet 6, all six rows, including a back
  edge the picture leaves ambiguous and the solution settles
- the DPLL trace, decision for decision
- exam task 5.2 on bounded model checking, unrolled transitions and
  counterexample
- the Hoare proof of exercise 6.2 with the sheet's invariants
- every answer of sheet 5 on Mealy machines and observation tables
- all three LCOM values from the lecture and sheet 2: 2/3, 0 and 4/7
- the game project estimate of sheet 2, 248 hours by two points and 250 by three

Where the course publishes no answer, an independent one was computed:
available and very busy expressions against the tables in Nielson, Nielson and
Hankin, both SAT solvers against brute force, and the learned automata against
their targets by the product construction.

## What is deliberately limited

Arithmetic is decided over **bounded** integer domains, or exactly over the
rationals by Fourier-Motzkin. Neither is a decision procedure for integer
arithmetic, and none can be once multiplication of variables is allowed. The
bounds are where that difficulty is parked, and every module that relies on
them says so.

## What is left

Architecture (ADD, views, SOLID) and the process models (V-model, Scrum,
CMMI). Both are methods rather than algorithms, so they belong in the lecture
notes rather than in code, and that is where they went: [tex/](tex/) holds
the written summary.
