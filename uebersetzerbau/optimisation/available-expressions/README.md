# Available expressions

An expression is **available** at a point when it has been computed on every
path to that point and no operand has changed since. Two identical computations
with an available expression between them are a common subexpression, and the
second one can be replaced by the first one's result.

This is the mirror image of liveness in both axes: **forwards**, and
**intersection** at joins, because "on every path" is a must property. Together
with very busy expressions, the must-backward analysis behind code hoisting,
the four corners of the monotone framework are:

| | may (union) | must (intersection) |
|---|---|---|
| forwards | reaching definitions | **available expressions** |
| backwards | **live variables** | very busy expressions |

## The initialisation is what makes it a must analysis

Every node except the entry starts with **everything** available, and the
iteration removes what cannot be justified. Starting from the empty set would
compute the least fixed point, which for an intersection framework says nothing
is ever available: correct and useless.

## Measured

| program | redundant |
|---|---|
| `t = a+b; u = a+b` | the second one |
| `t = a+b; a = 5; u = a+b` | none |
| join of `t = a+b` and `u = a-b` | none available after the join |
| join of `t = a+b` and `u = a+b` | `a+b` available after the join |

The third and fourth rows are the intersection at work: an expression computed
on only one branch is not available afterwards, however cheap it was.

## Kill comes after generate

For `a = a+b` the expression `a+b` is computed and then immediately
invalidated, so it is not available afterwards. Adding after killing would
wrongly claim it is, which is the same ordering trap as in the liveness
transfer function, in the opposite direction.
