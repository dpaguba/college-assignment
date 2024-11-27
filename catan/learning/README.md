# Learning

| Module | Topic |
|---|---|
| [bias-variance](bias-variance/) | the decomposition and where it stops |
| [overfitting](overfitting/) | the two curves and the turning point |
| [curse-of-dimensionality](curse-of-dimensionality/) | what breaks and what does not |
| [decision-tree](decision-tree/) | splits, checked against a search |
| [random-forest](random-forest/) | why two sources of randomness |
| [neural-network](neural-network/) | backpropagation, checked against differences |
| [optimisers](optimisers/) | six rules against their published forms |

The part of the deck taken from the machine learning lecture, minus what is
already covered under `docan/classification`. Every module is built around a
check that could fail: the three parts of the error have to add up, the
training error has to fall with every degree, the volume of the ball has to
match two derivations, the split has to match an exhaustive search, the
gradient has to match finite differences, and each update rule has to match
the paper it comes from.

The gradient check is the one to keep: a wrong backward pass still trains, so
nothing but finite differences finds it.
