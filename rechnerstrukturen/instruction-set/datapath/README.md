# The datapath

Every instruction takes the same five steps through the same hardware. What
differs is which steps do anything, and that is what the control signals say.

| instruction | reads memory | writes memory | writes a register | ALU second input |
|---|---|---|---|---|
| `add` | no | no | yes | register |
| `addi` | no | no | yes | immediate |
| `lw` | **yes** | no | yes | immediate |
| `sw` | no | **yes** | no | immediate |
| `bne` | no | no | no | register |

The ALU is the only place arithmetic happens, which is why a load and an add
share a datapath: `lw a3, 4(a0)` is an addition whose result is used as an
address. A branch is a subtraction whose zero flag is read instead of stored,
which is why comparisons against zero are the cheapest ones an instruction set
can offer.

## Single cycle against multicycle, measured

With a mix of 25% loads, 10% stores, 45% arithmetic and 20% branches the CPI is
4.05, and the comparison goes the opposite way from the intuitive one:

| stage times | single cycle | multicycle |
|---|---|---|
| 200, 100, 200, 200, 100 | 800 | 810 |
| 200 each | 1000 | **810** |
| 200, 100, 200, **800**, 100 | 1400 | 3240 |

The multicycle machine's period is the **longest** stage, so an unbalanced
pipeline hurts it: the single-cycle machine pays for a long stage once per
instruction and the multicycle machine pays for it every cycle.

It wins when the stages are balanced and the mix skips some of them, and its
real argument was never speed but hardware reuse: one ALU and one memory port
instead of several.
