# What a corner is worth

The expected number of cards per roll is the sum of the probabilities of the
adjacent numbers. Summing them is allowed even though at most one hex can pay
per roll: the expectation of a sum is the sum of the expectations, whether the
events are independent or not.

Checked against 300 000 simulated rolls; a corner at 6, 8 and 5 yields
14/36 = 0.389 cards per roll, and the simulation agrees to two decimals.

## Yield is not the whole story

Three hexes of the same resource give many cards of one kind, and building
takes four kinds. The module therefore reports the number of distinct
resources beside the yield. On one shuffled board the strongest corner carries
tokens 6, 5 and 6 for 0.389 cards from **two** resources, while the next one
gives 0.333 from three. Which is better depends on what else the player holds,
and the number alone cannot say.

## A city is a corner counted twice

Upgrading doubles the yield of a corner already owned, without needing a free
corner, a road to it, or the distance rule to cooperate. That is why the
comparison between building out and building up shifts over a game: early the
good corners are still free, late they are not.

## What the number leaves out

The harbours, what the opponents need, and the robber, who goes to the
strongest number on the board. The corner with the best expectation is also
the first one to be blocked.
