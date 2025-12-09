# Classification

| Module | Topic |
|---|---|
| [distances](distances/) | three measures, and which one is a metric |
| [knn-classifier](knn-classifier/) | k neighbours, votes and ties |
| [cross-validation](cross-validation/) | the folds and what they do not tell you |
| [naive-bayes](naive-bayes/) | multinomial, smoothed, in the log domain |

Two results in this block are warnings rather than methods. The cosine
distance fails the triangle inequality in 237 of 2 000 random triples, so
anything built on that inequality has no guarantee under it. And choosing k on
the validation data produces an error rate of 0.442 on data that contain no
signal at all, where the right answer is 0.500.
