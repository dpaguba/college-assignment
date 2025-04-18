# KI für Brettspiele

Twenty modules along a project that has two halves that barely touch: writing
an AI for Catan, and a machine learning lecture. The modules keep both and put
the numbers where the slides leave questions.

| Block | Modules | What it holds |
|---|---:|---|
| [board](board/) | 5 | geometry, dice, corners, costs, the seven |
| [move-choice](move-choice/) | 4 | legal moves, scoring, lookahead, expectimax |
| [learning](learning/) | 7 | bias and variance through to the optimisers |
| [limits](limits/) | 4 | four ways a number can be right and useless |

## What is in the folder

Two PDFs, one per semester, the same 77 slides apart from dates and a branch
name. The game implementation lives in the faculty's git and is not here, and
neither are any data. So the game side is rebuilt from the rules, exactly
where it can be, and the learning side from the lecture.

## Six results

**Two hexes on the same number beat two on different numbers.** Waiting for a
brick and a lumber both on a 6 takes 7.20 turns; on a 6 and an 8 it takes
10.80, at identical expected income. The difference is the wait for the later
of two, and it is solved as a Markov chain rather than simulated. The usual
advice to spread out is about the robber, and it costs a third of the building
speed.

**A weighted sum cannot prefer a balanced corner.** Three corners with feature
vectors (1,0), (0,1) and (0.5,0.5), and building needs both resources. Wanting
the third to win requires `w₂ > w₁` and `w₁ > w₂` at once. A grid of 4 225
weight vectors finds none, as it must. A product term fixes it immediately,
and that is the concrete reason a hand-written Catan evaluation needs
interactions.

**Looking one move further can lose the game.** With an evaluation function
whose error does not shrink near the leaves, the depth-1 search picks the move
worth 10 and the depth-2 search picks the one worth 0. Deeper search only pays
under an assumption about the evaluation, and in Catan it also costs eleven
dice branches per move.

**The seven flips the sign of a turn.** For a player holding nine cards, a
turn is worth +0.333 cards with the seven left out of the tree and **−0.389**
with it in. The seven pays no hex, so it drops out of an income calculation
without anyone noticing, and what drops out with it is the reason not to
hoard.

**No free lunch, enumerated.** Over all 32 target functions on five points,
six deliberately different learners each score exactly 0.5 on the unseen
points, to twelve decimals. On one smooth target they range from 0.00 to 1.00.
The averaging is where the theorem gets its force and where it stops being
about anything real.

**The textbook bias-variance curve has a boundary.** Bias falls and variance
rises, as the slide draws it, while the sample supports the fit. At 25 points
and degree 11 the measured bias is 2 793 and the variance 758 222: both rise
together, because the individual fits swing so far that even their average is
nowhere near the truth. The identity still holds; the picture does not.

## The board, derived

Nineteen hexes give 54 intersections and 72 roads, and Euler's formula
confirms it: `54 − 72 + 20 = 2`. The largest set of corners obeying the
distance rule has **27** members, half the board, while the box holds 20
settlements for four players. The rule is not what makes the board tight; the
pieces and the roads to reach a corner are.

## The checks

Every module is built around something that could fail. Dice probabilities
against the enumeration of all 36 pairs, the waiting time against 40 000
simulated games, expectimax against every fixed policy on 200 random trees,
the tree split against an exhaustive threshold search, backpropagation against
finite differences to 1.4 × 10⁻¹¹, each optimiser rule against its published
form, and the area under the ROC curve against a pair count and a rectangle
sum.

Mutation testing on those checks found one that was not a check: the
"independent" threshold search was quietly copying its answer from the
function it was meant to verify. It compares partitions now.
