# Dynamic scheduling

| Topic | |
|---|---|
| [scoreboarding](scoreboarding/) | out-of-order execution without renaming |
| [tomasulo](tomasulo/) | the same, with renaming |

Both let an instruction execute as soon as its operands are ready rather than
waiting for the one in front. The difference is one idea, and the two are
implemented side by side so that the idea can be measured rather than
described: an 18-cycle WAR stall on the same three-instruction program, in a
run whose total length is identical.
