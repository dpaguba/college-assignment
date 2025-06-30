"""Diskrete Fourier-Transformation, Abtasttheorem und Tiefpass."""

import cmath
import math


def dft(values):
    """Berechnet die diskrete Fourier-Transformation direkt.

    Die Summe über alle Abtastwerte mit dem Drehfaktor
    exp(−2πi k n / N) ist die Definition; sie kostet quadratisch viele
    Operationen, wo die schnelle Transformation N log N braucht.

    Returns:
        Liste der komplexen Koeffizienten.

    Raises:
        ValueError: bei einer leeren Reihe.
    """
    count = len(values)
    if count == 0:
        raise ValueError("leere Reihe")
    result = []
    for frequency in range(count):
        total = 0j
        for index, value in enumerate(values):
            angle = -2j * math.pi * frequency * index / count
            total += value * cmath.exp(angle)
        result.append(total)
    return result


def inverse_dft(coefficients):
    """Kehrt die Transformation um; das Vorzeichen im Exponenten dreht sich."""
    count = len(coefficients)
    result = []
    for index in range(count):
        total = 0j
        for frequency, value in enumerate(coefficients):
            angle = 2j * math.pi * frequency * index / count
            total += value * cmath.exp(angle)
        result.append(total / count)
    return result


def amplitudes(coefficients):
    """Beträge der Koeffizienten, auf die Länge der Reihe bezogen."""
    count = len(coefficients)
    return [abs(value) * 2 / count for value in coefficients]


def exercise_signal(count=400):
    """Liefert das Signal der Übung, 0.5·sin(3x) + 0.25·sin(10x).

    Abgetastet wird über eine ganze Zahl von Perioden, damit die
    Frequenzen genau auf Gitterpunkte fallen.
    """
    return [0.5 * math.sin(3 * 2 * math.pi * index / count)
            + 0.25 * math.sin(10 * 2 * math.pi * index / count)
            for index in range(count)]


def exercise_peaks():
    """Findet die beiden Frequenzen des Übungssignals wieder.

    Returns:
        Abbildung mit den Frequenzen und ihren Amplituden, die stärkere
        zuerst.
    """
    values = exercise_signal()
    spectrum = amplitudes(dft(values))
    half = len(spectrum) // 2
    ranked = sorted(range(1, half), key=lambda index: spectrum[index],
                    reverse=True)[:2]
    return {"frequencies": ranked,
            "amplitudes": [spectrum[index] for index in ranked]}


def aliasing_example(frequency=15, rate=20, seconds=1.0):
    """Zeigt, was unterhalb der Nyquist-Rate geschieht.

    Wird ein Signal langsamer abgetastet als mit der doppelten Frequenz,
    erscheint es im Spektrum an einer falschen Stelle.

    Args:
        frequency: wahre Frequenz in Schwingungen je Sekunde.
        rate: Abtastrate.
        seconds: Länge der Aufnahme.

    Returns:
        Abbildung mit der wahren und der gemessenen Frequenz und der
        Nyquist-Grenze.
    """
    count = int(rate * seconds)
    values = [math.sin(2 * math.pi * frequency * index / rate)
              for index in range(count)]
    spectrum = amplitudes(dft(values))
    half = count // 2
    measured = max(range(1, half + 1), key=lambda index: spectrum[index])
    return {"true frequency": frequency, "measured frequency": measured,
            "nyquist": rate / 2}


def low_pass(values, cutoff):
    """Entfernt alle Frequenzen oberhalb der Grenze.

    Der Filter wird im Frequenzbereich angewandt: die betroffenen
    Koeffizienten werden auf null gesetzt, danach wird zurücktransformiert.

    Raises:
        ValueError: bei einer negativen Grenzfrequenz.
    """
    if cutoff < 0:
        raise ValueError("Grenzfrequenz ist negativ")
    coefficients = dft(values)
    count = len(values)
    filtered = []
    for frequency, value in enumerate(coefficients):
        distance = min(frequency, count - frequency)
        filtered.append(value if distance <= cutoff else 0j)
    return [value.real for value in inverse_dft(filtered)]


def low_pass_example():
    """Misst die hohe Frequenz vor und nach dem Filter.

    Returns:
        Abbildung mit der Amplitude bei Frequenz 10 vor und nach dem
        Tiefpass mit der Grenze 5.
    """
    values = exercise_signal(200)
    before = amplitudes(dft(values))[10]
    filtered = low_pass(values, 5)
    after = amplitudes(dft(filtered))[10]
    return {"before": before, "after": after}


def parseval_holds(values):
    """Prüft die Gleichung von Parseval.

    Die Energie im Ortsbereich stimmt mit der im Frequenzbereich überein,
    geteilt durch die Zahl der Abtastwerte.
    """
    coefficients = dft(values)
    left = sum(value * value for value in values)
    right = sum(abs(value) ** 2 for value in coefficients) / len(values)
    return abs(left - right) < 1e-9 * max(1.0, abs(left))


def domains():
    """Beschreibt, welche Eigenschaften in welchem Bereich sichtbar sind."""
    return {"spatial": "where something happens",
            "frequency": "how fast it happens",
            "wavelet": "both at once, at the price of resolution"}
