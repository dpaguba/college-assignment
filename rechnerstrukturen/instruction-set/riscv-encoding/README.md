# RISC-V instruction encoding

Every instruction is 32 bits, and the six formats differ only in where the
immediate goes.

| format | used by | immediate |
|---|---|---|
| R | `add`, `sub`, `and`, `or` | none |
| I | `addi`, `ori`, `lw` | 12 bits, sign extended |
| S | `sw` | 12 bits, split in two pieces |
| B | `bne`, `beq` | 13 bits, low bit always zero |

The splitting of the S and B immediates looks gratuitous and is not: the
register fields sit in the **same bits in every format**, so the decoder can
read them before it knows the format. The immediate is the field that can
afford to be assembled later.

Verified by round trip: every immediate from -2048 to 2047 encodes and decodes
back to itself, every mnemonic survives encoding and decoding, and an
out-of-range immediate is rejected rather than silently truncated.

A branch offset must be even, because the low bit is not stored. That is not a
restriction in practice, since instructions are aligned, and it buys one more
bit of range.

## Register names

The sheets use ABI names: `a1` is `x11`, `a3` is `x13`, `a6` is `x16`, `sp` is
`x2`. Both spellings are accepted, because the exercise mixes them.
