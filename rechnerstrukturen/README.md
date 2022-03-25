# Rechnerstrukturen

Sixteen modules in five blocks, from a bit to an instruction.

| Block | |
|---|---|
| [data-representation](data-representation/) | integers, floats, text |
| [boolean-functions](boolean-functions/) | normal forms, minimisation, OBDDs |
| [combinational-circuits](combinational-circuits/) | gates, adders, multipliers, hazards |
| [sequential-circuits](sequential-circuits/) | flip-flops, automata, memory |
| [instruction-set](instruction-set/) | RISC-V encoding, assembly, datapath |

## Checked against the sheets

| sheet | reproduced |
|---|---|
| 2.1 | `(101)` in four representations, and `01011010` read back as 90, 90, 90 and -37 |
| 5.1 | the Quine-McCluskey primes of the five-variable function: three of them, of which two are essential |
| 8.1 | why `R = S = 1` is forbidden, statically and as a race |
| 11.1 | the assembly program in register transfer notation, executed |

## Three results that came out the other way round

**The sheet's function has three prime implicants, not two.** `b c d e` is
genuinely prime and genuinely redundant, which is exactly the distinction the
PI table exists to make.

**A multicycle machine is not automatically faster.** With the textbook stage
times it takes 810 units against the single-cycle machine's 800, and it gets
worse, not better, when one stage dominates. Its argument is hardware reuse.

**Booth's algorithm needs no correction term.** The recoding digits telescope
into the two's complement value of the multiplier, so signed operands work for
free rather than as an extra case, verified over every pair in `-8..7`.

## Relationship to Rechnerarchitektur

[rechnerarchitektur](../rechnerarchitektur/) starts where this course stops.
Caches, pipelines and dynamic scheduling are there; bits, gates, flip-flops and
instruction encoding are here. The datapath module is the seam: it is the last
thing this course builds and the first thing that one takes apart.
