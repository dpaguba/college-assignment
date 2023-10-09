# Evaluating a classifier

A score becomes a decision only after a threshold is chosen, and every
threshold gives a different confusion matrix. The ROC curve plots all of
them and the area under it summarises the ranking rather than any one
decision.

| ranking | area |
|---|---:|
| every positive above every negative | 1.0 |
| a mixed order | between |
| every positive below every negative | below 0.5 |

The area does not change when the scores are multiplied by ten, which the
module checks, because it depends only on the order. That invariance is why
it is the measure to report before the operating point is chosen, and why it
says nothing about how the classifier will behave once one is.
