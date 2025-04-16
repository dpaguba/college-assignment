# Limits

| Module | Topic |
|---|---|
| [no-free-lunch](no-free-lunch/) | the theorem, enumerated |
| [roc-and-auc](roc-and-auc/) | the ranking, and what it ignores |
| [cost-benefit](cost-benefit/) | the operating point |
| [base-rate-and-confusion](base-rate-and-confusion/) | the yardstick |

Four ways a number can be right and useless. The no-free-lunch theorem holds
exactly, to twelve decimals over all 32 target functions, and says nothing
about any single problem. The area under the ROC curve is unmoved by class
imbalance while precision falls from 0.87 to 0.21 on the same data. Accuracy
is a cost matrix nobody wrote down. And a 99 % test on a 1 % condition gives a
positive result that is right half the time.

For a game AI all four land in the same place: most moves are of no
consequence, so the interesting class is rare, and every measure that ignores
that reports success.
