# Additivity

Which measure may be summed over which axis. Three answers:

- **additive:** over every dimension. The risk score, for instance: it is
  recorded per kind of risk, so adding the three gives the project's total.
- **semi additive:** over some axes but not others. A stock level may be
  added across products and not across time.
- **non additive:** over none, because it is a ratio, and ratios do not add.

## The trap in this table

The Quartalsbudget belongs to the project quarter. The table splits its rows
by kind of risk, so the budget is repeated in all three rows of each project
quarter. Summing the column gives:

| | |
|---|---:|
| sum over all 24 rows | 8730 T€ |
| sum over the 8 distinct project quarters | 2910 T€ |
| factor | 3 |

Nothing is missing, nothing is mistyped, and the number is three times too
large. This is how a report ends up wrong without anybody making a mistake
that could be pointed at.

## How to notice

When the same value repeats word for word across the rows of a group, it does
not belong at row level. The test costs nothing: sum over the rows, sum over
the distinct keys, compare. If they differ, the measure has a finer grain
than the table.
