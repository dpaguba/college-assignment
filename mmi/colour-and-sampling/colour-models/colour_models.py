"""Colour models: RGB, HSV, HLS, CMYK and CIE XYZ, and the conversions between them.

Colour is not a physical quantity but a perception, and each model exists for a
different job:

- **RGB** is additive and device-oriented, because a screen adds light
- **CMYK** is subtractive and print-oriented, because ink removes light
- **HSV and HLS** are user-oriented, because "a lighter red" is a sensible
  instruction and "more green in the blue channel" is not
- **CIE XYZ** is device-independent, defined from measurements of human
  perception rather than from any hardware, which makes it the reference every
  other model is calibrated against

The conversions are where the exercises live, and each one is invertible except
where the model itself loses information.
"""

from __future__ import annotations

from dataclasses import dataclass


def rgb_to_hsv(red, green, blue):
    """Convert RGB in [0,1] to hue in degrees, saturation and value in [0,1].

    Value is the largest channel, saturation is how far the smallest is below
    it, and hue is which channel dominates. The hue is undefined for grey, and
    the convention here returns 0, which is what makes the conversion not quite
    invertible: every grey maps to hue 0 and comes back the same grey.
    """
    largest = max(red, green, blue)
    smallest = min(red, green, blue)
    spread = largest - smallest

    if spread == 0:
        hue = 0.0
    elif largest == red:
        hue = 60 * (((green - blue) / spread) % 6)
    elif largest == green:
        hue = 60 * ((blue - red) / spread + 2)
    else:
        hue = 60 * ((red - green) / spread + 4)

    saturation = 0.0 if largest == 0 else spread / largest
    return hue % 360, saturation, largest


def hsv_to_rgb(hue, saturation, value):
    """Convert hue in degrees, saturation and value in [0,1] back to RGB."""
    chroma = value * saturation
    sector = (hue % 360) / 60
    second = chroma * (1 - abs(sector % 2 - 1))
    offset = value - chroma

    table = [(chroma, second, 0), (second, chroma, 0), (0, chroma, second),
             (0, second, chroma), (second, 0, chroma), (chroma, 0, second)]
    red, green, blue = table[int(sector) % 6]

    return red + offset, green + offset, blue + offset


def rgb_to_hls(red, green, blue):
    """Convert RGB to hue, lightness and saturation.

    HLS differs from HSV in what the third axis means. Value is the brightest
    channel, so pure red has value 1; lightness is the midpoint between the
    brightest and the darkest, so pure red has lightness 0.5 and only white has
    lightness 1. That is the more intuitive scale for "how light is this
    colour", and the reason both models exist.
    """
    largest = max(red, green, blue)
    smallest = min(red, green, blue)
    spread = largest - smallest
    lightness = (largest + smallest) / 2

    if spread == 0:
        return 0.0, lightness, 0.0

    if largest == red:
        hue = 60 * (((green - blue) / spread) % 6)
    elif largest == green:
        hue = 60 * ((blue - red) / spread + 2)
    else:
        hue = 60 * ((red - green) / spread + 4)

    saturation = spread / (1 - abs(2 * lightness - 1)) if lightness not in (0, 1) else 0.0
    return hue % 360, lightness, min(1.0, saturation)


def hls_to_rgb(hue, lightness, saturation):
    """Convert hue, lightness and saturation back to RGB."""
    chroma = (1 - abs(2 * lightness - 1)) * saturation
    sector = (hue % 360) / 60
    second = chroma * (1 - abs(sector % 2 - 1))
    offset = lightness - chroma / 2

    table = [(chroma, second, 0), (second, chroma, 0), (0, chroma, second),
             (0, second, chroma), (second, 0, chroma), (chroma, 0, second)]
    red, green, blue = table[int(sector) % 6]

    return red + offset, green + offset, blue + offset


def rgb_to_cmyk(red, green, blue):
    """Convert RGB to cyan, magenta, yellow and key.

    The naive subtractive conversion gives three inks, and printing a grey with
    equal parts of all three wastes ink and produces a muddy black. Pulling out
    the common part as **key**, the black plate, is why CMYK has four channels
    and not three.
    """
    key = 1 - max(red, green, blue)
    if key == 1:
        return 0.0, 0.0, 0.0, 1.0

    cyan = (1 - red - key) / (1 - key)
    magenta = (1 - green - key) / (1 - key)
    yellow = (1 - blue - key) / (1 - key)
    return cyan, magenta, yellow, key


