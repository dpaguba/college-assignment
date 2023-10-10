# Naive Bayes

Multiply the class prior by the likelihood of each feature given the class,
as though the features were independent.

They usually are not. The module builds a data set whose two features
correlate at 0.94, which violates the assumption badly, and the classifier
still reaches 0.9 accuracy. The reason is that a decision needs only the
ranking of the classes and not the correctness of the probabilities, and the
dependence inflates both sides of the comparison.

## Smoothing is not optional

Without it, one unseen feature value makes the whole product zero and the
class impossible, whatever the other features say. The module shows that
directly: the probability of a class given an unseen value is exactly zero
without smoothing and positive with it. A single unfamiliar word would
otherwise veto an entire document.
