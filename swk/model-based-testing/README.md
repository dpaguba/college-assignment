# Model-based testing

Four modules: the model, the table, the learner, the tests. Exercise sheet 5
in full.

| Folder | Role |
|---|---|
| [mealy-machines](mealy-machines/) | the model, equivalence, minimisation |
| [observation-table](observation-table/) | what a learner knows |
| [lstar](lstar/) | learning a model from queries |
| [test-suites](test-suites/) | generating tests from a model, and the oracle |

## The circle these four form

A model gives you tests and an oracle. A learner gives you a model from a
system you cannot read. But the learner needs an equivalence oracle, and the
only way to build one for a real system is a **test suite**. So the tests come
from the model, and the model comes from the tests.

That circle is not a flaw in the presentation, it is the actual state of the
field: automata learning in practice is a loop between a learner and a
conformance test suite, and the guarantee you get at the end is the guarantee
the suite was able to give.

The module shows it directly. Learning `M3` with the weak suite
`{a, b, aa, ab}` returns a two-state machine and reports success. The real
machine has three states.

## The exercise, reproduced

Every published answer of sheet 5 comes out:

| Task | Answer | Reproduced |
|---|---|---|
| 5.1a | switch cover from access sequences | the same 12 words |
| 5.1b | how many transition pairs | 12 |
| 5.2a | expected output for `abba` | `0010`, claim rejected |
| 5.2b | expected output for `baab` | `1000`, claim rejected |
| 5.3 | close the table, build the hypothesis | two states, and why that is wrong |
| 5.4a | shortest counterexample for H against M3 | `abaa` |
| 5.4b | extend the table and reclose | L\* does it and reaches M3 |
