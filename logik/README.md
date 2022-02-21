# Logik für Informatiker

Three logics, in the order the course takes them, as a library of one folder
per topic.

| Block | |
|---|---|
| [propositional-logic](propositional-logic/) | equivalence transformations, resolution, Horn formulas |
| [modal-logic](modal-logic/) | Kripke structures, equivalences, satisfiability, bisimulation |
| [predicate-logic](predicate-logic/) | structures, normal forms, Herbrand, unification, Prolog |

## The published solutions are the oracle

All six sheets come with solutions, so most modules are checked against a known
answer:

| sheet | reproduced |
|---|---|
| 1 | the ten-step NNF derivation of `!(C <-> B) \| !(!A \| B)`, each step named and model-preserving |
| 2 | the holiday entailment, refuted in 32 saturation steps against the solution's handful |
| 3 | the **whole evaluation table** of `<>(A \| []B) -> <>[]!B`, holding in worlds 2, 3 and 4 |
| 4 | bisimulation of a loop with its unwinding |
| 5 | the eight Herbrand terms with one function symbol, the expansion instances, and ground resolution |
| 6 | first-order resolution with unification, and a Prolog program answering a query |

The sheet 3 structure is drawn as a picture, so the accessibility relation was
**reconstructed from the published table**: nine rows constrain it enough to pin
it down to `1 -> {1,3}`, `2 -> {}`, `3 -> {2}`, `4 -> {4}`, and every row then
matches.

## Three findings

**A dead end satisfies every box.** World 2 of the sheet's structure has no
successors, so `[]phi` is vacuously true and `<>phi` false there for every
`phi`. That single fact is why the formula holds in world 2, and it is the whole
point of the exercise.

**The naming convention had teeth.** Variables were recognised as single
letters, so the renaming that resolution performs before every step turned every
variable into a constant and every unification after the first rename failed.
All the tests passed, because they all used unrenamed terms.

**Skolemisation is not an equivalence.** `same_models` now refuses formulas with
function symbols rather than trying to compare a formula with its Skolem form,
because that comparison is the wrong question and would have quietly answered
it.

## Deliberate overlap

Propositional CNF, Tseitin, DPLL and CDCL are in
[swk/verification](../swk/verification/); regular and context-free machinery is
in [gti](../gti/). Neither is repeated. What this subject adds is the
proof-producing resolution, the Horn fragment, all of modal logic, and all of
predicate logic.
