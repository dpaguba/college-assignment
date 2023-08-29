# Shapley values

A player's value is the average of what they add, over every order in which
the players could arrive. Computed as a weighted sum over all subsets not
containing them.

## The glove game

Two players hold a left glove, one holds a right. A pair is worth one euro,
single gloves nothing. The values come out at 1/6, 1/6 and 2/3: the scarce
side is worth four times as much, although all three contribute the same
quantity. That is the whole idea of the construction, and it is why it cannot
be replaced by counting contributions.

## Four axioms

Efficiency: the values sum to the value of the full coalition. Symmetry: two
interchangeable players get the same. Dummy: a player who adds nothing gets
nothing. Additivity: two games played side by side add up.

The Shapley value is the **only** allocation satisfying all four, which is why
the choice is not a matter of taste. The price is in the exponent: 2ⁿ
evaluations, so a million per explained prediction at twenty features. Every
practical implementation approximates, and inherits the axioms only
approximately.
