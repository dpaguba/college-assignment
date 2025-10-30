# OLAP

OLAP is about access to data and navigation through it. The cube has
qualitative dimensions on its axes and quantitative measures inside.

| Module | Topic |
|---|---|
| [cube](cube/) | the hypercube built from the project table |
| [roll-up-drill-down](roll-up-drill-down/) | changing the level of aggregation |
| [slice-and-dice](slice-and-dice/) | cutting the cube down |
| [rotation](rotation/) | the same numbers, different axes |
| [drill-through](drill-through/) | from a figure back to the rows |
| [additivity](additivity/) | which measure may be summed over which axis |

The six operations of the lecture are exactly the first five modules plus
drill-down. The sixth module is not an operation but the condition under
which they give the right answer, and it is the one the lecture does not
spell out.

Every operation is verified against a plain scan of the rows, and drill-down
is verified against roll-up: the parts must add up to the whole on every
axis. Rotation is verified by doing it twice.
