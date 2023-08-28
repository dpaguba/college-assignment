# White, grey and black boxes

A white box is readable as a whole: a rule, a line, a shallow tree. A grey box
has a known structure whose behaviour can no longer be followed. A black box
offers only inputs and outputs.

## What the white box costs, measured twice

| Task | Decision stump | 5 nearest neighbours |
|---|---:|---:|
| sign of the product of two features | 51.8 % | 95.8 % |
| sign of one feature | 100 % | 98.5 % |

On the first task the interpretable model is useless, because a single
threshold splits the plane into half-planes and the target is two opposite
quadrants. On the second the interpretable model is the better one.

The trade-off between accuracy and interpretability is therefore not a law but
a property of the task, and it can be measured before the argument starts.

## The question underneath

Not accuracy but accountability: does somebody have to be able to contest the
decision. Where they do, the reason has to be checkable, and a post-hoc
explanation of a black box is a guess about the reason rather than the reason.
