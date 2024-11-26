# The board

| Module | Topic |
|---|---|
| [hex-board](hex-board/) | the geometry, derived rather than looked up |
| [dice-odds](dice-odds/) | 36 outcomes and the pips that encode them |
| [settlement-value](settlement-value/) | what a corner is worth per roll |
| [building-economy](building-economy/) | the costs, and how long they take |
| [robber-and-discard](robber-and-discard/) | the seven, twice over |

Everything in this block is exact and therefore checkable. The 54
intersections and 72 roads come out of the construction and are confirmed by
Euler's formula. The dice probabilities come from enumerating all 36 pairs.
The waiting time for a building is the absorption time of a small Markov
chain, solved rather than simulated, and the simulation then agrees with it.

The one result worth carrying to the table: two hexes on the **same** number
give the resources for a road in 7.2 turns, two hexes on different numbers in
10.8, at identical expected income.
