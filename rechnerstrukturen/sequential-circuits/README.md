# Sequential circuits

| Topic | |
|---|---|
| [flip-flops](flip-flops/) | one bit of memory, and its forbidden input |
| [synchronous-automata](synchronous-automata/) | Moore, Mealy, and the encoding into flip-flops |
| [memory-organisation](memory-organisation/) | decoders, cells, and the SRAM against DRAM trade |

Adding state to a circuit adds time, and everything here follows from that:
the forbidden flip-flop input is a race, the difference between the two machine
models is one cycle, and the reason DRAM is slow is that its state decays.
