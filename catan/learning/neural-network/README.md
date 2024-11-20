# A small network

Forward pass, backward pass, and one check that matters.

## The gradient check

Every single parameter is nudged up and down, and the change in the error
divided by the step must equal the computed derivative. Over 26 parameters the
largest disagreement is **1.4 × 10⁻¹¹**.

This is the only test that reliably finds a wrong backward pass. A sign error
or a missing transpose usually leaves the network training, only slower, and
nothing else in the pipeline notices.

## XOR, with and without a hidden layer

| hidden units | error | correct of 4 |
|---:|---:|---:|
| 4 | 0.00026 | **4** |
| 0 | 0.250 | 3 |

Without a hidden layer the network is a single dividing line, and no line
separates XOR. The objection is correct and was famous; what was wrong was the
conclusion that it settles the matter.

## The gradient vanishes going backwards

The derivative of the logistic function is at most a quarter, so in a deep
network the error is multiplied by something below a quarter at every step
back. Measured over eight layers:

| | mean gradient |
|---|---:|
| last layer | 4.2 × 10⁻³ |
| first layer | 1.1 × 10⁻⁷ |

A factor of 39 326. The front layers effectively stop learning, which is why
deep networks use other activations, and why "deeper" was not simply a matter
of adding layers.

## The output has to match the target

Sigmoid with Bernoulli and binary cross-entropy, softmax with multinoulli and
discrete cross-entropy, linear with a Gaussian and squared error. The rule
underneath the table is that the output function has to cover the range of the
target: a sigmoid cannot predict a quantity that grows past one, and a linear
output cannot promise a probability.
