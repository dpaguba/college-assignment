"""Edge detection: finding where the image changes fast.

An edge is a large derivative, so every detector is a derivative estimator
followed by a decision. The differences between them are entirely in how they
estimate the derivative of a signal that is sampled and noisy, and in how they
decide what counts as large.

The hard part is noise. Differentiating amplifies high frequencies, and noise
is high frequency, so a derivative taken naively reports the noise and not the
edge. Every method here answers that in some way, and Canny answers it best.
"""

from __future__ import annotations

import math

SOBEL_X = [[-1.0, 0.0, 1.0],
           [-2.0, 0.0, 2.0],
           [-1.0, 0.0, 1.0]]
"""Horizontal derivative with a `[1 2 1]` smoothing across it, hence separable."""

SOBEL_Y = [[-1.0, -2.0, -1.0],
           [0.0, 0.0, 0.0],
           [1.0, 2.0, 1.0]]
"""Vertical derivative, the transpose of `SOBEL_X`."""

PREWITT_X = [[-1.0, 0.0, 1.0],
             [-1.0, 0.0, 1.0],
             [-1.0, 0.0, 1.0]]
"""The same with uniform smoothing, which weights the diagonal neighbours more."""

PREWITT_Y = [[-1.0, -1.0, -1.0],
             [0.0, 0.0, 0.0],
             [1.0, 1.0, 1.0]]
"""Vertical Prewitt."""

ROBERTS_X = [[1.0, 0.0], [0.0, -1.0]]
"""A 2x2 diagonal difference: cheapest, most noise sensitive, half a pixel off."""

ROBERTS_Y = [[0.0, 1.0], [-1.0, 0.0]]
"""The other diagonal."""


def convolve(image, kernel):
    """Correlate an image with a kernel, clamping at the border."""
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
                    sy = max(0, min(height - 1, y + ky - offset_y))
                    sx = max(0, min(width - 1, x + kx - offset_x))
                    total += kernel[ky][kx] * image[sy][sx]
            row.append(total)
        result.append(row)

    return result


def gradient(image, kernel_x=None, kernel_y=None):
    """Magnitude and direction of the image gradient at every pixel.

    The magnitude is where the edge is, the direction is which way it faces,
    and both are needed: thinning an edge to one pixel means comparing along
    the direction, which is what non-maximum suppression does.
    """
    kernel_x = SOBEL_X if kernel_x is None else kernel_x
    kernel_y = SOBEL_Y if kernel_y is None else kernel_y

    gx = convolve(image, kernel_x)
    gy = convolve(image, kernel_y)

    magnitude = [[math.hypot(gx[y][x], gy[y][x]) for x in range(len(image[0]))]
                 for y in range(len(image))]
    direction = [[math.atan2(gy[y][x], gx[y][x]) for x in range(len(image[0]))]
                 for y in range(len(image))]

    return magnitude, direction


def non_maximum_suppression(magnitude, direction):
    """Keep only pixels that are a local maximum along the gradient direction.

    A gradient operator reports a wide ridge across an edge, several pixels
    thick. Thinning it by comparing each pixel to its two neighbours **along**
    the gradient, not around it, leaves a one-pixel line, which is what a
    detector is supposed to produce.

    The direction is quantised to four cases, because comparing against
    interpolated neighbours is more expensive and rarely changes the answer.
    """
    height, width = len(magnitude), len(magnitude[0])
    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            angle = math.degrees(direction[y][x]) % 180

            if angle < 22.5 or angle >= 157.5:
                neighbours = (magnitude[y][x - 1], magnitude[y][x + 1])
            elif angle < 67.5:
                neighbours = (magnitude[y - 1][x + 1], magnitude[y + 1][x - 1])
            elif angle < 112.5:
                neighbours = (magnitude[y - 1][x], magnitude[y + 1][x])
            else:
                neighbours = (magnitude[y - 1][x - 1], magnitude[y + 1][x + 1])

            if magnitude[y][x] >= max(neighbours):
                result[y][x] = magnitude[y][x]

    return result


