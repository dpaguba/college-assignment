# The production programme

Five products competing for 500 kg of a bottleneck. Exercise 3 of tutorial
nine, and the one place in the course where a spreadsheet solves an
optimisation problem.

The idea is the **relative contribution margin**: margin per unit of the
scarce factor, not per unit of product. A product with a high absolute margin
that eats a lot of capacity displaces two products that together earn more.

| Product | Margin | Usage | Relative | Demand |
|---|---:|---:|---:|---:|
| A | 30 € | 2 kg | 15 | 80 |
| D | 12 € | 1 kg | 12 | 100 |
| C | 45 € | 5 kg | 9 | 50 |
| B | 24 € | 3 kg | 8 | 60 |
| E | 36 € | 6 kg | 6 | 40 |

Full demand needs 930 kg against 500 available, which is why there is
anything to plan. Taking products in order of relative margin: A at 80 units
(160 kg), D at 100 units (100 kg), C at 48 of its 50 units (240 kg), and the
capacity is exactly used. Contribution: **5760 €**.

## Two checks

Ranking by **absolute** margin instead, which is the ordering that suggests
itself, gives 3840 €. The right ordering is worth a third of the profit, and
that difference is the entire content of the exercise.

The 5760 € was verified against a bounded-knapsack dynamic programme over the
same capacity with the same 330 units, which reaches the same figure. The
greedy rule is not merely plausible here, it is optimal.

## Part b

The exercise asks for the capacity limit to become a cell so the formula need
not be rewritten. `variable_capacity` is that parameter, and the table it
returns shows what hangs on it: 300 kg gives 3960 €, 700 kg gives 7326 €.
