"""Image restoration: undoing a known degradation.

Restoration is not enhancement. Enhancement makes an image look better by any
means; restoration assumes a model of what damaged it and tries to invert that
model. The model here is the standard one: the observed image is the true image
convolved with a blur, plus noise.

    g = h * f + n

Inverting the convolution is a division in the frequency domain, which is
trivial to write and almost useless to apply, because the blur destroys the
high frequencies and the division amplifies whatever is left there, which is
noise. Everything in this module is a way of dealing with that.
"""

from __future__ import annotations

import cmath
import math
import random


def fft(signal):
    """Radix-2 FFT. See [fourier-transform](../fourier-transform/) for why."""
    n = len(signal)
    if n <= 1:
        return list(signal)

    even, odd = fft(signal[0::2]), fft(signal[1::2])
    factors = [cmath.exp(-2j * math.pi * index / n) * odd[index] for index in range(n // 2)]

    return ([even[index] + factors[index] for index in range(n // 2)]
            + [even[index] - factors[index] for index in range(n // 2)])


def ifft(spectrum):
    """The inverse transform."""
    n = len(spectrum)
    result = fft([value.conjugate() for value in spectrum])
    return [value.conjugate() / n for value in result]


def fft2(image):
    """Two-dimensional transform, rows then columns."""
    rows = [fft([complex(value) for value in row]) for row in image]
    height, width = len(rows), len(rows[0])
    columns = [fft([rows[y][x] for y in range(height)]) for x in range(width)]
    return [[columns[x][y] for x in range(width)] for y in range(height)]


def ifft2(spectrum):
    """The inverse two-dimensional transform."""
    rows = [ifft(row) for row in spectrum]
    height, width = len(rows), len(rows[0])
    columns = [ifft([rows[y][x] for y in range(height)]) for x in range(width)]
    return [[columns[x][y] for x in range(width)] for y in range(height)]


def pad_kernel(kernel, height, width):
    """Place a kernel in an image-sized array with its centre at the origin.

    The transform treats index 0 as the centre and the array as periodic, so
    the kernel has to be wrapped around the corners. Doing it wrong shifts the
    restored image by half the kernel, which looks like the restoration failed
    rather than like the indexing did.
    """
    k_height, k_width = len(kernel), len(kernel[0])
    offset_y, offset_x = k_height // 2, k_width // 2
    padded = [[0.0] * width for _ in range(height)]

    for y in range(k_height):
        for x in range(k_width):
            padded[(y - offset_y) % height][(x - offset_x) % width] += kernel[y][x]

    return padded


def degrade(image, kernel, noise_sigma=0.0, seed=None):
    """Apply the degradation model: blur, then add Gaussian noise.

    Used to make test data where the answer is known, which is the only way to
    measure a restoration properly. On a real photograph there is nothing to
    compare against, and every method looks plausible.
    """
    if seed is not None:
        random.seed(seed)

    height, width = len(image), len(image[0])
    spectrum = fft2(image)
    kernel_spectrum = fft2(pad_kernel(kernel, height, width))

    blurred = ifft2([[spectrum[y][x] * kernel_spectrum[y][x] for x in range(width)]
                     for y in range(height)])

    return [[value.real + (random.gauss(0, noise_sigma) if noise_sigma else 0.0)
             for value in row] for row in blurred]


def inverse_filter(image, kernel, epsilon=1e-12):
    """Divide by the blur's spectrum. Exact without noise, useless with it.

    Where the blur's transfer function is near zero, the division multiplies by
    an enormous number. With no noise there is nothing there to amplify and the
    result is exact. With even a trace of noise, those frequencies dominate the
    output completely and the image disappears under a texture that has nothing
    to do with it.
    """
    height, width = len(image), len(image[0])
    spectrum = fft2(image)
    kernel_spectrum = fft2(pad_kernel(kernel, height, width))

    restored = []
    for y in range(height):
        row = []
        for x in range(width):
            value = kernel_spectrum[y][x]
            row.append(spectrum[y][x] / value if abs(value) > epsilon else 0j)
        restored.append(row)

    return [[value.real for value in row] for row in ifft2(restored)]


def pseudo_inverse(image, kernel, cutoff=0.1):
    """The inverse filter, but leaving alone the frequencies the blur destroyed.

    One threshold: where the blur's response is below the cutoff, do not
    divide. Crude, and it works, because the failure of the inverse filter is
    entirely concentrated in those frequencies. The price is that the detail
    they carried is not recovered, only prevented from exploding.
    """
    height, width = len(image), len(image[0])
    spectrum = fft2(image)
    kernel_spectrum = fft2(pad_kernel(kernel, height, width))

    restored = []
    for y in range(height):
        row = []
        for x in range(width):
            value = kernel_spectrum[y][x]
            row.append(spectrum[y][x] / value if abs(value) >= cutoff else spectrum[y][x])
        restored.append(row)

    return [[value.real for value in row] for row in ifft2(restored)]


def wiener_filter(image, kernel, noise_to_signal=0.01):
    """The minimum mean square error restoration for a known noise level.

    Multiply by `conj(H) / (|H|^2 + K)` instead of dividing by `H`. Where the
    blur is strong the term behaves like the inverse filter; where the blur
    killed the signal, `K` dominates and the gain goes to zero instead of to
    infinity. The transition is smooth rather than a threshold, which is why it
    beats the pseudo-inverse.

    `K` is the noise-to-signal power ratio. Setting it to zero recovers the
    plain inverse filter exactly, which is the sense in which this is the same
    filter with the noise accounted for.
    """
    height, width = len(image), len(image[0])
    spectrum = fft2(image)
    kernel_spectrum = fft2(pad_kernel(kernel, height, width))

    restored = []
    for y in range(height):
        row = []
        for x in range(width):
            value = kernel_spectrum[y][x]
            power = abs(value) ** 2
            row.append(spectrum[y][x] * value.conjugate() / (power + noise_to_signal))
        restored.append(row)

    return [[value.real for value in row] for row in ifft2(restored)]


def motion_blur_kernel(length, horizontal=True):
    """A straight line of equal weights, the model of a camera pan.

    Its transfer function is a sinc. On a sampled image its zeros land on
    actual frequencies only when the blur length divides the image width: at
    length 8 on a 32-wide image the response is exactly 0 at k = 4, 8, 12, 16,
    20, 24 and 28, while at length 7 the smallest value is 0.018 and nothing
    vanishes.

    Where it does vanish the information is not attenuated but gone, and no
    filter recovers it. Division by zero has no answer, and that is a fact
    about the blur rather than about the algorithm.
    """
    weight = 1.0 / length
    if horizontal:
        return [[weight] * length]
    return [[weight] for _ in range(length)]


def gaussian_kernel(size, sigma):
    """A Gaussian blur, whose transfer function is a Gaussian with no zeros.

    Nothing is ever exactly destroyed, only attenuated, so in exact arithmetic
    it is fully invertible. In floating point with noise it is not, which is
    the whole point of the module.
    """
    centre = size // 2
    kernel = [[math.exp(-((x - centre) ** 2 + (y - centre) ** 2) / (2 * sigma ** 2))
               for x in range(size)] for y in range(size)]
    total = sum(sum(row) for row in kernel)
    return [[value / total for value in row] for row in kernel]


def rmse(first, second):
    """Root mean square difference between two images."""
    total = sum((a - b) ** 2 for row_a, row_b in zip(first, second)
                for a, b in zip(row_a, row_b))
    count = len(first) * len(first[0])
    return math.sqrt(total / count)


def psnr(first, second, peak=1.0):
    """Peak signal-to-noise ratio in decibels, the usual reported number.

    Above about 40 dB the difference is invisible; below 20 dB it is obvious.
    It correlates only loosely with what a viewer notices, which is why it is
    always reported alongside the pictures and never instead of them.
    """
    error = rmse(first, second)
    if error < 1e-15:
        return float("inf")
    return 20 * math.log10(peak / error)


def transfer_function(kernel, height, width):
    """The magnitudes of a blur's frequency response.

    Reading off its minimum says immediately whether the blur is invertible in
    principle: a zero means those frequencies were deleted, and a small value
    means restoring them multiplies the noise there by the reciprocal.
    """
    spectrum = fft2(pad_kernel(kernel, height, width))
    return [[abs(value) for value in row] for row in spectrum]
