# The flags register

Four flags matter for control flow: carry at bit 0, zero at bit 6, sign at
bit 7, overflow at bit 11. Carry belongs to unsigned arithmetic and is set
when a subtraction had to borrow; overflow belongs to signed arithmetic and is
set when the result no longer fits.

A comparison is a subtraction that throws its result away and keeps the flags,
which is why `je` and `jz` are the same instruction under two names.

## Exercise 2.1a

`cmp eax, ebx` with eax = 0 and ebx = 1234 gives

| flag | value |
|---|---|
| ZF | 0 |
| CF | 1 |
| SF | 1 |
| OF | 0 |

so `je` and `jz` are not taken, `jb` is taken because the carry flag is set,
and `jl` is taken because the sign and overflow flags differ. Both jumps are
taken here, for different reasons and by reading different flags. Choosing
the wrong pair is the classic bug, and it only shows up once negative values
or very large unsigned values appear.

## Exercise 2.1b

`pushf`, `pop ax`, then `and 0xFFFE` clears bit 0, `or 0x00C0` sets bits 6
and 7, `and 0xF7FF` clears bit 11, then `push ax` and `popf`. Afterwards:
**CF = 0, ZF = 1, SF = 1, OF = 0**, which the module computes from the mask
operations rather than from the answer.

The verified values match the published solution.
