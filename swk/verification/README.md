# Verification

Nine modules, from propositional formulas to Hoare proofs. The verification
half of the quality lecture.

Everything here reduces to one question, **is this formula satisfiable**, and
the modules are layered around answering it.

| Folder | Role |
|---|---|
| [propositional-logic](propositional-logic/) | formulas, CNF, Tseitin, what entailment means |
| [dpll](dpll/) | the lecture's SAT algorithm, with its trace |
| [cdcl](cdcl/) | clause learning, and where it stops helping |
| [linear-arithmetic](linear-arithmetic/) | the theory solver: Fourier-Motzkin and bounded search |
| [transition-systems](transition-systems/) | the model: `<s, I, G>`, components, composition |
| [bounded-model-checking](bounded-model-checking/) | unroll k steps, find counterexamples |
| [inductive-invariants](inductive-invariants/) | prove all steps, or find out why you cannot |
| [hoare-logic](hoare-logic/) | weakest preconditions and verification conditions |
| [symbolic-execution](symbolic-execution/) | path conditions and generated tests |

## The one trick

Every question in the course is an entailment, and every entailment is tested
by looking for a model of its negation:

```
a |= b     holds exactly when     a and not b     has no model
```

k-safety is that. The inductive step is that. Each verification condition of a
Hoare proof is that. Once the trick is in place, the work moves to the solver,
which is why half of these folders are about deciding formulas rather than
about programs.

## Bounded, inductive, symbolic

Three different ways around the same wall, that the state space is infinite:

- **bounded** model checking gives up completeness and finds real bugs with
  concrete traces, fast
- **inductive** invariants give up automation and prove properties for all
  steps, if you can find the invariant
- **symbolic** execution gives up termination on loops and produces test
  inputs with proofs that they reach where they claim

The lecture teaches all three because none of them is enough alone, and
`inductive_invariants.explain` shows the two working together: bounded
checking hunts for counterexamples, induction proves the survivors.

## How it was checked

- the DPLL trace against the lecture's worked example, decision for decision
- bounded model checking against exam task 5.2, including the unrolled
  transitions the task asks to be written out and the counterexample at k = 2
- the Hoare proof of exercise 6.2 with the invariants the sheet asks for, and
  the failure with a wrong invariant
- symbolic execution against the lecture's own example, both branches with the
  path conditions on the slide
- both SAT solvers against brute force on 400 random instances each, with every
  model independently verified
