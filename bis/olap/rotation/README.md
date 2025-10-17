# Rotation

The numbers do not change, the reading direction does. `pivot` builds a cross
table from two dimensions and one measure; `transpose` swaps its axes.

Projects in the rows and kinds of risk in the columns is the project
manager's view: which risk does my project carry. Transposed it is the risk
manager's view: which kind of risk weighs across all projects. Same twenty-
four numbers, two different questions.

## The check

Transposing twice must return the original table. That holds here on all
twelve ordered pairs of the four dimensions, which is a cheap and complete
test of the operation.

Empty combinations are kept as `None` rather than dropped, so the table stays
rectangular. P4 has no third quarter, so the cell for (P4, Q3) is empty, and
that is visible instead of silently missing.
