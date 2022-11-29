# Graph mining

| Topic | |
|---|---|
| [pagerank](pagerank/) | the recursive popularity measure |
| [random-surfer](random-surfer/) | the walk behind the formula |
| [convergence](convergence/) | how fast, and what decides it |

The fourth lecture. The result worth carrying is the one the exercise graph
produces: node 3 has three incoming links and node 4 has the highest rank,
because node 4's one important source gives it everything while node 3's
sources are spread thin.

Everything here is checked twice. The iteration is compared with the exact
solution of the linear system, and both are compared with a random walk of
200 000 steps.
