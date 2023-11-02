"""Convolution: the same small kernel applied everywhere.

A kernel slides over the input and computes a weighted sum at each position,
so a pattern is recognised wherever it occurs and the weights are shared
across positions. That sharing is the whole saving: a fully connected layer
on a hundred inputs with eight outputs needs 808 parameters, and eight
kernels of width five need 48.

Shifting the input shifts the output, which is what "translation equivariant"
means and why a convolution suits an image.
"""


def apply(signal, kernel):
    """The valid convolution of a signal with a kernel."""
    width = len(kernel)
    return [sum(signal[index + offset] * kernel[offset]
                for offset in range(width))
            for index in range(len(signal) - width + 1)]


def max_pool(signal, size):
    """The maximum of each window, which shrinks the signal."""
    return [max(signal[index:index + size])
            for index in range(0, len(signal) - size + 1, size)]


def parameter_count(width, kernel, filters):
    """The parameters of a convolutional layer against a dense one."""
    return {"convolutional": filters * (kernel + 1),
            "fully connected": filters * (width + 1),
            "ratio": (width + 1) / (kernel + 1)}


def receptive_field(layers, kernel):
    """How much of the input one output position depends on.

    It grows linearly with the depth for a fixed kernel, which is why deep
    stacks of small kernels replaced single large ones: the same field with
    fewer parameters and more non-linearity.
    """
    return 1 + layers * (kernel - 1)
