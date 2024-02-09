# Association rules

A rule splits a frequent itemset, and its confidence is the share of the
transactions containing the left side that also contain the right.

Confidence alone finds artefacts. In the module's example the rule has a
confidence of 0.875 and a lift of 0.97:

| | |
|---|---:|
| confidence | 0.875 |
| base rate of the right side | 0.900 |
| lift | 0.972 |

The right side occurs in 90 percent of the transactions anyway, so a rule
predicting it 87.5 percent of the time is doing **worse** than guessing. A
lift below one means the left side makes the right side less likely, and
confidence cannot see that because it never looks at the base rate.

That is the standard warning of the chapter and the reason no rule should be
reported without its lift.
