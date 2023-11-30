# Deep learning

| Topic | |
|---|---|
| [training-improvements](training-improvements/) | four problems and their answers |
| [convolution](convolution/) | shared weights, and what they buy |
| [interpretability](interpretability/) | which feature the accuracy came from |

Chapter six. The basic network is in
[gdw/learning/neural-networks](../../gdw/learning/neural-networks/); this
block is about what makes a deep one work and what to ask of it afterwards.

The two numbers to carry: ten logistic layers keep one part in a million of
the gradient, and a convolutional layer over a hundred inputs uses 48
parameters where a dense one uses 808.

The result that is not a number: a model can be perfectly accurate and use
the wrong feature, and only an importance measure says so.
