# Size metrics

Lines of code and its relatives. The lecture opens the metrics section with
LOC, calls it the simplest indicator of complexity, and immediately lists the
family: number of classes, number of methods, number of anything.

## Why they are kept and distrusted

Free to collect and comparable over time, which is worth a lot. And they
measure typing, not difficulty: the same function in two styles differs by a
factor of two in lines and not at all in what it does.

The ratios are more informative than the counts. `comment_ratio` says whether
anything is documented at all; a count of comment lines says only how big the
file is.

## Nesting beats length

`nesting_depth` is the better signal, and the one that matches how code reads:
three levels are followable, six are not. Length can always be cut by moving
code elsewhere; nesting cannot be hidden that way.

## Cyclomatic complexity for Python

`cyclomatic_complexity` counts decision points: conditionals, loops, exception
handlers, boolean operators and comprehension filters, plus one. On a control
flow graph that equals `e - n + 2p`, which is how the
[program analysis](../../program-analysis/cyclomatic-complexity/) folder
computes it for the While language. Counting decisions reaches the same number
without building the graph.

## Measured on this repository

| | swk | dap2 |
|---|---|---|
| files | 26 | 100 |
| lines | 4979 | 7700 |
| documented share | 33% | 36% |
| longest function | 61 | 108 |
| deepest nesting | 5 | 6 |

The most complex functions here are the dataflow worklist (23), the linear
arithmetic conversions (18) and the symbolic execution walk (17). All three
are the places where a bug would be hardest to find, which is the one thing
the number is genuinely good at pointing out.
