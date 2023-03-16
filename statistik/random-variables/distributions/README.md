# Random variables and their distributions

A random variable attaches a number to each outcome. Its distribution
function is the probability of not exceeding a point, and for a discrete
variable it is a staircase: right continuous, with a jump at each value equal
to the probability of that value.

The die of the fifth sheet has faces 1, 3, 3, 4, 4, 6, so

```
p(1) = 1/6,  p(3) = 1/3,  p(4) = 1/3,  p(6) = 1/6
```

and the distribution function jumps by those amounts. Right continuity is
what fixes the value **at** a jump, and the tests check it in both
directions: the value at 3 equals the value just after 3 and differs from the
value just before.

For a continuous variable the density replaces the probability function. A
density is not a probability, it may exceed one, and only its integral over
an interval is a probability, which is why every single point has probability
zero. That fact is checked rather than asserted, because it is the source of
most confusion about continuous variables.
