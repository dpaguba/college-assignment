# Roll-up and drill-down

The same computation in two directions. Roll-up keeps some axes and drops the
rest; drill-down adds an axis back.

Average risk per project, which is a roll-up onto one axis:

| Project | Mean risk |
|---|---:|
| P5 IoT Produkt | 8.00 |
| P2 KI-Prognose | 6.50 |
| P3 ERP-Migration | 5.83 |
| P1 Kundenportal | 3.50 |
| P4 Neue Fassade | 3.33 |

## The check that matters

`consistency` sums the drilled-down parts and compares them against the
rolled-up whole. For an additive measure they must agree, and on this table
they do for every axis. When they stop agreeing, one of two things is true:
the decomposition is wrong, or the measure is not additive over that axis.
The second case is the common one and is what the additivity module is for.

## Hierarchies

A dimension usually carries levels: day, month, quarter, year. Roll-up moves
one level up, drill-down one down. This table stores only the lowest level of
each dimension and computes everything above it, which is the normal
arrangement: storing the aggregates as well means keeping them consistent for
ever.
