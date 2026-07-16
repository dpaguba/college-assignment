# Interval bounds

Push a box through the network. For a linear layer the bound is exact
arithmetic: every positive weight takes the lower input bound and every
negative weight the upper one. The rectifier clips both bounds at zero.

The result is always sound, so it contains every possible output. It does not
promise to be tight: as soon as a value appears in two places, the arithmetic
treats it as two independent quantities and the range widens.

## Sound, and looser with depth

| depth | bound width | sampled width | looseness |
|---:|---:|---:|---:|
| 1 | 0.1007 | 0.0994 | 1.013 |
| 2 | 0.0238 | 0.0234 | 1.014 |
| 5 | 0.0138 | 0.0090 | 1.523 |
| 8 | 0.000192 | 0.0000715 | **2.682** |

Compared as a ratio, not a difference: the networks differ in scale by orders
of magnitude at different depths. The sampled width is itself an
underestimate, because a sample hits the corners of the box only by accident,
so the ratio is a lower bound on the looseness.

A single linear layer with no rectifier is exact: the gap against the corner
values is 0.0.

## Sound and useless at the same time

With a large input box and four layers, the bound comes out at (−1.81, 1.18)
while the sampled range is (−0.48, 0.19). The bound is correct and answers the
question "is the output always positive" with a shrug.

That is the normal case and the reason the work goes into sharper methods:
soundness is cheap, tightness is not.

## What a bound is worth

It is a statement about every input in the box, not about the ones that were
tried. That makes it different in kind from any test: no number of experiments
confirms it, and a single counterexample refutes it.
