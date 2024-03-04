"""Dithering: trading spatial resolution for colour resolution.

Quantising a smooth gradient to few levels produces visible bands. Dithering
scatters the rounding error instead of letting it accumulate, so the average
over a small area is right even though every single pixel is wrong. The eye
integrates, and the banding disappears.

The lecture splits the problem in two, and so does this module:

- **colour quantisation**: which few colours to use, answered by the median cut
  algorithm
- **colour replacement**: which of them to put in each pixel, answered by
  ordered or error-diffusion dithering
"""

from __future__ import annotations

from dataclasses import dataclass


def median_cut(colours, count):
    """Choose a palette of the requested size by splitting boxes at the median.

    Put every colour in one box. Repeatedly take the box with the **longest
    side**, split it at the median along that side, and stop when there are
    enough boxes. The palette is the average of each box.

    Splitting at the median rather than the midpoint is what makes it adaptive:
    an image that is mostly sky spends its palette on shades of blue, because
    that is where the colours actually are. Splitting the longest side is what
    keeps the boxes from degenerating into slabs.

    The count is rounded down to a power of two, since each round doubles the
    number of boxes.
    """
    if not colours:
        return []

    boxes = [list(colours)]

    while len(boxes) < count:
        target = max(boxes, key=_box_length)
        if len(target) < 2:
            break

        boxes.remove(target)
        first, second = _split(target)
        boxes.extend([first, second])

    return [_average(box) for box in boxes if box]


def _box_length(box):
    """The longest side of the bounding box of a set of colours."""
    if not box:
        return 0
    return max(max(colour[channel] for colour in box) - min(colour[channel] for colour in box)
               for channel in range(3))


def _split(box):
    """Split a box at the median of its longest channel."""
    channel = max(range(3),
                  key=lambda index: max(colour[index] for colour in box)
                  - min(colour[index] for colour in box))
    ordered = sorted(box, key=lambda colour: colour[channel])
    middle = len(ordered) // 2
    return ordered[:middle], ordered[middle:]


def _average(box):
    """The mean colour of a box, which becomes the palette entry."""
    return tuple(sum(colour[channel] for colour in box) / len(box) for channel in range(3))


def nearest(palette, colour):
    """The palette entry closest to a colour, by squared distance in RGB.

    Squared distance in RGB is the cheap choice and not the perceptual one.
    Doing it in Lab, which
    [colour-models](../colour-models/) can compute, matches the eye better and
    costs a conversion per comparison.
    """
    return min(palette, key=lambda entry: sum((a - b) ** 2 for a, b in zip(entry, colour)))


BAYER_4 = ((0, 8, 2, 10),
           (12, 4, 14, 6),
           (3, 11, 1, 9),
           (15, 7, 13, 5))
"""The 4x4 Bayer matrix: a fixed threshold pattern that spreads error in space."""


def ordered_dither(image, levels, matrix=BAYER_4):
    """Dither by comparing each pixel against a position-dependent threshold.

    The matrix shifts the rounding decision by a small amount that depends on
    where the pixel is, so a constant grey between two levels comes out as a
    regular pattern of both. No state is carried between pixels, which makes it
    parallel and fast, and gives it the characteristic crosshatch texture.
    """
    size = len(matrix)
    step = 1 / (levels - 1)
    result = []

    for y, row in enumerate(image):
        output = []
        for x, value in enumerate(row):
            threshold = (matrix[y % size][x % size] + 0.5) / (size * size) - 0.5
            shifted = value + threshold * step
            index = max(0, min(levels - 1, round(shifted / step)))
            output.append(index * step)
        result.append(output)

    return result


def floyd_steinberg(image, levels):
    """Dither by pushing each pixel's rounding error on to its neighbours.

    The error goes right, down-left, down and down-right in the proportions
    7, 3, 5, 1 out of 16. Because the error is carried rather than discarded,
    the local average matches the original exactly, which is why this looks
    better than ordered dithering on photographs.

    The cost is that it is **sequential**: each pixel depends on the ones
    before it, so it cannot be parallelised the way the ordered version can.
    """
    working = [list(row) for row in image]
    height, width = len(working), len(working[0])
    step = 1 / (levels - 1)

    for y in range(height):
        for x in range(width):
            old = working[y][x]
            index = max(0, min(levels - 1, round(old / step)))
            new = index * step
            working[y][x] = new
            error = old - new

            for dx, dy, weight in ((1, 0, 7 / 16), (-1, 1, 3 / 16),
                                   (0, 1, 5 / 16), (1, 1, 1 / 16)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < width and 0 <= ny < height:
                    working[ny][nx] += error * weight

    return working


def mean_absolute_error(first, second):
    """Average difference between two images, for comparing dithering methods."""
    total = 0.0
    count = 0
    for row_first, row_second in zip(first, second):
        for a, b in zip(row_first, row_second):
            total += abs(a - b)
            count += 1
    return total / count


def block_average_error(first, second, block=4):
    """Average difference over blocks, which is what dithering is optimising.

    Pixel for pixel a dithered image is **worse** than a plain quantised one:
    every pixel is deliberately wrong. Averaged over a small block it is much
    better, and that is the whole trade, invisible to a per-pixel metric.
    """
    height, width = len(first), len(first[0])
    total = 0.0
    count = 0

    for y in range(0, height - block + 1, block):
        for x in range(0, width - block + 1, block):
            mean_first = sum(first[y + dy][x + dx] for dy in range(block)
                             for dx in range(block)) / (block * block)
            mean_second = sum(second[y + dy][x + dx] for dy in range(block)
                              for dx in range(block)) / (block * block)
            total += abs(mean_first - mean_second)
            count += 1

    return total / max(1, count)


def gradient(width=32, height=32):
    """A horizontal ramp, the image where banding is most visible."""
    return [[x / (width - 1) for x in range(width)] for _ in range(height)]
