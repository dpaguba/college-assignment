# Branch prediction

| Topic | |
|---|---|
| [dynamic-predictors](dynamic-predictors/) | one bit, two bits, and what each fixes |
| [correlating-predictors](correlating-predictors/) | history, and the tournament that combines them |
| [branch-target-buffer](branch-target-buffer/) | knowing where a taken branch goes |

Prediction exists because pipelines are deep, and it gets more elaborate as
they get deeper: the penalty is set by the depth, so the only remaining factor
is accuracy. The progression here is the history of that pressure, and each
step is measured on a pattern that defeats the previous one.
