# Modal logic

| Topic | |
|---|---|
| [kripke-structures](kripke-structures/) | worlds, accessibility, and evaluating a formula at a world |
| [modal-equivalences](modal-equivalences/) | the dualities, and the two distributions that fail |
| [modal-satisfiability](modal-satisfiability/) | deciding satisfiability, and the finite model property |
| [bisimulation](bisimulation/) | when no modal formula can tell two worlds apart |

## Why this block is entirely new

Propositional and first-order logic appear elsewhere in this repository, in
[swk/verification](../../swk/verification/) and
[gti](../../gti/). Modal logic does not appear anywhere else, and it is the
part of this course with the most direct use: a Kripke structure **is** a
transition system, `[]` is "on all paths from here", and the correspondence
between axioms and frame properties is how a specification language chooses
what its transitions may do.
