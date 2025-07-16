# Duality

Every linear program has a dual with one variable per constraint, and the two
optima agree. The dual variables are shadow prices: the value of one more
unit of each resource.

For the sheet's production problem:

| constraint | price |
|---|---:|
| machine hours | 0.5 |
| raw material | 0.3 |
| market limit | 0 |

The market limit is not binding, so another unit of it is worth nothing. The
other two are exhausted and each additional hour or unit is worth exactly
what the price says, which the module verifies by relaxing the bound and
measuring the improvement rather than by reading it off a tableau.

That is what turns a solved model into advice. The optimum says what to
produce; the prices say what to buy.
