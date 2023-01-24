# Elasticity

Percentage change in quantity per percentage change in price. For linear
demand it is not constant: zero at a price of zero, minus infinity at the
prohibitive price, and exactly minus one halfway between.

The module computes it analytically and by finite difference, and the two
agree at every price tested.

## What it is for

In the elastic range a price rise lowers revenue, in the inelastic range it
raises it, and at minus one revenue is at its maximum. Searching a grid for
the revenue peak lands on the same price the formula gives, which is the check
that both are right.

## Why the number is rarely known

It requires knowing what would have happened at another price, and that can
only be observed if the price actually was different. Historical data helps
little, because something else usually changed along with the price. An
experiment works and is visible, and customers react to being experimented on.
The number is therefore an estimate, and the recommendation is only as good as
the estimate.
