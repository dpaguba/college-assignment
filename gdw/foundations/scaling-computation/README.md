# Scaling computation

Two laws answering two different questions.

**Amdahl** asks how much faster a fixed problem runs on more processors:

| workers | 2 | 4 | 16 | 1000 |
|---|---:|---:|---:|---:|
| speedup at 10% serial | 1.82 | 3.08 | 6.4 | 9.91 |

The ceiling is ten, whatever the machine. A tenth of the work that cannot be
split decides the answer, and adding processors past sixteen buys almost
nothing.

**Gustafson** asks how much more work fits in the same time, and its answer
grows with the machine, because a larger problem usually has a larger
parallel part and the same serial one.

Neither law is wrong. They describe different experiments, and quoting one
against the other is the standard confusion in this area.
