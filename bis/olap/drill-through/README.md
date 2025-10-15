# Drill-through

Drill-down stays inside the cube and goes one level deeper; the answer is
still an aggregate. Drill-through leaves the cube and shows the records
behind the figure.

`explain` computes a figure and puts its ingredients next to it: the value,
the individual contributions, the source rows and how many there were.

## Why the row count belongs in the report

An average over three rows and an average over thirty look identical in a
report. `when_a_figure_is_thin` says how many rows a figure rests on and
warns below a floor, because that is the single most common way a dashboard
misleads: a striking number that turns out to be one case.

In this table the risk of P4 and P5 rests on three rows each, and that of P1,
P2 and P3 on six. Comparing their averages is fair, but only after noticing
that the first two cover one quarter and the others two.
