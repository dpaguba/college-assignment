# Dynamic programming

Bellman's principle: whatever the first decision was, the rest of an optimal
policy is optimal for the state it leads to. That condition is what makes the
backward recursion valid, and it is a property of the problem rather than of
the method.

The module checks it on the example rather than assuming it: the tail of the
optimal path is compared with the optimal path from its own start, and they
agree.

## Memoisation, in two numbers

| computing the twentieth Fibonacci number | calls |
|---|---:|
| plain recursion | 21 891 |
| with the results remembered | 39 |

Same answer, 561 times fewer calls. The saving comes from the overlap between
subproblems, which is the second condition dynamic programming needs and the
one that decides whether it applies at all.
