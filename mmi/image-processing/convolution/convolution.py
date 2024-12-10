"""Convolution: the operation almost every image filter is.

Slide a small kernel over the image, and each output pixel is the weighted sum
of its neighbourhood. Blur, sharpen, emboss and the first stage of every edge
detector are the same loop with different weights.

Two properties make it worth naming rather than just writing the loop. It is
linear and shift-invariant, so it is fully described by its response to a
single point, and in the frequency domain it becomes a multiplication, which is
why [fourier-transform](../fourier-transform/) is in this block at all.
"""

from __future__ import annotations

import math


def convolve(image, kernel, border="clamp"):
    """Correlate an image with a kernel.

    Strictly this is correlation: true convolution flips the kernel first. For
    the symmetric kernels used in filtering the two coincide, and for the
    asymmetric ones the sign convention is usually chosen to make correlation
    the intended operation anyway. The distinction matters when composing
    filters or comparing against a Fourier-domain product, where the flip is
    not optional.
    """
    height, width = len(image), len(image[0])
    k_height, k_width = len(kernel), len(kernel[0])
    offset_y, offset_x = k_height // 2, k_width // 2
    result = []

    for y in range(height):
        row = []
        for x in range(width):
            total = 0.0
            for ky in range(k_height):
                for kx in range(k_width):
                    sample = _sample(image, x + kx - offset_x, y + ky - offset_y, border)
                    total += kernel[ky][kx] * sample
            row.append(total)
        result.append(row)

    return result


def _sample(image, x, y, border):
    """Read a pixel, deciding what lies outside the image.

    There is no correct answer, only trade-offs. Zero padding darkens the
    edges, clamping repeats the border and biases towards it, wrapping assumes
    the image tiles, which is what the Fourier transform assumes and why the
    two agree only under that choice, and mirroring is the usual default
    because it introduces no new intensity and no artificial edge.
    """
    height, width = len(image), len(image[0])

    if border == "zero":
        if not (0 <= x < width and 0 <= y < height):
            return 0.0
    elif border == "clamp":
        x, y = max(0, min(width - 1, x)), max(0, min(height - 1, y))
    elif border == "wrap":
        x, y = x % width, y % height
    elif border == "mirror":
        x = _mirror(x, width)
        y = _mirror(y, height)

    return image[y][x]


def _mirror(index, size):
    """Reflect an index back inside the image."""
    if size == 1:
        return 0
    period = 2 * size - 2
    index = index % period
    return index if index < size else period - index


def box_kernel(size):
    """A uniform average, the cheapest blur and the worst behaved.

    Its frequency response is a sinc, which oscillates and goes negative, so a
    box blur inverts some frequency bands rather than attenuating them. Visible
    as ringing near sharp edges, and the reason it survives only where speed
    matters more than quality.
    """
    weight = 1.0 / (size * size)
    return [[weight] * size for _ in range(size)]


def gaussian_kernel(size, sigma=None):
    """A Gaussian blur, the only rotationally symmetric separable kernel.

    Its transform is another Gaussian, so it attenuates every frequency
    monotonically and rings at none of them. It is also the only kernel that
    creates no new extrema as the blur strengthens, which is why scale-space
    theory is built on it and not on anything else.
    """
    if sigma is None:
        sigma = size / 6.0

    centre = size // 2
    kernel = [[math.exp(-((x - centre) ** 2 + (y - centre) ** 2) / (2 * sigma ** 2))
               for x in range(size)] for y in range(size)]

    total = sum(sum(row) for row in kernel)
    return [[value / total for value in row] for row in kernel]


def gaussian_1d(size, sigma=None):
    """The one-dimensional Gaussian, for the separated form."""
    if sigma is None:
        sigma = size / 6.0

    centre = size // 2
    values = [math.exp(-((x - centre) ** 2) / (2 * sigma ** 2)) for x in range(size)]
    total = sum(values)
    return [value / total for value in values]


def separable_convolve(image, horizontal, vertical, border="clamp"):
    """Apply two one-dimensional passes instead of one two-dimensional kernel.

    A separable `k x k` kernel costs `2k` multiplications per pixel instead of
    `k^2`. At `k = 15` that is 30 against 225, and the results are identical,
    not approximately equal. The Gaussian and the box are separable; a general
    kernel is separable exactly when its matrix has rank one.
    """
    first = convolve(image, [list(horizontal)], border)
    return convolve(first, [[value] for value in vertical], border)


def sharpen_kernel(strength=1.0):
    """Unsharp masking as a single kernel.

    The image plus a multiple of the difference between it and its blur. What
    it really does is amplify high frequencies, so it amplifies noise at the
    same rate, and past a point it produces the bright halo along edges that
    marks an over-sharpened photograph.
    """
    return [[0.0, -strength, 0.0],
            [-strength, 1.0 + 4.0 * strength, -strength],
            [0.0, -strength, 0.0]]


LAPLACIAN = [[0.0, 1.0, 0.0],
             [1.0, -4.0, 1.0],
             [0.0, 1.0, 0.0]]
"""The discrete second derivative, summing to zero so flat areas map to zero."""

EMBOSS = [[-2.0, -1.0, 0.0],
          [-1.0, 1.0, 1.0],
          [0.0, 1.0, 2.0]]
"""A directional derivative plus one, which reads as lighting from one corner."""


def kernel_sum(kernel):
    """The sum of a kernel's weights, which is its response to a flat image.

    A blur must sum to 1 or it changes the overall brightness. A derivative
    must sum to 0 or a flat region produces a non-zero response, which is a
    brightness offset masquerading as structure.
    """
    return sum(sum(row) for row in kernel)


def median_filter(image, size=3):
    """Replace each pixel by the median of its neighbourhood.

    Not a convolution, and that is the point: the median is not linear, so it
    cannot be written as a kernel and it does not obey the frequency-domain
    argument. What it buys is that a single wildly wrong pixel does not move
    the median at all, while it moves any weighted average.

    Against salt-and-pepper noise this is the difference between removing the
    noise and smearing it around.
    """
    height, width = len(image), len(image[0])
    offset = size // 2
    result = []

    for y in range(height):
        row = []
        for x in range(width):
            window = [_sample(image, x + dx, y + dy, "clamp")
                      for dy in range(-offset, offset + 1)
                      for dx in range(-offset, offset + 1)]
            window.sort()
            row.append(window[len(window) // 2])
        result.append(row)

    return result


def rank(matrix, tolerance=1e-9):
    """Numerical rank by Gaussian elimination, to test separability."""
    rows = [list(row) for row in matrix]
    height, width = len(rows), len(rows[0])
    result = 0

    for column in range(width):
        pivot = None
        for row in range(result, height):
            if abs(rows[row][column]) > tolerance:
                pivot = row
                break
        if pivot is None:
            continue

        rows[result], rows[pivot] = rows[pivot], rows[result]
        divisor = rows[result][column]
        rows[result] = [value / divisor for value in rows[result]]

        for row in range(height):
            if row != result and abs(rows[row][column]) > tolerance:
                factor = rows[row][column]
                rows[row] = [a - factor * b for a, b in zip(rows[row], rows[result])]

        result += 1

    return result


def difference(first, second):
    """Largest absolute difference between two images."""
    return max(abs(a - b)
               for row_first, row_second in zip(first, second)
               for a, b in zip(row_first, row_second))
