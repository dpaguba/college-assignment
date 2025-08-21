# Hazards and forwarding

Three data hazards, and only one is a real dependence.

| name | pattern | real | removed by |
|---|---|---|---|
| RAW | read after write | **yes** | nothing |
| WAR | write after read | no | renaming |
| WAW | write after write | no | renaming |

RAW is a dependence of the computation. WAR and WAW exist only because two
instructions happen to use the same register name, which is why
[tomasulo](../../dynamic-scheduling/tomasulo/) removes them and why no amount
of cleverness removes RAW.

## Forwarding does not remove the load-use stall

Forwarding routes a result from the end of execute to the input of the next
execute. A load's value is not available until the end of memory, one stage
later, so the consumer still waits one cycle. Measured: one stall for a load
followed immediately by its use, and none when any instruction sits between
them.

## The CPI equation

    CPI = base + branches * taken * penalty + accesses * miss rate * penalty

Each term is a product, so improving any factor of any term is worth the same
as improving the others. That is why a deep pipeline invests in prediction
accuracy: its penalty is fixed by the depth, so the only factor left is the
middle one.

## The critical path is the bound

The longest chain of RAW edges is what no schedule can beat. Counting only RAW
edges is the point: the other two kinds are removable and do not belong in a
lower bound.
