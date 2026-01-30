"""Die Erwerbsfunktion der bayesschen Optimierung."""

import math

import numpy as np


def _normal_cdf(value):
    """Die Verteilungsfunktion der Standardnormalverteilung."""
    return 0.5 * (1.0 + math.erf(value / math.sqrt(2.0)))


def _normal_pdf(value):
    """Die Dichte der Standardnormalverteilung."""
    return math.exp(-0.5 * value ** 2) / math.sqrt(2.0 * math.pi)


def expected_improvement(mean, deviation, best, tradeoff=0.0):
    """Der erwartete Gewinn über den bisher besten Wert.

    Gesucht wird das Maximum. Der Gewinn ist der Überschuss über den
    besten bisher gesehenen Wert, und weil die Vorhersage eine
    Verteilung ist, wird er erwartet. Die geschlossene Form besteht aus
    zwei Teilen: dem Vorsprung des Mittelwerts, gewichtet mit der
    Wahrscheinlichkeit einer Verbesserung, und der Streuung, gewichtet
    mit der Dichte an der Schwelle.

    Der erste Teil zieht dorthin, wo es gut aussieht, der zweite
    dorthin, wo wenig bekannt ist. Beide stehen in einer Formel, und
    das ist der ganze Grund, warum es funktioniert.

    Args:
        mean: der vorhergesagte Mittelwert.
        deviation: die vorhergesagte Streuung.
        best: der bisher beste beobachtete Wert.
        tradeoff: ein Zuschlag, der die Erkundung dämpft.

    Returns:
        Der erwartete Gewinn, nie negativ.

    Raises:
        ValueError: bei einer negativen Streuung oder einem negativen
            Zuschlag.
    """
    if deviation < 0.0 or tradeoff < 0.0:
        raise ValueError("Streuung und Zuschlag dürfen nicht negativ sein")
    gain = mean - best - tradeoff
    if deviation == 0.0:
        return max(0.0, gain)
    standard = gain / deviation
    return gain * _normal_cdf(standard) + deviation * _normal_pdf(standard)


def by_sampling(mean, deviation, best, tradeoff=0.0, draws=200000,
                seed=0):
    """Rechnet denselben Wert durch Ziehen aus der Verteilung aus.

    Gezogen werden Werte aus der vorhergesagten Verteilung, und gemittelt
    wird, um wie viel sie den besten übertreffen. Diese Rechnung hat mit
    der geschlossenen Form nichts gemein und ist damit die Probe.

    Raises:
        ValueError: bei einer negativen Streuung oder Ziehungszahl.
    """
    if deviation < 0.0 or draws <= 0:
        raise ValueError("unzulässige Angaben")
    rng = np.random.default_rng(seed)
    drawn = rng.normal(mean, max(deviation, 1e-12), size=draws)
    return float(np.mean(np.maximum(0.0, drawn - best - tradeoff)))


def exploration_against_exploitation():
    """Zeigt, welche von zwei Stellen die Erwerbsfunktion wählt.

    Die eine Stelle sagt einen leicht besseren Wert voraus und ist gut
    bekannt; die andere sagt einen etwas schlechteren voraus und ist
    kaum bekannt. Die Erwerbsfunktion nimmt die zweite, weil dort noch
    etwas zu holen ist. Eine Suche, die nur dem Mittelwert folgt, nähme
    die erste und bliebe für immer, wo sie ist.

    Returns:
        Abbildung mit beiden Werten und der Wahl.
    """
    known = expected_improvement(mean=1.0, deviation=0.05, best=0.9)
    unknown = expected_improvement(mean=0.8, deviation=1.0, best=0.9)
    return {"the safe one": known, "the uncertain one": unknown,
            "chosen": "the uncertain one" if unknown > known
                      else "the safe one",
            "what a greedy search would take": "the safe one",
            "why": "wo nichts bekannt ist, ist noch etwas zu holen"}


def the_tradeoff_parameter():
    """Zeigt, was der Zuschlag bewirkt.

    Er verlangt, dass eine Stelle den bisher besten Wert um einen
    Mindestbetrag übertrifft, bevor sie überhaupt zählt. Damit wird die
    Suche vorsichtiger und bleibt länger in bekannten Gegenden. Der
    Zuschlag ist der einzige Regler in der Formel und wird meist auf
    null gesetzt, was eine Entscheidung ist und keine Vorgabe.

    Returns:
        Abbildung mit dem Wert bei mehreren Zuschlägen.
    """
    return {"values": {round(value, 2):
                       round(expected_improvement(0.0, 1.0, 0.0, value), 4)
                       for value in (0.0, 0.25, 0.5, 1.0, 2.0)},
            "what it does": "es verlangt einen Mindestvorsprung",
            "the usual setting": 0.0,
            "why that is a choice": "sie wird selten begründet"}


def why_not_just_the_mean():
    """Sagt, warum die Vorhersage allein nicht reicht.

    Wer immer dort misst, wo der Mittelwert am höchsten ist, misst immer
    wieder an derselben Stelle: die Beobachtung bestätigt die Vorhersage
    und ändert nichts. Der Rest des Raums bleibt unbekannt, und ein
    besseres Gebiet wird nie gefunden. Die Streuung im zweiten Summanden
    ist genau das Gegenmittel.
    """
    return {"the greedy failure": "immer dieselbe Stelle messen",
            "why it never escapes": "die Beobachtung bestätigt die "
                                    "Vorhersage",
            "the remedy": "die Streuung als zweiter Summand",
            "the balance": "sie ergibt sich aus der Formel und wird "
                           "nicht eingestellt"}
