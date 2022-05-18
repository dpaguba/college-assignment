# Interleavings

k processes with n₁, n₂, … steps have (Σnᵢ)! / Πnᵢ! possible runs: the order
within a process is fixed, the order between them is not. The module computes
the multinomial coefficient and, for small inputs, enumerates the runs to
check the formula against a count.

Three processes with equal step counts:

| Steps each | Runs |
|---:|---:|
| 1 | 6 |
| 2 | 90 |
| 3 | 1 680 |
| 4 | 34 650 |
| 5 | 756 756 |

## The consequence

A bug that appears in one of 756 756 runs will not appear in a thousand test
executions, and will appear in production. That is why the tools in this
course are reachability graphs, bisimulation and model checking rather than
more tests.
