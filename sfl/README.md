# SFL

Thirty-two modules across eight blocks, following the eleven lectures and the
seven exercise sheets of the course.

This is the best-supplied subject in the whole collection: every sheet came
with its solution, and the exam came with answers. Where a published answer
exists it is reproduced rather than approximated.

## The published answers, reproduced

| exercise | answer |
|---|---|
| 1.2 | the parliament listing, and the set-user-id bit on `omicron.sh` |
| 1.3b | the Bell-LaPadula and Biba table, line for line |
| 1.3c | together the models permit nothing between levels, measured as zero |
| 2.1a | `cmp eax, ebx` with 0 and 1234: je and jz not taken, jb and jl taken |
| 2.1b | after the mask sequence: CF = 0, ZF = 1, SF = 1, OF = 0 |
| 2.2 | the instruction pointer at 2, 7, 3 and 1234 |
| 3.1 | two positive numbers whose 32-bit sum is negative |
| 3.3c | the check passed by overwriting the flag beside the buffer |
| 5.1 | key 13, and Kerckhoffs's principle as the plaintext |
| 5.2 | Shannon, *A Mathematical Theory of Communication* |
| 5.3c | 16 bits passed, 14 failed; the length is what leaks |
| 6.1 | the third identity holds only for coprime a, with a counterexample |
| 6.2a | d = 37 |
| 6.2b | p + q = n + 1 − φ(n), then a quadratic |
| 6.3a | the three candidate hash functions rated |
| 7.1 | both firewall rule sets, executed against packets |

## Where the answer came out sharper than expected

Exercise 6.3d asks whether a hash with a deterministic inverse can still
resist collisions. It cannot, and the birthday bound is not the reason:
hashing any message and asking the inverse for a preimage yields a collision
in two evaluations, because a 512-bit input space mapped onto 160 bits gives
every hash about 2³⁵² preimages.

## What the block on exercise 4 is not doing

Exercise 4 covers SQL injection, cross-site request forgery and cross-site
scripting. Those are implemented in `wt2/security/`, against a real sqlite3
database and the standard library's HTML parser, including the numeric
parameter case this sheet asks about, where there are no quotes to escape.
They are not duplicated here.
