# Context-free languages

Ten modules for the second block of GTI: lectures 07 to 11, exercise sheets 4
to 7.

| Folder | What it does |
|---|---|
| [context-free-grammars](context-free-grammars/) | rules, derivations, ambiguity |
| [grammar-cleanup](grammar-cleanup/) | useless variables, epsilon and unit rules |
| [chomsky-normal-form](chomsky-normal-form/) | the five steps CNF1 to CNF5 |
| [greibach-normal-form](greibach-normal-form/) | every rule starts with a terminal |
| [pushdown-automata](pushdown-automata/) | the model, both acceptance modes |
| [cfg-pda-conversion](cfg-pda-conversion/) | grammars and automata, both directions |
| [cyk](cyk/) | the word problem, cubic |
| [ll1-parsing](ll1-parsing/) | FIRST, FOLLOW, table, conflicts |
| [cfl-pumping-lemma](cfl-pumping-lemma/) | the game with four cut points |
| [cfl-closure](cfl-closure/) | what survives, and the counterexample |

## What changes from the regular level

**More power**: a rule can recurse with symbols on both sides, so `a^n b^n` is
expressible. **Less determinism**: deterministic pushdown automata are strictly
weaker than nondeterministic ones. **Less closure**: intersection and
complement are gone. **More cost**: membership is cubic instead of linear, and
equivalence becomes undecidable, which is why this block has no counterpart to
the first block's decision algorithms folder.

## Verified against the marked solutions

- **Sheet 5, CNF**: all three parts, every intermediate grammar rule for rule,
  including the generating and reachable sets and the nullable set
- **Sheet 7, LL(1)**: all three verdicts and every FIRST and FOLLOW set,
  including the FIRST sets of the right-hand sides

Where the sheets publish no numbers, the checks are structural: Greibach and
Chomsky conversions preserve the language through CYK, the grammar-automaton
round trip preserves it in both directions, and the pumping games run with a
control on a language that does pump.
