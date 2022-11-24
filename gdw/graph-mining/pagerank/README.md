# PageRank

The rank of a page is the probability that a surfer following links at random
and occasionally jumping is looking at it.

On the exercise graph:

| node | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| incoming links | 1 | 2 | 3 | 2 | 1 |
| rank | 0.066 | 0.123 | 0.311 | **0.330** | 0.170 |

Node 3 has the most incoming links and node 4 has the highest rank. The
reason is where the links come from: node 4's single most important source is
node 3, which has one outgoing link and gives it everything, while node 3's
sources split their rank several ways.

That is the whole idea of the algorithm in one example. Counting links is a
popularity measure; PageRank is a recursive one, and the two disagree on a
graph of five nodes.

## Two details that are not details

The damping factor is the chance of following a link rather than jumping, and
without it a sink absorbs all the probability: the module shows a two-node
graph where node 2 ends with more than 0.9. A page with no outgoing links
leaks probability unless its rank is redistributed, which the implementation
does explicitly.

The power iteration is checked against the exact solution of the linear
system, so convergence to something is distinguished from convergence to the
right thing.
