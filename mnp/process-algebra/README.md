# Process algebra

| Topic | |
|---|---|
| [ccs](ccs/) | prefix, choice, parallel, restriction, and the buffers |
| [bisimulation](bisimulation/) | when two processes are the same, in two senses |
| [pi-calculus](pi-calculus/) | passing names, and a topology that changes |

A process algebra gives behaviour a syntax and an equality. The syntax is
small: prefix, choice, parallel composition, restriction. The equality is the
part that does the work, because it decides which implementations count as
correct with respect to a specification.

The block's central example is `a.(b + c)` against `a.b + a.c`. Same traces,
different behaviour, and the difference matters exactly when it matters to a
user: whether the choice is yours or the machine's. Getting that distinction
into a definition is what bisimulation is for.

The pi-calculus then relaxes the one thing CCS holds fixed. Channels become
values, so the communication structure evolves, and the encodings show that
data is not a separate ingredient.
