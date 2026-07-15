# The nearest different answer

What would have to change for the model to answer differently. The nearest
such point is found by search and checked against a full enumeration of the
grid.

## The norm decides what the answer looks like

Starting from (0.2, 0.2):

| norm | answer | features changed |
|---|---|---:|
| L1 | (0.502, **0.200**) | **1** |
| L2 | (0.441, 0.318) | 2 |

The first norm minimises the sum of the changes and therefore changes as few
features as possible, usually one. The second minimises the straight-line
distance and spreads the change over everything.

For someone who has to act, the first is usable and the second is not: "raise
your income by three hundred euros" can be followed, "change all seven of your
entries a little" cannot.

The start point has to lie on the search grid for this to be visible at all.
Without it, every answer appears to touch every feature, which is an artefact
of the discretisation and not a property of the norm.

## The nearest answer can be useless

| | distance | changes an unchangeable feature |
|---|---:|---|
| nearest | **0.269** | yes |
| nearest among the usable ones | 0.604 | no |

The model reacts most strongly to the feature that cannot be changed, so the
nearest counterfactual changes exactly that one. It is correctly computed and
worthless. Distance is the wrong objective until someone has said what is
allowed to change.

## What it does not explain

It says what would have to change. It does not say why the model decides as it
does, and it certainly does not say whether the decision is right. A model
using an inadmissible variable produces equally clean counterfactuals.
