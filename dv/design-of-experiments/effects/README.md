# Main effects and interactions

Two factors, four cells. The main effect of a factor is the mean change when
it moves from its low to its high level; the interaction is the difference of
the two differences, halved so that it enters the model on the same scale.

On the table 20, 30, 25, 45:

- effect of A: 15
- effect of B: 10
- interaction AB: 5

Four cells and four parameters, so the model with the interaction reproduces
the table exactly. Dropping the interaction leaves a largest error of 2.5 in
every cell, which is the interaction itself distributed over the four
corners.

An interaction is visible in the plot as two lines that are not parallel. The
module's numbers come out identically to those of the 2^k module on the same
data, which is the same computation written twice from two directions.
