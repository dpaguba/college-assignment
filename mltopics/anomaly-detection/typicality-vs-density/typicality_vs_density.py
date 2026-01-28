"""Warum die Dichte nicht die Zugehörigkeit misst."""

import math

import numpy as np


def log_density(point, sigma=1.0):
    """Die logarithmische Dichte einer Normalverteilung um den Ursprung.

    Raises:
        ValueError: bei einer nicht positiven Streuung.
    """
    if sigma <= 0.0:
        raise ValueError("die Streuung muss positiv sein")
    values = np.asarray(point, dtype=float)
    dimension = values.shape[-1]
    return (-0.5 * dimension * math.log(2.0 * math.pi * sigma ** 2)
            - 0.5 * np.sum(values ** 2, axis=-1) / sigma ** 2)


def mode_versus_samples(dimension=50, samples=4000, seed=0):
    """Vergleicht die Dichte im Gipfel mit der einer Stichprobe.

    Für eine Standardnormalverteilung ist die Dichte im Ursprung am
    grössten, und trotzdem liegt dort fast nie ein Punkt. Die Stichprobe
    sammelt sich auf einer Schale vom Radius Wurzel d, deren Breite mit
    der Dimension nicht wächst.

    Der Unterschied in der logarithmischen Dichte ist exakt d halbe:
    der Gipfel hat minus d halbe mal log zwei Pi, eine Stichprobe im
    Mittel dasselbe minus d halbe.

    Raises:
        ValueError: bei einer nicht positiven Dimension.
    """
    if dimension <= 0 or samples <= 0:
        raise ValueError("Dimension und Stichprobe müssen positiv sein")
    rng = np.random.default_rng(seed)
    cloud = rng.normal(size=(samples, dimension))
    radii = np.sqrt((cloud ** 2).sum(axis=1))
    at_mode = float(log_density(np.zeros(dimension)))
    of_sample = float(np.mean(log_density(cloud)))
    return {"dimension": dimension,
            "log density at the mode": at_mode,
            "mean log density of a sample": of_sample,
            "gap": at_mode - of_sample, "predicted gap": dimension / 2.0,
            "mean radius": float(radii.mean()),
            "radius spread": float(radii.std()),
            "predicted radius": math.sqrt(dimension)}


def over_dimensions(dimensions=(2, 10, 50, 200)):
    """Misst den Abstand zwischen Gipfel und Stichprobe über die Dimension.

    Returns:
        Liste mit einer Zeile je Dimension.
    """
    return [mode_versus_samples(dimension=dimension, samples=2000)
            for dimension in dimensions]


def typicality(point, sigma=1.0, dimension=None):
    """Misst, wie typisch ein Punkt für die Verteilung ist.

    Nicht die Dichte, sondern der Abstand der logarithmischen Dichte von
    ihrem Erwartungswert, mit umgekehrtem Vorzeichen, damit ein höherer
    Wert typischer heisst. Ein Punkt mit zu hoher Dichte ist ebenso
    untypisch wie einer mit zu niedriger, und genau das übersieht jede
    Rechnung, die nur die Dichte anschaut.

    Raises:
        ValueError: bei einer nicht positiven Streuung.
    """
    values = np.asarray(point, dtype=float)
    dimension = values.shape[-1] if dimension is None else dimension
    expected = (-0.5 * dimension * math.log(2.0 * math.pi * sigma ** 2)
                - 0.5 * dimension)
    return -np.abs(log_density(values, sigma) - expected)


def the_narrow_one_wins(dimension=100, samples=2000, narrow=0.5, seed=1):
    """Reproduziert die Beobachtung von Nalisnick und anderen.

    Ein Modell für die Standardnormalverteilung bekommt zwei
    Stichproben: eine aus der eigenen Verteilung und eine aus einer
    engeren, die es nie gesehen hat. Die fremde Stichprobe liegt näher
    am Ursprung, also gibt das Modell ihr die höhere Dichte. Nach der
    Dichte allein wäre das Fremde das Normale.

    Der Fehler liegt nicht im Modell. Er liegt in der Annahme, dass hohe
    Dichte Zugehörigkeit bedeutet. Über die Typizität gemessen fällt die
    fremde Stichprobe sofort auf.

    Returns:
        Abbildung mit beiden Massen für beide Stichproben.

    Raises:
        ValueError: bei einer unzulässigen Streuung.
    """
    if not 0.0 < narrow < 1.0:
        raise ValueError("die enge Streuung liegt zwischen null und eins")
    rng = np.random.default_rng(seed)
    own = rng.normal(size=(samples, dimension))
    foreign = rng.normal(size=(samples, dimension)) * narrow
    return {"dimension": dimension, "narrow sigma": narrow,
            "log density of the wide sample":
                float(np.mean(log_density(own))),
            "log density of the narrow sample":
                float(np.mean(log_density(foreign))),
            "but it is the wrong answer": True,
            "typicality of the wide sample":
                float(np.mean(typicality(own))),
            "typicality of the narrow sample":
                float(np.mean(typicality(foreign))),
            "why": "hohe Dichte heisst nicht Zugehörigkeit"}


def what_it_means_for_outlier_exposure():
    """Verbindet die Beobachtung mit der Themenstellung.

    Die Arbeit soll untersuchen, ob Outlier Exposure die Kalibrierung
    verbessert, und begründet das mit genau diesem Befund: tiefe
    generative Modelle geben fremden Daten die höhere Dichte. Die
    Rechnung oben zeigt, dass ein Teil davon gar kein Modellfehler ist,
    sondern eine Eigenschaft hochdimensionaler Verteilungen, die schon
    bei einer perfekt bekannten Normalverteilung auftritt.

    Daraus folgt für den Entwurf der Versuche: wer die Verbesserung
    durch Outlier Exposure messen will, muss diesen Anteil vorher
    abziehen, sonst misst er die Geometrie und nicht die Methode.
    """
    return {"the claim": "tiefe Modelle geben fremden Daten die höhere "
                         "Dichte",
            "what the calculation adds": "ein Teil davon tritt schon bei "
                                         "einer exakt bekannten "
                                         "Verteilung auf",
            "the consequence for the experiment": "diesen Anteil vorher "
                                                  "abziehen",
            "otherwise": "gemessen wird die Geometrie, nicht die Methode"}
