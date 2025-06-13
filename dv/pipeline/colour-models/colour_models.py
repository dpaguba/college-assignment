"""Farbmodelle der Bilderzeugungs-Pipeline und die Wege zwischen ihnen."""

import math

LUMINANCE = (0.2126, 0.7152, 0.0722)


def _check(*channels):
    """Prüft, dass jeder Kanal im Einheitsintervall liegt.

    Raises:
        ValueError: sobald ein Kanal ausserhalb liegt.
    """
    for channel in channels:
        if not 0.0 <= channel <= 1.0:
            raise ValueError("Kanal liegt ausserhalb von [0, 1]")


def rgb_to_hsv(red, green, blue):
    """Rechnet eine Farbe von RGB nach HSV um.

    Args:
        red, green, blue: Kanäle im Einheitsintervall.

    Returns:
        Tripel (Farbton in [0, 1), Sättigung, Hellwert).

    Raises:
        ValueError: bei einem Kanal ausserhalb des Einheitsintervalls.
    """
    _check(red, green, blue)
    largest = max(red, green, blue)
    smallest = min(red, green, blue)
    span = largest - smallest
    if span == 0:
        hue = 0.0
    elif largest == red:
        hue = ((green - blue) / span) % 6
    elif largest == green:
        hue = (blue - red) / span + 2
    else:
        hue = (red - green) / span + 4
    saturation = 0.0 if largest == 0 else span / largest
    return hue / 6.0, saturation, largest


def hsv_to_rgb(hue, saturation, value):
    """Rechnet eine Farbe von HSV nach RGB zurück.

    Raises:
        ValueError: bei Sättigung oder Hellwert ausserhalb von [0, 1].
    """
    _check(saturation, value)
    if saturation == 0:
        return value, value, value
    sector = (hue % 1.0) * 6.0
    index = int(sector)
    offset = sector - index
    first = value * (1 - saturation)
    second = value * (1 - saturation * offset)
    third = value * (1 - saturation * (1 - offset))
    table = [(value, third, first), (second, value, first),
             (first, value, third), (first, second, value),
             (third, first, value), (value, first, second)]
    return table[index % 6]


def rgb_to_grey(red, green, blue):
    """Bildet eine Farbe auf ihre Helligkeit ab.

    Die Gewichte 0.2126, 0.7152 und 0.0722 stammen aus der Empfindlichkeit
    des Auges; das arithmetische Mittel der Kanäle wäre eine andere,
    schlechtere Antwort.
    """
    _check(red, green, blue)
    return sum(weight * channel
               for weight, channel in zip(LUMINANCE, (red, green, blue)))


def interpolate(model, first, second, position):
    """Mischt zwei Farben im genannten Modell.

    Args:
        model: ``rgb`` oder ``hsv``.
        first, second: Farben als RGB-Tripel.
        position: Mischanteil zwischen 0 und 1.

    Returns:
        Die gemischte Farbe als RGB-Tripel.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    if model == "rgb":
        return tuple(a + (b - a) * position
                     for a, b in zip(first, second))
    if model == "hsv":
        start = rgb_to_hsv(*first)
        end = rgb_to_hsv(*second)
        mixed = tuple(a + (b - a) * position for a, b in zip(start, end))
        return hsv_to_rgb(*mixed)
    raise ValueError("unbekanntes Farbmodell")


def interpolation_differs(first, second):
    """Misst, wie weit die beiden Mischwege in der Mitte auseinanderliegen.

    Returns:
        Abbildung mit beiden Mischfarben und ihrem euklidischen Abstand.
    """
    in_rgb = interpolate("rgb", first, second, 0.5)
    in_hsv = interpolate("hsv", first, second, 0.5)
    distance = math.sqrt(sum((a - b) ** 2 for a, b in zip(in_rgb, in_hsv)))
    return {"rgb": in_rgb, "hsv": in_hsv, "distance": distance}


def models():
    """Nennt die Modelle der Vorlesung und wonach sie gebaut sind."""
    return {"RGB": "additive, for screens",
            "CMY": "subtractive, for print",
            "HSV": "hue, saturation, value, closer to how colour is named",
            "CIE Lab": "built so that equal steps look equally large"}
