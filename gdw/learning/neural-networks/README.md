# Neural networks

A single neuron draws a line, so it learns anything a line separates. The
perceptron rule converges on the conjunction and never converges on the
exclusive or, which the module demonstrates by running it.

A hidden layer fixes it, and only because the activation is not linear.
Composing linear maps gives a linear map, so a stack of linear layers is a
single layer however deep it is, which the module checks numerically by
comparing a two-layer linear network with the single layer holding the
product of its matrices.

## Why depth was hard

The derivative of the logistic function is at most a quarter, so the gradient
is multiplied by at most that at every layer:

| depth | share of the gradient surviving |
|---|---:|
| 2 | 1/16 |
| 10 | 1/1 048 576 |

That is the vanishing gradient, and it is why deep networks needed a
different activation before they could be trained at all.
