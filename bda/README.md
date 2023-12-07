# Big Data Analytics

Twenty-four modules in six blocks, following the eight chapters of the
lecture. The basics shared with
[Grundlagen der Datenwissenschaft](../gdw/) stay there; this subject takes
the variants, the ensembles and the high-dimensional half.

| Block | |
|---|---|
| [data-exploration](data-exploration/) | scales, summaries, and a real data set |
| [clustering](clustering/) | k-means variants, silhouette, EM, density, hierarchy |
| [classification](classification/) | neighbours, Bayes, pruning, ROC |
| [ensembles](ensembles/) | bagging, boosting, forests |
| [deep-learning](deep-learning/) | training, convolution, interpretability |
| [patterns-and-dimensions](patterns-and-dimensions/) | FP-growth, closed sets, the curse, PCA |

## The published solutions, reproduced

| Sheet | Result |
|---|---|
| 10, AdaBoost | ε₁ = 0.3, α₁ = ln(7/3) = 0.8473, weights 1/6 and 1/14, ε₂ = 0.2857, α₂ = 0.9163 |
| 12, Apriori and FP-growth | 13 frequent itemsets, 10 closed, and the two maximal ones {ACE} and {DEF} |
| 12, closed sets | A is frequent and not closed, because {AE} has the same support |

## Numbers worth keeping

| | |
|---|---:|
| penguins: overall mean mass against every species | 4216 g, none within 400 g |
| nearest neighbour on the bill measurements | 0.944 |
| two concentric rings: DBSCAN against k-means | 2 clusters against 18 errors of 36 |
| out-of-bag share against 1/e | 0.3682 against 0.3679 |
| naive Bayes on features correlated at 0.94 | 0.9 accuracy |
| pruning: training and test accuracy | 0.94 → 0.90 and 0.75 → 0.76 |
| distance spread, 2 against 200 dimensions | 0.475 against 0.041 |
| ball inside a cube, 2 against 10 dimensions | 0.785 against 0.002 |
| convolutional against dense parameters | 48 against 808 |
| FP-growth against Apriori, database passes | 2 against 4 |

## Three results that argue with the first guess

**Principal components without standardisation find the units.** On the
penguins the first raw component explains 99.99 percent of the variance and
is body mass, because grams are numerically larger than millimetres. After
standardising, the first explains 65 percent and the first two 85, which is a
statement about the birds rather than about the measuring instruments.

**A violated assumption is not a broken model.** Naive Bayes on two features
correlated at 0.94 reaches 0.9 accuracy, because a decision needs the ranking
of the classes and not the correctness of the probabilities.

**Accuracy cannot see which feature it came from.** The interpretability
module builds a model that is perfectly accurate and uses only a spurious
feature; permutation importance names it and no measure of performance does.

## Verification

The AdaBoost rounds and the itemset families are compared with the published
solutions. FP-growth is compared with an enumeration of every subset. The
nearest neighbour classifier is evaluated leave-one-out on real
measurements. The out-of-bag share is measured against 1/e, and the
clustering methods are compared against each other on data built so that one
of them has to fail.
