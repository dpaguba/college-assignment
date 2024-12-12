"""The discrete Fourier transform: an image as a sum of waves.

Every image is a sum of sinusoids, and the transform gives the amplitude and
phase of each. Nothing is lost, the transform is invertible, and what changes
is which questions are easy: "how much fine detail is there" is a scan of the
spectrum and an awkward computation on the pixels.

The reason it matters for filtering is the convolution theorem. Convolution in
space is multiplication in frequency, so a filter that costs `k^2` per pixel
becomes one multiplication per frequency, and the whole design of a filter
becomes a choice of which frequencies to keep.
"""

from __future__ import annotations

import cmath
import math


def dft(signal):
    """The definition, `O(n^2)`.

    Kept because it is the specification the FFT is checked against, and
    because for small inputs the constant factor makes it faster.
    """
    n = len(signal)
    return [sum(signal[k] * cmath.exp(-2j * math.pi * index * k / n) for k in range(n))
            for index in range(n)]


def idft(spectrum):
    """The inverse, differing only in the sign of the exponent and a scale."""
    n = len(spectrum)
    return [sum(spectrum[k] * cmath.exp(2j * math.pi * index * k / n)
                for k in range(n)) / n for index in range(n)]


def fft(signal):
    """Cooley-Tukey radix-2, `O(n log n)`, for power-of-two lengths.

    Split into even and odd indices. Each half is a transform of half the
    length, and the two combine with one multiplication per output. Because the
    same twiddle factors repeat across the recursion, the `n^2` products of the
    definition collapse into `n log n`.

    The speedup is what made frequency-domain filtering practical: at `n = 1024`
    it is a factor of about a hundred, and the factor grows with the input.
    """
    n = len(signal)
    if n <= 1:
        return list(signal)
    if n & (n - 1):
        return dft(signal)

    even = fft(signal[0::2])
    odd = fft(signal[1::2])
    factors = [cmath.exp(-2j * math.pi * index / n) * odd[index] for index in range(n // 2)]

    return ([even[index] + factors[index] for index in range(n // 2)]
            + [even[index] - factors[index] for index in range(n // 2)])


def ifft(spectrum):
    """The inverse FFT, by conjugating, transforming and conjugating back."""
    n = len(spectrum)
    conjugated = [value.conjugate() for value in spectrum]
    result = fft(conjugated)
    return [value.conjugate() / n for value in result]


def fft2(image):
    """Two-dimensional transform, as rows then columns.

    The 2D transform is separable, so it never needs to be written out:
    transform every row, then every column of the result. Both orders give the
    same answer, which is the same separability argument as the Gaussian blur
    in [convolution](../convolution/).
    """
    rows = [fft(row) for row in image]
    height, width = len(rows), len(rows[0])

    columns = []
    for x in range(width):
        column = fft([rows[y][x] for y in range(height)])
        columns.append(column)

    return [[columns[x][y] for x in range(width)] for y in range(height)]


def ifft2(spectrum):
    """The inverse two-dimensional transform."""
    rows = [ifft(row) for row in spectrum]
    height, width = len(rows), len(rows[0])

    columns = []
    for x in range(width):
        columns.append(ifft([rows[y][x] for y in range(height)]))

    return [[columns[x][y] for x in range(width)] for y in range(height)]


def magnitude(spectrum):
    """The amplitude of each frequency, which is what a spectrum image shows."""
    return [[abs(value) for value in row] for row in spectrum]


def phase(spectrum):
    """The phase of each frequency, which is where the structure actually is."""
    return [[cmath.phase(value) for value in row] for row in spectrum]


def shift(spectrum):
    """Move the zero frequency to the centre, for display.

    The transform puts the zero frequency in the corner and wraps the negative
    frequencies around to the far side. Shifting by half the size in each
    direction makes the picture symmetric about the centre, which is the only
    reason it is ever done.
    """
    height, width = len(spectrum), len(spectrum[0])
    half_y, half_x = height // 2, width // 2
    return [[spectrum[(y + half_y) % height][(x + half_x) % width]
             for x in range(width)] for y in range(height)]


def low_pass(spectrum, radius):
    """Keep frequencies within a radius of the centre, discard the rest.

    A blur, described from the other side. The sharp cutoff is what makes it a
    bad blur: an ideal low pass in frequency is a sinc in space, and the sinc's
    ringing shows up as ripples around every edge. Real filters taper.
    """
    height, width = len(spectrum), len(spectrum[0])
    result = []

    for y in range(height):
        row = []
        for x in range(width):
            dy = min(y, height - y)
            dx = min(x, width - x)
            row.append(spectrum[y][x] if math.hypot(dx, dy) <= radius else 0j)
        result.append(row)

    return result


def high_pass(spectrum, radius):
    """Discard the low frequencies, keeping the detail.

    The zero frequency is the average brightness, so removing it makes the
    image average to zero and turns everything flat into grey. That is why a
    high-passed image looks like an embossing rather than like a photograph.
    """
    height, width = len(spectrum), len(spectrum[0])
    result = []

    for y in range(height):
        row = []
        for x in range(width):
            dy = min(y, height - y)
            dx = min(x, width - x)
            row.append(0j if math.hypot(dx, dy) <= radius else spectrum[y][x])
        result.append(row)

    return result


def convolve_fourier(image, kernel):
    """Convolve by multiplying spectra, the theorem applied.

    The kernel is zero-padded to the image size and its centre moved to the
    origin, because the transform treats index 0 as the centre of the kernel
    and the image as periodic. Getting that wrap wrong shifts the result by
    half the kernel, which looks like a bug in the filter rather than in the
    indexing.

    The result matches direct convolution with wraparound borders, and only
    with wraparound: the frequency domain has no concept of an edge, so it
    always assumes the image tiles.
    """
    height, width = len(image), len(image[0])
    k_height, k_width = len(kernel), len(kernel[0])
    offset_y, offset_x = k_height // 2, k_width // 2

    padded = [[0j] * width for _ in range(height)]
    for y in range(k_height):
        for x in range(k_width):
            padded[(y - offset_y) % height][(x - offset_x) % width] += kernel[y][x]

    image_spectrum = fft2([[complex(value) for value in row] for row in image])
    kernel_spectrum = fft2(padded)

    product = [[image_spectrum[y][x] * kernel_spectrum[y][x] for x in range(width)]
               for y in range(height)]

    return [[value.real for value in row] for row in ifft2(product)]


def power_spectrum(spectrum):
    """Squared magnitudes, which is what Parseval's theorem is about."""
    return sum(abs(value) ** 2 for row in spectrum for value in row)


def energy(image):
    """Sum of squared pixel values.

    Parseval's theorem says this equals the total power in the spectrum divided
    by the number of samples. It is the statement that the transform is a
    rotation: it moves the information without changing how much there is.
    """
    return sum(abs(value) ** 2 for row in image for value in row)


def dominant_frequencies(spectrum, count=5):
    """The strongest frequencies, excluding the constant term.

    The zero frequency is the average brightness and dominates every natural
    image, so it is always excluded when looking for structure.
    """
    height, width = len(spectrum), len(spectrum[0])
    entries = []

    for y in range(height):
        for x in range(width):
            if y == 0 and x == 0:
                continue
            entries.append((abs(spectrum[y][x]), (y, x)))

    entries.sort(reverse=True)
    return entries[:count]
