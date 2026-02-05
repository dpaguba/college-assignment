"""Der Fluch des Gewinners bei der Auswahl von Einstellungen."""

import math

import numpy as np


def _normal_quantile(share):
    """Das Quantil der Standardnormalverteilung.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins.
    """
    if not 0.0 < share < 1.0:
        raise ValueError("der Anteil liegt zwischen null und eins")
    low, high = -10.0, 10.0
    for _ in range(200):
        middle = (low + high) / 2.0
        if 0.5 * (1.0 + math.erf(middle / math.sqrt(2.0))) < share:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def winners_curse(candidates=50, size=1000, seed=0, truth=0.75):
    """Misst, wie stark die Auswahl den Gewinner überschätzt.

    Alle Einstellungen sind in Wahrheit gleich gut. Gemessen wird jede
    auf derselben Validierungsmenge, also unterscheiden sich die
    Messungen nur durch Zufall. Wer den besten nimmt, nimmt damit den
    grössten Zufallsausschlag mit, und die gemessene Güte ist zu hoch.

    Auf frischen Daten verschwindet der Ausschlag, und der Unterschied
    ist die Verzerrung. Sie kostet nichts an Rechenzeit und wird trotzdem
    ständig übersehen, weil sie wie ein Erfolg aussieht.

    Args:
        candidates: die Zahl der geprüften Einstellungen.
        size: die Grösse der Validierungsmenge.
        seed: der Startwert.
        truth: die wahre Güte jeder Einstellung.

    Returns:
        Abbildung mit beiden Messungen und ihrer Differenz.

    Raises:
        ValueError: bei unzulässigen Angaben.
    """
    if candidates < 1 or size < 1:
        raise ValueError("Kandidaten und Grösse müssen positiv sein")
    if not 0.0 < truth < 1.0:
        raise ValueError("die Güte liegt zwischen null und eins")
    rng = np.random.default_rng(seed)
    on_validation = rng.binomial(size, truth, size=candidates) / size
    winner = int(np.argmax(on_validation))
    fresh = rng.binomial(size, truth) / size
    return {"candidates": candidates, "size": size, "truth": truth,
            "measured on the selection set": float(on_validation[winner]),
            "measured on fresh data": float(fresh),
            "bias": float(on_validation[winner] - truth),
            "winner": winner}


def over_candidates(counts=(1, 2, 5, 20, 100, 500), size=1000, runs=200,
                    truth=0.75):
    """Misst die Verzerrung über die Zahl der geprüften Einstellungen.

    Sie wächst mit dem Logarithmus: zehnmal so viele Einstellungen
    kosten nicht die zehnfache Verzerrung, aber sie wächst ohne Grenze.
    Wer lange genug sucht, findet immer etwas, das gut aussieht.

    Returns:
        Liste mit einer Zeile je Zahl.
    """
    found = []
    for count in counts:
        biases = [winners_curse(count, size, seed, truth)["bias"]
                  for seed in range(runs)]
        found.append({"candidates": count,
                      "bias": float(np.mean(biases)),
                      "runs": runs})
    return found


def a_third_set_removes_it(candidates=50, size=1000, seed=0, truth=0.75):
    """Zeigt, was ein dritter, einmal benutzter Datensatz leistet.

    Ausgewählt wird auf der Validierungsmenge, berichtet wird auf einer
    Menge, die bei der Auswahl keine Rolle gespielt hat. Dann ist die
    berichtete Zahl wieder unverzerrt. Das kostet Daten und nichts
    sonst, und es ist der einzige zuverlässige Weg.

    Returns:
        Abbildung mit der Verzerrung auf beiden Mengen.
    """
    rng = np.random.default_rng(seed)
    on_validation = rng.binomial(size, truth, size=candidates) / size
    winner = int(np.argmax(on_validation))
    on_third = rng.binomial(size, truth) / size
    return {"bias on the selection set":
            float(on_validation[winner] - truth),
            "bias on the third set": float(on_third - truth),
            "candidates": candidates, "size": size,
            "what it costs": "Daten, sonst nichts"}


def the_expected_maximum(counts=(2, 10, 100, 1000), runs=4000, seed=0):
    """Vergleicht den gemessenen grössten Ausschlag mit der Näherung.

    Der Erwartungswert des Grössten von k normalverteilten Zahlen lässt
    sich gut durch das Quantil zur Stelle (k − 0.375) durch (k + 0.25)
    annähern. Damit ist die Verzerrung nicht nur beobachtet, sondern
    vorhergesagt: sie ist diese Zahl mal der Streuung der Messung.

    Returns:
        Liste mit einer Zeile je Zahl.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Läufen.
    """
    if runs <= 0:
        raise ValueError("die Zahl der Läufe muss positiv sein")
    rng = np.random.default_rng(seed)
    found = []
    for count in counts:
        drawn = rng.normal(size=(runs, count)).max(axis=1)
        found.append({"candidates": count,
                      "measured": float(drawn.mean()),
                      "approximation":
                          _normal_quantile((count - 0.375)
                                           / (count + 0.25))})
    return found


def what_this_means_for_a_benchmark():
    """Überträgt den Befund auf den Vergleich von Verfahren.

    Ein Verfahren, dessen Einstellungen auf denselben Daten gewählt
    wurden, auf denen berichtet wird, sieht besser aus als eines, dessen
    Einstellungen festlagen, und zwar auch dann, wenn beide gleich gut
    sind. Der Vorsprung wächst mit der Zahl der geprüften Einstellungen,
    also mit dem Rechenaufwand, den jemand aufwenden konnte.

    Genau das nennt eine der Themenstellungen als grundlegenden Fehler
    der Auswertung im Offline-Reinforcement-Learning: das versteckte
    Abstimmen bläht die berichteten Ergebnisse auf. Der Befund ist nicht
    auf dieses Gebiet beschränkt.
    """
    return {"the effect": "wer mehr Einstellungen prüfen konnte, sieht "
                          "besser aus",
            "even when": "beide Verfahren gleich gut sind",
            "what grows with it": "die Rechenzeit, die jemand hatte",
            "the fix": "die Zahl der geprüften Einstellungen berichten "
                       "und auf einer dritten Menge messen"}
