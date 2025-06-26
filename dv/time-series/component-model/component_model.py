"""Komponentenmodell einer Zeitreihe: Trend, Saison und Residuum."""

import math


def example_series(periods=8, period=12):
    """Baut eine Reihe aus linearem Trend, Saison und kleinem Rauschen.

    Die Reihe ist so gebaut, dass Trend und Saison bekannt sind und das
    Verfahren sich daran messen lässt.

    Returns:
        Liste der Werte.
    """
    values = []
    for index in range(periods * period):
        season = 3.0 * math.sin(2 * math.pi * (index % period) / period)
        noise = 0.1 * math.sin(index * 7.0)
        values.append(10.0 + 0.05 * index + season + noise)
    return values


def moving_average(series, period):
    """Glättet die Reihe mit einem zentrierten gleitenden Mittel.

    Bei gerader Saisonlänge werden die beiden Randwerte halb gewichtet,
    damit das Fenster symmetrisch bleibt.

    Returns:
        Liste gleicher Länge; an den Rändern steht None.

    Raises:
        ValueError: wenn die Saisonlänge nicht in die Reihe passt.
    """
    if period < 2 or period > len(series):
        raise ValueError("Saisonlaenge passt nicht zur Reihe")
    half = period // 2
    result = [None] * len(series)
    for index in range(half, len(series) - half):
        if period % 2 == 0:
            window = series[index - half:index + half + 1]
            total = sum(window[1:-1]) + (window[0] + window[-1]) / 2
            result[index] = total / period
        else:
            result[index] = sum(series[index - half:index + half + 1]) / period
    return result


def seasonal_figure(series, period):
    """Bestimmt die mittlere Abweichung je Position innerhalb der Saison.

    Vom Trend befreit wird über den gleitenden Mittelwert; die
    Positionsmittel werden anschliessend so verschoben, dass sie sich zu
    null addieren.

    Returns:
        Liste der Saisonwerte, ein Wert je Position.
    """
    trend = moving_average(series, period)
    sums = [0.0] * period
    counts = [0] * period
    for index, value in enumerate(series):
        if trend[index] is None:
            continue
        sums[index % period] += value - trend[index]
        counts[index % period] += 1
    figure = [sums[position] / counts[position] if counts[position] else 0.0
              for position in range(period)]
    offset = sum(figure) / period
    return [value - offset for value in figure]


def decompose(series, period):
    """Zerlegt eine Reihe additiv in Trend, Saison und Residuum.

    Returns:
        Abbildung mit den drei Komponenten, jeweils in der Länge der
        Reihe; im Trend stehen an den Rändern None.

    Raises:
        ValueError: wenn die Saisonlänge nicht in die Reihe passt.
    """
    trend = moving_average(series, period)
    figure = seasonal_figure(series, period)
    season = [figure[index % period] for index in range(len(series))]
    residual = [None if trend[index] is None
                else series[index] - trend[index] - season[index]
                for index in range(len(series))]
    return {"trend": trend, "season": season, "residual": residual}


def recovers_a_known_series(period=12):
    """Misst, wie genau die Zerlegung die eingebauten Komponenten trifft.

    Returns:
        Abbildung mit dem grössten Fehler von Trend und Saison.
    """
    series = example_series(period=period)
    parts = decompose(series, period)
    trend_error = 0.0
    for index, value in enumerate(parts["trend"]):
        if value is None:
            continue
        trend_error = max(trend_error, abs(value - (10.0 + 0.05 * index)))
    season_error = 0.0
    for position in range(period):
        expected = 3.0 * math.sin(2 * math.pi * position / period)
        season_error = max(season_error,
                           abs(parts["season"][position] - expected))
    return {"trend error": trend_error, "season error": season_error}


def additive_versus_multiplicative(period=12):
    """Vergleicht beide Modelle auf einer Reihe mit wachsender Schwankung.

    Wächst die Saisonschwankung mit dem Niveau, trifft das multiplikative
    Modell besser: dort wird geteilt, wo das additive subtrahiert.

    Returns:
        Abbildung mit dem mittleren quadrierten Residuum beider Modelle.
    """
    values = []
    for index in range(6 * period):
        level = 10.0 + 0.2 * index
        factor = 1.0 + 0.3 * math.sin(2 * math.pi * (index % period) / period)
        values.append(level * factor)
    additive = decompose(values, period)
    trend = moving_average(values, period)
    ratios = [0.0] * period
    counts = [0] * period
    for index, value in enumerate(values):
        if trend[index] is None or trend[index] == 0:
            continue
        ratios[index % period] += value / trend[index]
        counts[index % period] += 1
    figure = [ratios[position] / counts[position] if counts[position] else 1.0
              for position in range(period)]
    scale = sum(figure) / period
    figure = [value / scale for value in figure]
    additive_error = 0.0
    multiplicative_error = 0.0
    count = 0
    for index, value in enumerate(values):
        if trend[index] is None:
            continue
        additive_error += additive["residual"][index] ** 2
        predicted = trend[index] * figure[index % period]
        multiplicative_error += (value - predicted) ** 2
        count += 1
    return {"additive error": additive_error / count,
            "multiplicative error": multiplicative_error / count}


def goals():
    """Nennt die Ziele der Zeitreihenanalyse aus der Vorlesung."""
    return ["describe", "explain", "forecast", "control"]
