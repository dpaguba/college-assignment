# Integer programming

Dropping the integrality gives a linear program whose optimum bounds the
integer one, and branch and bound uses that bound twice: to prune a branch
that cannot beat the best solution found, and to choose where to branch.

| | nodes explored |
|---|---:|
| branch and bound | 5 |
| enumerating every integer point | 961 |

Both find the same optimum, and the bound is what removes the other 956.

## The greedy warning

The knapsack with values 60, 100 and 120 against weights 10, 20 and 30 in a
capacity of 50:

| | value |
|---|---:|
| optimum | 220 |
| best ratio first | 160 |

The greedy rule takes the item with the best value per weight and thereby
blocks the two that fit together. It is fast, it is wrong here by 27 percent,
and it gives no indication that it is wrong, which is the difference between
a heuristic and an exact method.
