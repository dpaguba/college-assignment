# RISC-V assembly and transfer notation

The exercise asks for each instruction's effect in register transfer notation,
`Reg[13] := Reg[14] + Reg[15]`, which is exactly what the machine does in one
step. Producing the notation and executing the instruction from the same parsed
form keeps the two descriptions from drifting apart.

| instruction | notation |
|---|---|
| `ori a1, x0, 30` | `Reg[11] := Reg[0] \| 30` |
| `add a1, a2, a3` | `Reg[11] := Reg[12] + Reg[13]` |
| `lw a3, 4(a0)` | `Reg[13] := Mem[Reg[10] + 4]` |
| `sw a1, 8(a0)` | `Mem[Reg[10] + 8] := Reg[11]` |

## Register zero is hardware, not convention

Writing to `x0` is legal and has no effect, because the register file has no
storage for that number. Simulating it any other way makes `ori a1, x0, 30`
behave differently on the model than on the machine, and that idiom is how
every small constant is loaded.

## A loop, executed

    ori a1, x0, 5
    ori a6, x0, 0
    loop:
      addi a6, a6, 1
      addi a1, a1, -1
      bne a1, x0, loop

leaves `a6` at 5 and `a1` at 0, which is the shape of the counting loop the
sheet asks to trace, including the `bne` that falls through exactly once.
