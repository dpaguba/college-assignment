# Relative and absolute references

Copying a formula shifts every relative reference by the offset between the
two cells and leaves every absolute one alone. That is the whole of what the
dollar sign does, and `copy_formula` implements exactly it.

## The mistake the exercise exists to prevent

The gross price in D6 is `=C6*(1+$D$22)`. Filled down, C6 walks with the
formula and $D$22 stays. Without the dollar signs the VAT rate walks too: D7
refers to D23, D8 to D24, and after eight rows the rate points at an empty
cell.

The result is not an error. An empty cell counts as zero, so the formula
returns the net price, and the column looks entirely plausible. That is why
this particular mistake survives review.

| | D6 | D9 | D13 |
|---|---|---|---|
| with dollars | `=C6*(1+$D$22)` | `=C9*(1+$D$22)` | `=C13*(1+$D$22)` |
| without | `=C6*(1+D22)` | `=C9*(1+D25)` | `=C13*(1+D29)` |
