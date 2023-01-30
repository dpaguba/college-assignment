# Marketing (Modul 2: Markt und Absatz)

Eleven lectures and, unusually, exercises **with solutions**: break-even, one-
and multi-stage contribution costing, price and distribution. Sixteen modules
follow them, and every figure the sheets give is reproduced.

| Block | Modules | What it holds |
|---|---:|---|
| [foundations](foundations/) | 3 | what marketing is, planning, the mix |
| [costing](costing/) | 4 | break-even, contribution margins, price floors |
| [pricing](pricing/) | 4 | elasticity, the optimal price, differentiation, revenue management |
| [distribution](distribution/) | 2 | channels and the arithmetic behind them |
| [demand](demand/) | 3 | consumer behaviour, research, the life cycle |

## The exercises, reproduced

**Break-even, "Daniel's Clear".** Fixed costs 500 000 €, variable unit cost
4 €, price 14 €. Critical quantity 50 000; with a target profit of 600 000 it
is 110 000; the unit contribution is 10 €.

**Multi-stage contribution costing, Bosch GmbH.** Five products in two areas,
25 000 € of fixed costs of which 12 000 belong to area A and 7 000 to area B.
Area A contributes 19 905 € after its own fixed costs, area B **−500 €**, the
company 19 405 €, and the operating result is 13 405 €.

The Handrührer has a contribution of −700 €: it sells for 30 € and costs 37 €
in variable cost alone. Every unit sold loses seven euros before any fixed
cost is allocated, and that is the one case where the calculation gives a
clear answer.

## Three things the code checks that the sheets do not

**The death spiral is real and quantified.** Allocating the fixed costs by
volume makes three of the five products look loss-making. Dropping those three
takes the operating result from 13 405 € to 800 €, because their contributions
go and the fixed costs stay.

**The optimal price does not depend on the fixed costs.** A grid search finds
the same price of 30 € at fixed costs of 0, 5 000 and 50 000 €, and only the
profit moves. The Cournot formula says so and the search confirms it.

**Littlewood's rule had an off-by-one.** Written with `P(D > y)` instead of
`P(D ≥ y)` it protects one demand level too few: 20 seats where the exhaustive
search over all protection levels finds 30. With the comparison corrected the
rule matches the search at every price ratio tested. The search is what caught
it.
