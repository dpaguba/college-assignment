# Depreciation

Four methods over the same asset, 100 000 € with a salvage value of 10 000 €
and five years. All four write off 90 000 €. Which years carry it is the only
open question.

| Method | Year 1 | Total |
|---|---:|---:|
| linear | 18 000 | 90 000 |
| declining, 40 % | 40 000 | 90 000 |
| declining with switch, 30 % | 30 000 | 90 000 |
| by usage | follows the output | 90 000 |

## The base of the declining rate

The rate applies to the **book value**, not to the book value less the salvage
value. Using the wrong base moves the switch year by a whole year: with
100 000 €, 10 000 € salvage, five years and 30 %, the correct base switches in
year 4 (30 000, 21 000, 14 700, 12 150, 12 150) and the wrong one in year 3.
The cross-check found this by disagreeing with the module; the module was
right and the cross-check was wrong.

The geometric series never reaches the salvage value on its own, which is why
the last year takes whatever remains.

## When to switch

Switch in the first year in which the linear amount over the remaining life is
at least the declining amount. With 100 000 €, no salvage, five years and
40 %, that is year 4: 40 000, 24 000, 14 400, 10 800, 10 800. After the switch
the amounts are flat, which is a test the module runs.

## What the choice does change

Not the total, but the profit of each year, the tax paid in each year, and
therefore the interest on the tax deferred. That is the whole benefit, and it
is real.
