"""Exponentielles Glätten einer Zeitreihe."""


def smooth(series, alpha):
    """Glättet rekursiv mit s(t) = α x(t) + (1 − α) s(t − 1).

    Der erste geglättete Wert ist der erste Beobachtungswert, wie es die
    Übung vorgibt.

    Args:
        series: die Beobachtungen.
        alpha: Glättungsparameter zwischen null und eins.

    Returns:
        Liste der geglätteten Werte.

    Raises:
        ValueError: bei einem α ausserhalb von [0, 1] oder leerer Reihe.
    """
    if not 0.0 <= alpha <= 1.0:
        raise ValueError("alpha liegt ausserhalb von [0, 1]")
    if not series:
        raise ValueError("leere Reihe")
    result = [float(series[0])]
    for value in series[1:]:
        result.append(alpha * value + (1 - alpha) * result[-1])
    return result


def weights(alpha, count):
    """Gewichte, mit denen die Vergangenheit in den letzten Wert eingeht.

    Der jüngste Wert bekommt α, der davor α(1 − α) und so fort. Die Reihe
    ist geometrisch; nach n Gliedern fehlt noch genau (1 − α)ⁿ zur Eins,
    was zugleich das Gewicht des Startwerts ist.

    Raises:
        ValueError: bei einem α ausserhalb von (0, 1].
    """
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha liegt ausserhalb von (0, 1]")
    return [alpha * (1 - alpha) ** step for step in range(count)]


def missing_weight(alpha, count):
    """Gewicht, das nach ``count`` Gliedern noch beim Startwert liegt."""
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha liegt ausserhalb von (0, 1]")
    return (1 - alpha) ** count


def matches_closed_form(series, alpha):
    """Vergleicht die Rekursion mit der ausgeschriebenen Summe.

    Der geglättete Wert lässt sich auch als gewichtete Summe aller
    bisherigen Beobachtungen schreiben, mit dem Startwert als Rest. Beide
    Wege müssen dasselbe liefern.
    """
    recursive = smooth(series, alpha)
    for index in range(len(series)):
        total = 0.0
        for step in range(index):
            total += alpha * (1 - alpha) ** step * series[index - step]
        total += (1 - alpha) ** index * series[0]
        if abs(total - recursive[index]) > 1e-9:
            return False
    return True


def roughness(series):
    """Misst, wie stark eine Reihe von Punkt zu Punkt springt."""
    return sum(abs(later - earlier)
               for earlier, later in zip(series, series[1:]))


def lag_on_a_trend(alpha=0.3, length=40):
    """Misst, wie weit die geglättete Reihe hinter einem Trend zurückbleibt.

    Auf einer steigenden Geraden bleibt das einfache exponentielle Glätten
    dauerhaft zurück; der Abstand strebt gegen (1 − α)/α mal der Steigung.

    Returns:
        Abbildung mit dem gemessenen und dem erwarteten Abstand.
    """
    slope = 1.0
    series = [slope * index for index in range(length)]
    smoothed = smooth(series, alpha)
    return {"gap": series[-1] - smoothed[-1],
            "expected": slope * (1 - alpha) / alpha}


def forecast(series, alpha, steps=1):
    """Sagt die nächsten Werte voraus.

    Das einfache exponentielle Glätten hat kein Trendglied, deshalb ist
    die Vorhersage für jeden Horizont derselbe letzte geglättete Wert.

    Raises:
        ValueError: bei einer nicht positiven Schrittzahl.
    """
    if steps < 1:
        raise ValueError("Schrittzahl muss positiv sein")
    return [smooth(series, alpha)[-1]] * steps


def quality(series, predicted):
    """Berechnet die üblichen Prognosefehler.

    Returns:
        Abbildung mit mittlerem absolutem Fehler, mittlerem quadriertem
        Fehler und dessen Wurzel.
    """
    if len(series) != len(predicted):
        raise ValueError("Reihen sind verschieden lang")
    absolute = sum(abs(a - b) for a, b in zip(series, predicted)) / len(series)
    squared = sum((a - b) ** 2 for a, b in zip(series, predicted)) / len(series)
    return {"mae": absolute, "mse": squared, "rmse": squared ** 0.5}
