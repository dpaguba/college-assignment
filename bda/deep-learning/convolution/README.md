# Convolution

The same small kernel applied at every position, so a pattern is recognised
wherever it occurs and the weights are shared.

The saving is the point:

| layer over 100 inputs, 8 outputs | parameters |
|---|---:|
| fully connected | 808 |
| convolutional with kernels of width 5 | 48 |

Shifting the input shifts the output, which the module checks directly. That
equivariance is what makes a convolution suit an image: a feature does not
have to be learned again for every position.

Pooling shrinks the signal and keeps the maximum of each window, which adds a
tolerance to small shifts on top of the equivariance. A stack of small
kernels grows the receptive field linearly with the depth, which is why deep
stacks replaced single large kernels: the same field, fewer parameters, more
non-linearity between them.
