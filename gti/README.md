# GTI: Grundbegriffe der Theoretischen Informatik

The whole course as running code. 32 modules in four blocks, plain Python, no
dependencies.

| Block | Modules | Lectures | Sheets |
|---|---|---|---|
| [regular-languages](regular-languages/) | 11 | 01 to 06 | 1 to 3 |
| [context-free](context-free/) | 10 | 07 to 11 | 4 to 7 |
| [computability](computability/) | 7 | 12 to 16 | 8 to 11 |
| [complexity](complexity/) | 4 | 17 to 20 | 12 |

## The staircase

Each block adds one thing and pays for it.

| Level | Machine | Can decide | Cost of membership | Closed under |
|---|---|---|---|---|
| regular | finite control | `a*b*` | linear | everything |
| context-free | + a stack | `a^n b^n` | cubic | not intersection, not complement |
| decidable | + a tape | `a^n b^n c^n` | unbounded | complement, not much else |
| semi-decidable | the same, without halting | halting itself | never | not complement |

The two languages in the third column are the whole argument: `a^n b^n`
separates the first level from the second, `a^n b^n c^n` separates the second
from the third, and both are implemented at every level where they belong.

## Verified against the published solutions

Sheet solutions exist for all twelve exercise sheets, which made this the most
checkable subject of the three done so far.

- **Sheet 3, Nerode**: all four word equivalences and the index of 5
- **Sheet 5, Chomsky normal form**: all three parts, every intermediate grammar
  rule for rule, including the generating, reachable and nullable sets
- **Sheet 7, LL(1)**: all three verdicts, every FIRST and FOLLOW set, and the
  FIRST sets of the right-hand sides
- **Sheet 10, queue automata**: the model implemented as the sheet defines it,
  empty queue and epsilon reads included

Where no solution is published the checks are structural, and there are a lot
of them: the four representations of a regular language agree on 120 random
expressions, the closure operations agree with direct word testing on 80
language pairs, the two minimisation algorithms agree on every automaton, every
NP reduction preserves yes-instances and transports certificates, and the
Cook-Levin formula agrees with the machine it encodes.

## Seven real bugs, all found by verification

Not one of them was found by reading the code:

1. `0` as the empty set stole the digit from the alphabet, so `(0|1)+` silently
   became `1+`
2. combining automata over different alphabets got stuck instead of rejecting,
   249 disagreements in one sweep
3. minimisation dropped the trap state, so the Nerode index came out 2 instead
   of 5
4. both example Turing machines accepted too much, for want of a verification
   phase
5. the reduction left the head one cell off, so the simulated machine read its
   own input from the second symbol
6. the Rice sample could not separate syntactic from semantic properties
7. the Cook-Levin check never returned, because brute force SAT on 265
   variables is 10^79 assignments

Each is documented in the README of the folder where it happened.
