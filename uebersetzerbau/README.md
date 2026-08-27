# Übersetzerbau

A compiler as a library: one folder per topic, an implementation and a README
each. The five blocks are the phases, in the order a program passes through
them.

| Block | |
|---|---|
| [lexical-analysis](lexical-analysis/) | characters to tokens |
| [parsing](parsing/) | tokens to a tree |
| [semantic-analysis](semantic-analysis/) | what the tree means, and whether it means anything |
| [code-generation](code-generation/) | tree to instructions |
| [optimisation](optimisation/) | instructions to better instructions |

## The published solutions are the oracle

Unusually, every exercise sheet comes with a full solution, so most modules are
checked against a known answer rather than against a second implementation.
What is reproduced:

| sheet | reproduced |
|---|---|
| 1.1 | three regular expressions, plus the two near-miss variants the solution explains: `1(0\|1)*10` misses the number 2, `(b\|abb?)*` wrongly accepts `abbb` |
| 1.2 | `(a+\|b).c*` becomes 14 NFA states, 5 DFA states, **3** after minimisation |
| 1.3 | `011001011001001` scans as **T3(0110), T1(0101), T3(10), T1(01001)**, with the priority decision at position 4 |
| 2.1 | the unique parse tree of `(id+id+id)*id`, and both derivations, 15 sentential forms each |
| 3.1 | both First and Follow computations and both LL(1) tables, and the 18-step parse of `aabcbrbr` |
| 4.1 | the LR(1) automaton with **10** states, LALR with **6**, four merged pairs, no reduce-reduce conflict, and the 11-configuration parse of `abacb` |
| 4.2 | the attribute grammar for `a^n b^n a^n`, giving counts 2, 2, 2 on `aabbaa` |
| 5.2 | `B x; if (x == null) x = (B)this;` type-checks in class `C` and throws `ClassCastException` at run time |
| 5.3 | the do-while scheme with one conditional jump and no others, and the address of `a[3,5]` at **1260** |
| 6.2 | only `x = a+b` is dead, then only `a = 1`, and the wrong transfer function loses `y` at node 5 |

## Four defects the tests found

| defect | how it surfaced |
|---|---|
| naive top-down parse-tree enumeration | did not terminate on `E ::= E + T`, replaced by a chart over spans |
| epsilon marker written as ASCII `e` | collided with the terminal `e` in the dangling-else grammar |
| back edges detected by reachability | reported 4 loops instead of 1 on a graph with a straight-line prefix |
| the type checker declaring into its own scope | checking the same fragment twice raised a redeclaration error, and every test used a fresh checker so all sixteen passed |

The third and fourth are the interesting ones: both were wrong in a way that
made every test written against them pass.

## Deliberate overlap with other subjects

Thompson's construction, the subset construction and minimisation are proved in
[gti/regular-languages](../gti/regular-languages/); the monotone dataflow
framework is in [swk/program-analysis](../swk/program-analysis/). Neither is
repeated here. What this subject adds is the compiler-specific part: the
scanner's tie-breaking rules, the parse tables and their conflicts, and the
analyses applied to the exercise sheets' own control flow graphs.
