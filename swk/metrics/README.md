# Metrics

Five modules for the measurement half of the quality lecture: LCOM, coupling,
size, coding standards, and a report that runs all of them over real code.

| Folder | What it measures |
|---|---|
| [lcom](lcom/) | cohesion inside a class, four variants |
| [coupling-and-cohesion](coupling-and-cohesion/) | dependencies between modules |
| [size-metrics](size-metrics/) | lines, nesting, complexity |
| [coding-standards](coding-standards/) | rules a build can fail on |
| [metrics-report](metrics-report/) | all of it, over a directory |

## The one sentence about metrics worth keeping

They point at places worth looking, and they do not know what they found.

Every module here says so in its own terms: LCOM4 counts responsibilities but
cannot tell a cohesive B-tree from a class that should be split, instability
is a direction and not a score, and cyclomatic complexity counts branching,
which is one source of difficulty out of several.

That is not a reason to skip them. It is the reason they are reported together
rather than reduced to a single number, and it is why the tool prints the
worst five of each rather than a grade.

## Verification

The three LCOM values the course publishes all come out exactly: 2/3 for the
exercise class, 0 for the cohesive one, 4/7 for the merged one. The rest was
checked by running it against this repository and reading what it found:
`while_language` most depended upon with no dependencies of its own, no
dependency cycles, and the complexity ranking picking out the three functions
that are in fact the hardest to follow.