def cmyk_to_rgb(cyan, magenta, yellow, key):
    """Convert CMYK back to RGB."""
    return ((1 - cyan) * (1 - key),
            (1 - magenta) * (1 - key),
            (1 - yellow) * (1 - key))


SRGB_TO_XYZ = ((0.4124564, 0.3575761, 0.1804375),
               (0.2126729, 0.7151522, 0.0721750),
               (0.0193339, 0.1191920, 0.9503041))
"""The sRGB primaries in CIE XYZ, with the D65 white point."""

XYZ_TO_SRGB = ((3.2404542, -1.5371385, -0.4985314),
               (-0.9692660, 1.8760108, 0.0415560),
               (0.0556434, -0.2040259, 1.0572252))
"""The inverse matrix, used to bring a measured colour back to a screen."""


def gamma_expand(value):
    """Undo the sRGB transfer function, turning a stored value into linear light.

    Screens do not store light linearly. Doing arithmetic on the stored values
    directly, which is what naive image code does, blends and resizes in the
    wrong space, and the visible symptom is that a half-and-half mix of black
    and white comes out too dark.
    """
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def gamma_compress(value):
    """Apply the sRGB transfer function, turning linear light into a stored value."""
    return 12.92 * value if value <= 0.0031308 else 1.055 * value ** (1 / 2.4) - 0.055


def rgb_to_xyz(red, green, blue, linear=False):
    """Convert sRGB to CIE XYZ, expanding the gamma unless the input is already linear."""
    if not linear:
        red, green, blue = gamma_expand(red), gamma_expand(green), gamma_expand(blue)

    return tuple(row[0] * red + row[1] * green + row[2] * blue for row in SRGB_TO_XYZ)


def xyz_to_rgb(x, y, z, linear=False):
    """Convert CIE XYZ to sRGB, compressing the gamma unless linear output is wanted."""
    values = [row[0] * x + row[1] * y + row[2] * z for row in XYZ_TO_SRGB]
    if linear:
        return tuple(values)
    return tuple(gamma_compress(max(0.0, min(1.0, value))) for value in values)


def xyz_to_lab(x, y, z, white=(0.95047, 1.0, 1.08883)):
    """Convert CIE XYZ to L*a*b*, which is roughly perceptually uniform.

    Uniform means equal numeric distances look like equal colour differences,
    which XYZ and RGB emphatically are not. That is what makes Lab the space to
    measure colour differences in, and the cube root is where the uniformity
    comes from: perception of lightness follows roughly a power law.
    """
    def transfer(value):
        """The CIE nonlinearity: a cube root, made linear near zero.

        The linear segment below 0.008856 exists because the cube root has an
        infinite slope at the origin, which would make dark colours
        numerically unstable.
        """
        return value ** (1 / 3) if value > 0.008856 else 7.787 * value + 16 / 116

    fx, fy, fz = (transfer(x / white[0]), transfer(y / white[1]), transfer(z / white[2]))
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def colour_difference(first, second):
    """The CIE76 distance between two sRGB colours, measured in Lab.

    The naive alternative, Euclidean distance in RGB, says that two dark blues
    are as different as two bright greens with the same numeric gap, which does
    not match what anyone sees. Converting first is the fix, and it costs two
    matrix multiplications.
    """
    first_lab = xyz_to_lab(*rgb_to_xyz(*first))
    second_lab = xyz_to_lab(*rgb_to_xyz(*second))
    return sum((a - b) ** 2 for a, b in zip(first_lab, second_lab)) ** 0.5


def luminance(red, green, blue):
    """Relative luminance, the Y of XYZ, which is what "brightness" means.

    The weights are not equal: green contributes about 72 per cent and blue
    about 7. Averaging the three channels instead, which is the usual quick
    greyscale conversion, makes blues far too light and greens too dark.
    """
    return rgb_to_xyz(red, green, blue)[1]
