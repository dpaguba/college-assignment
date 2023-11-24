# Classification

| Topic | |
|---|---|
| [nearest-neighbour](nearest-neighbour/) | no model, all the work at prediction |
| [naive-bayes](naive-bayes/) | a false assumption that works |
| [tree-pruning](tree-pruning/) | trading training accuracy for the other kind |
| [classifier-evaluation](classifier-evaluation/) | ranking against deciding |

Chapter five. The basic decision tree is in
[gdw/learning/decision-trees](../../gdw/learning/decision-trees/); this block
adds the methods that make different assumptions and the evaluation that
compares them.

Two results are worth carrying. Naive Bayes reaches 0.9 accuracy on features
correlated at 0.94, so a violated assumption is not automatically a broken
model. And pruning a tree costs four points of training accuracy and gains
one of test accuracy, which is the only direction that says the removed
structure was noise.
