# Neural networks

A neuron computes a weighted sum and fires when it passes a threshold, so its
decision boundary is a straight line and its decision region a half plane.
Conjunction needs weights 1, 1 and threshold 1.5: only both inputs together
reach it.

## Why one neuron cannot do equivalence

The inputs with output 1 are (0,0) and (1,1); those with output 0 are (0,1)
and (1,0). The two segments cross, so the convex hulls of the two classes
meet, at distance exactly 0. No line has one class on each side.

The test is the same hull-distance computation used by the support vector
module, and it is checked against a grid search over weights and thresholds:
both agree that and, or, nand and nor are separable and that exclusive-or and
equivalence are not.

## Two layers

The hidden layer computes the conjunction and the nor of the inputs. In that
new pair of coordinates the four cases land on three points and the two
classes come apart, so an or-neuron finishes the job. The module reports the
separability before and after the hidden layer: not separable in the input
space, separable in the hidden space.

That is what a hidden layer does. It is not more capacity in a vague sense,
it is a change of coordinates in which a linear boundary is enough.

Trained instead with backpropagation and logistic units, the squared error
falls from 1.09 to 0.0005 over the four cases.
