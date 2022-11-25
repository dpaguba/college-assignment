# Evaluation

| Topic | |
|---|---|
| [confusion-matrix](confusion-matrix/) | four counts, and the misleading summary |
| [precision-recall](precision-recall/) | two numbers that pull apart |
| [cross-validation](cross-validation/) | testing on data the model has not seen |

The block that decides whether anything in the previous one worked. Two
numbers make the case: a classifier that finds nothing scores 99 percent
accuracy on an unbalanced problem, and a model that memorises its training
data scores 1.00 on it and 0.40 under cross validation.

Both failures look like success in the summary that is usually reported, and
both are visible immediately in the summary that is not.
