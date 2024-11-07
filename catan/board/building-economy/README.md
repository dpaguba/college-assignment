# The cost of building

| | Brick | Lumber | Wool | Grain | Ore |
|---|---:|---:|---:|---:|---:|
| road | 1 | 1 | | | |
| settlement | 1 | 1 | 1 | 1 | |
| city | | | | 2 | 3 |
| development card | | | 1 | 1 | 1 |

Brick and lumber build outwards, grain and ore build upwards. Wool appears
once in each set, which makes it the resource most easily traded away.

## How long the waiting is, exactly

The waiting time is not simulated but solved. The state is the stock, capped
at what is needed; a roll moves it; the expected number of steps to the target
state is the absorption time of a small Markov chain. That matters because the
resources do not arrive independently: one roll serves every adjacent hex
carrying that number at once, so any formula treating them separately is
wrong.

| Building | Corner | Turns |
|---|---|---:|
| road | brick on 6, lumber on 8 | **10.80** |
| road | brick and lumber both on 6 | **7.20** |
| settlement | 6, 8, 5, 9 | 16.98 |
| city | grain on 6, ore on 8 and 5 | 17.88 |

Checked against 40 000 simulated games each; the exact 10.80 and the simulated
10.75 agree.

## Two numbers worth reading twice

The slowest single resource for the road takes 7.2 turns on its own. Waiting
for **both** takes 10.80, so the second half of the wait costs 3.6 turns and
comes from nothing but having to wait for the later of two.

And two hexes on the same number beat two hexes on different numbers, 7.20
against 10.80, even though the expected income per turn is identical.
Concentration removes the waiting for the last card; spreading adds it. The
usual advice to diversify is about robustness against the robber, not about
speed, and the two pull in opposite directions.
