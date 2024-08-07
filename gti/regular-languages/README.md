# Regular languages

Eleven modules for the first block of GTI: lectures 01 to 06, exercise sheets
1 to 3.

| Folder | What it does |
|---|---|
| [regular-expressions](regular-expressions/) | syntax, derivatives, matching |
| [finite-automata](finite-automata/) | DFA and NFA, the two models |
| [thompson-construction](thompson-construction/) | expression to epsilon-NFA |
| [subset-construction](subset-construction/) | NFA to DFA, with the blow-up |
| [state-elimination](state-elimination/) | automaton back to an expression |
| [minimisation](minimisation/) | table filling and Hopcroft |
| [nerode](nerode/) | the classes the language forces |
| [closure-properties](closure-properties/) | product, complement, star, reversal |
| [pumping-lemma](pumping-lemma/) | the game, played automatically |
| [decision-algorithms](decision-algorithms/) | emptiness, finiteness, equivalence |
| [applications](applications/) | search and tokenising |

## The circle they close

```
expression --Thompson--> epsilon-NFA --subsets--> DFA --minimise--> minimal DFA
     ^                                                                    |
     +------------------------ state elimination -------------------------+
```

Every arrow is implemented, and the round trip was checked on 120 random
expressions: all four representations accept exactly the same words up to
length 4, the two minimisation algorithms agree, and the number of states of
the minimal automaton equals the Nerode index every time.

## How it was checked

- **Sheet 3, task 3.1** on Nerode classes: all four equivalences and the index
  of 5 come out as the marked solution has them.
- The 2^k blow-up of the subset construction, exactly, for k up to 5.
- Closure operations against direct word testing, 80 random language pairs and
  four operations.
- Equivalence and inclusion against brute force over all words up to length 5,
  80 pairs.
- The pumping game on `a^n b^n`, palindromes and `a^(n²)`, with a control run
  on a regular language so the game cannot "prove" everything irregular.

Two real bugs came out of those sweeps, and both are documented where they
happened: the empty-set notation stealing the digit `0`, and combining automata
over different alphabets.
