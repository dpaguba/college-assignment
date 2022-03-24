# Instruction set

| Topic | |
|---|---|
| [riscv-encoding](riscv-encoding/) | six formats, one word |
| [riscv-assembly](riscv-assembly/) | executing it, and transfer notation |
| [datapath](datapath/) | what the control unit switches |

The three are one object seen at three distances. The encoding is what the
decoder reads, the assembly is what a person writes, and the datapath is what
both of them are descriptions of. The encoding's oddities, split immediates and
fixed register positions, are explained only by the third.
