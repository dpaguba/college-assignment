# Lexical analysis

The first phase of a compiler is a decision procedure: given the next
characters, which token is this. The specification is a list of regular
expressions and the implementation is a table-driven automaton.

| Topic | Question |
|---|---|
| [regex-to-dfa](regex-to-dfa/) | how a specification becomes an automaton |
| [maximum-munch](maximum-munch/) | which token wins when several match |
| [lexer-generator](lexer-generator/) | how a generator merges the rules into one table |

The path is entirely mechanical, which is the point: a scanner is generated,
not written, and the interesting decisions are all in the two tie-breaking
rules rather than in the automaton theory.
