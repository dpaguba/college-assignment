# Grundlagen der Datenwissenschaft

Twenty-two modules in six blocks, covering the eleven lectures and the
exercise sheets of both terms the course was taken in.

| Block | |
|---|---|
| [foundations](foundations/) | CRISP-DM, data quality, scaling, map and reduce |
| [graph-mining](graph-mining/) | PageRank and the surfer behind it |
| [pattern-mining](pattern-mining/) | Apriori, rules, closed and maximal sets |
| [similarity-search](similarity-search/) | shingles, Jaccard, MinHash, banding |
| [learning](learning/) | entropy, trees, margins, networks, clusters |
| [evaluation](evaluation/) | matrices, precision, cross validation |

## The exercises, reproduced

| Sheet | Result |
|---|---|
| 3, PageRank | the five-node graph, with node 4 ranking highest |
| 4, Apriori | frequent, closed and maximal itemsets at support two |
| 7, similarity | shingles, Jaccard, and MinHash signatures |
| 8, entropy | a die plus a coin: 2.7516 bits |
| 9, precision and recall | both two thirds on the example |

## Numbers worth keeping

| | |
|---|---:|
| effort in a project: preparation against modelling | 45% against 15% |
| Amdahl's ceiling at 10 percent serial | 10, whatever the machine |
| Apriori candidates against the full lattice | 8 against 15 |
| entropy of a die plus a coin | 2.7516 bits, against 2.585 for the die |
| decision tree, unlimited: training against test | 0.99 against 0.81 |
| degree nine polynomial on twelve points: variance | 29 145 |
| unbalanced classifier: accuracy against recall | 0.99 against 0.00 |
| memorising model: training against cross validated | 1.00 against 0.40 |
| LSH with 20 bands of 5: threshold | 0.549 |

## Three results that argue with the first guess

**The most linked page is not the highest ranked.** On the exercise graph node
3 has three incoming links and node 4 has the higher rank, because node 4's
single most important source has one outgoing link and gives it everything.
Counting links and ranking recursively are different measures, and five nodes
are enough to separate them.

**A rule with 87.5 percent confidence can be worse than guessing.** Its right
side occurs in 90 percent of the transactions anyway, so the lift is 0.97 and
the left side makes the right side less likely. Confidence measures a rule
against nothing.

**The textbook MinHash hash family is biased.** The linear family of a
multiplier and an offset modulo a prime gave estimates off by 0.025 in both
directions, three times the sampling error, and the error was invisible in a
single run. Averaging over eight seeds exposed it and a proper avalanche
mixer removed it.

## Verification

PageRank is computed twice, by power iteration and by solving the linear
system, and both are compared with a random walk of 200 000 steps. Apriori is
compared with a brute force enumeration of every subset. The MinHash estimate
is compared with the exact Jaccard similarity over several seeds, which is
what exposed the biased hash family. The bias-variance decomposition is
measured rather than derived, and its three terms are checked against the
total error.
