# Finite automata

DFA and NFA, the two models the whole first block moves between.

A DFA has exactly one choice per step. An NFA may have several or none, and may
take epsilon steps that read nothing. Both accept exactly the regular
languages, which is the first real theorem of the course.

## Partial automata and the trap

The DFA here is allowed to be **partial**: a missing transition means the run
gets stuck and the word is rejected. That is convenient and it is a trap in two
places, both of which cost a correctness bug if forgotten:

- **complement**: swapping the accepting states of a partial automaton does not
  turn the stuck words into accepted ones, so the complement loses exactly the
  words with no run. `complete` adds the trap state first.
- **combining two automata**: an automaton that has never seen the symbol `b`
  has no transition for it, so a product with another automaton over `{a, b}`
  gets stuck instead of rejecting.

The second one is not hypothetical. It was found here by a random cross-check
comparing the product construction against direct word testing: 249
disagreements, all on pairs of languages over different alphabets. `with_alphabet`
is the fix, and every operation in [closure-properties](../closure-properties/)
now calls it.

## The epsilon closure

The one operation that makes epsilon transitions harmless. A set of NFA states
is always kept closed under epsilon steps, so everything else can pretend they
do not exist. It is why the subset construction needs no special case for them.

## Enumeration order

`language(max_length)` returns words in shortlex order: shortest first,
alphabetical within a length. The regular expression module returns the same
order for the same reason, so two results can be compared directly rather than
as sets.
