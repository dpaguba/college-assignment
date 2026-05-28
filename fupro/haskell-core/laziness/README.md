# Lazy evaluation

A value is computed only if it is needed, so a definition may mention an
infinite list or a computation that never terminates as long as nothing
forces it.

The exam asks for an infinite list of triples solving `5x + y² + 10 = z` that
is productive, meaning `take 2` has to finish. That rules out the obvious
nested loop, which would never leave `x = 0`. Enumerating the pairs
diagonally reaches every pair eventually, which is the same argument as the
countability of the pairs of naturals from any first-semester course.

```
take 2 solutions  =  [(0,0,10), (0,1,11)]
```

which is exactly the output the exam prints as acceptable.

## What laziness buys and costs

It buys the separation of production from consumption: a sieve can be written
as an infinite stream and the caller decides how much of it exists. It costs
predictability about when work happens, which is why the module counts how
many of three defined values a consumer actually forces, and gets one.
