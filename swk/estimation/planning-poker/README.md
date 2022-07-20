# Planning poker

Turning several opinions into one number, and why the number is not the point.

Everyone estimates simultaneously, the extremes explain themselves, the round
repeats. The lecture is explicit that the **discussion** is the product: the
highest and lowest estimator each know something the others do not, and the
re-estimate is where that knowledge moves.

```
round 1: {Anna: 3, Bohdan: 13, Vika: 5, Hlib: 5}  spread 4.3  no consensus
round 2: {Anna: 5, Bohdan: 8,  Vika: 5, Hlib: 5}  spread 1.6  consensus
agreed: 5 points
```

## The deck is not linear

1, 2, 3, 5, 8, 13, 21. The gaps grow because precision does not: nobody can
tell a 17-point story from an 18-point one, and a deck that offers both invites
a false argument. The commercial variant adds 0, a half, and a "too big to
estimate" card, which is a scale that admits its own limits.

## Median, not mean

The average of 3 and 13 is 8, which nobody offered. The median stays inside
what the team actually said, and the result is snapped back to a card on the
deck, because a consensus of 6.5 is a number the scale cannot express.

## Triangulation

The lecture's own advice: check estimates against each other, not against
hours. A two-point story should look about twice a one-point story, and two
five-point stories should look alike. `triangulate` lists the pairs where the
ratio of points is far from the ratio of the reference sizes, which is where a
scale has drifted without anyone noticing.

## Points to time

`to_hours` needs a measured velocity and refuses to work without one. That is
the whole discipline of the technique: points have no time in them, and a team
that converts them by a fixed rate has quietly gone back to estimating hours
with extra steps.