def hysteresis(image, low, high):
    """Two thresholds: strong pixels are edges, weak ones only if connected.

    One threshold cannot work. Set it high and long edges break into dashes
    wherever the contrast dips; set it low and noise becomes edges. Hysteresis
    uses the high threshold to decide what an edge is and the low one to decide
    how far it continues, which is the observation that edges are connected and
    noise is not.
    """
    height, width = len(image), len(image[0])
    result = [[0.0] * width for _ in range(height)]
    stack = []

    for y in range(height):
        for x in range(width):
            if image[y][x] >= high:
                result[y][x] = 1.0
                stack.append((x, y))

    while stack:
        x, y = stack.pop()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    if result[ny][nx] == 0.0 and image[ny][nx] >= low:
                        result[ny][nx] = 1.0
                        stack.append((nx, ny))

    return result


def gaussian_kernel(size, sigma):
    """A normalised Gaussian, for the smoothing step."""
    centre = size // 2
    kernel = [[math.exp(-((x - centre) ** 2 + (y - centre) ** 2) / (2 * sigma ** 2))
               for x in range(size)] for y in range(size)]
    total = sum(sum(row) for row in kernel)
    return [[value / total for value in row] for row in kernel]


def canny(image, sigma=1.0, low=0.1, high=0.2):
    """Smooth, differentiate, thin, threshold with hysteresis.

    Canny derived the steps rather than assembling them: he wrote down what a
    good detector should do, one edge per edge, located correctly, few false
    positives, and showed the optimum is close to the derivative of a Gaussian
    followed by exactly this thinning and thresholding.

    Sigma is the one real parameter. Small sigma finds fine detail and noise;
    large sigma finds only strong edges and displaces curved ones outwards.
    """
    size = max(3, int(sigma * 6) | 1)
    smoothed = convolve(image, gaussian_kernel(size, sigma))
    magnitude, direction = gradient(smoothed)
    thinned = non_maximum_suppression(magnitude, direction)

    peak = max(max(row) for row in thinned) or 1.0
    normalised = [[value / peak for value in row] for row in thinned]

    return hysteresis(normalised, low, high)


LAPLACIAN = [[0.0, 1.0, 0.0],
             [1.0, -4.0, 1.0],
             [0.0, 1.0, 0.0]]
"""The second derivative, whose zero crossings are the edges."""


def laplacian_of_gaussian(image, sigma=1.0):
    """Smooth first, then take the second derivative.

    The second derivative crosses zero where the first is at a maximum, so the
    edge is a zero crossing rather than a peak. That makes localisation exact
    and thinning unnecessary, and it makes the operator useless on noisy input
    without the smoothing step, because the second derivative amplifies noise
    even harder than the first.
    """
    size = max(3, int(sigma * 6) | 1)
    smoothed = convolve(image, gaussian_kernel(size, sigma))
    return convolve(smoothed, LAPLACIAN)


def zero_crossings(image, threshold=0.0):
    """Pixels where the second derivative changes sign.

    A sign change between neighbours means the true zero is between them, so
    the edge is localised to sub-pixel accuracy in principle. The threshold on
    the size of the jump is what stops every noise-induced sign flip from
    counting.
    """
    height, width = len(image), len(image[0])
    result = [[0.0] * width for _ in range(height)]

    for y in range(1, height - 1):
        for x in range(1, width - 1):
            centre = image[y][x]
            for dy, dx in ((0, 1), (1, 0), (1, 1), (1, -1)):
                neighbour = image[y + dy][x + dx]
                if centre * neighbour < 0 and abs(centre - neighbour) > threshold:
                    result[y][x] = 1.0
                    break

    return result


def count_edges(binary):
    """Number of pixels marked as an edge."""
    return sum(1 for row in binary for value in row if value > 0)


def edge_thickness(binary, row):
    """Widths of the runs of edge pixels along one row.

    The measurement that shows what non-maximum suppression is for: a raw
    gradient threshold gives runs several pixels wide, and a thinned detector
    gives runs of one.
    """
    runs = []
    current = 0

    for value in binary[row]:
        if value > 0:
            current += 1
        elif current:
            runs.append(current)
            current = 0

    if current:
        runs.append(current)
    return runs


def threshold(image, level):
    """Binarise an image at a level."""
    return [[1.0 if value >= level else 0.0 for value in row] for row in image]
