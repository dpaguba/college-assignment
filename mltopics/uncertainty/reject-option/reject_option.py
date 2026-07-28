"""Vorhersagen ablehnen statt raten."""

import numpy as np


def _run(size, seed, informative=True):
    """Erzeugt Vorhersagen, Marken und eine Zuversicht.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    if size <= 0:
        raise ValueError("die Grösse muss positiv sein")
    rng = np.random.default_rng(seed)
    probability = rng.uniform(0.5, 1.0, size=size)
    correct = rng.uniform(size=size) < probability
    confidence = probability if informative else rng.uniform(size=size)
    return correct.astype(int), confidence


def risk_coverage(size=4000, seed=0, steps=20, informative=True):
    """Misst den Fehler auf dem angenommenen Teil bei jeder Abdeckung.

    Sortiert wird nach der Zuversicht, dann wird von unten abgeschnitten.
    Ist die Zuversicht brauchbar, so fällt der Fehler auf dem Rest; ist
    sie es nicht, bleibt er stehen. Genau darin besteht die Prüfung
    einer Unsicherheitsschätzung, und sie braucht keine wahre
    Unsicherheit zum Vergleich.

    Returns:
        Liste mit einer Zeile je Abdeckung, aufsteigend.

    Raises:
        ValueError: bei einer nicht positiven Grösse.
    """
    correct, confidence = _run(size, seed, informative)
    order = np.argsort(-confidence, kind="stable")
    sorted_correct = correct[order]
    plain = float(1.0 - correct.mean())
    found = []
    for step in range(1, steps + 1):
        keep = max(1, int(size * step / steps))
        found.append({"coverage": keep / size,
                      "risk": float(1.0
                                    - sorted_correct[:keep].mean()),
                      "kept": keep, "plain": plain})
    return found


def area_under_the_curve(rows):
    """Mittelt den Fehler über die Abdeckungen.

    Raises:
        ValueError: bei einer leeren Kurve.
    """
    if not rows:
        raise ValueError("leere Kurve")
    return float(np.mean([row["risk"] for row in rows]))


def a_useless_confidence(size=4000, seed=0):
    """Vergleicht eine brauchbare Zuversicht mit einer gewürfelten.

    Beide Modelle sagen dasselbe voraus und irren gleich oft. Der
    Unterschied liegt allein darin, ob sie wissen, wann sie irren, und
    die Kurve zeigt es sofort.

    Returns:
        Abbildung mit beiden Kurven.
    """
    real = risk_coverage(size, seed, informative=True)
    fake = risk_coverage(size, seed, informative=False)
    return {"risk at full coverage": fake[-1]["risk"],
            "risk at half coverage": fake[len(fake) // 2 - 1]["risk"],
            "risk at half coverage with a real confidence":
                real[len(real) // 2 - 1]["risk"],
            "area with a real confidence": area_under_the_curve(real),
            "area with a useless one": area_under_the_curve(fake),
            "why": "beide irren gleich oft, nur eines weiss wann"}


def where_to_stop(size=4000, seed=0, steps=20):
    """Bestimmt die Abdeckung, bei der die Kosten am kleinsten sind.

    Ablehnen ist nicht umsonst: eine abgelehnte Vorhersage muss von
    einem Menschen bearbeitet werden. Ist das billig, lohnt es sich,
    viel abzulehnen; ist es teuer, lohnt sich fast nichts. Die
    Kurve allein sagt also noch nicht, wo zu schneiden ist.

    Returns:
        Abbildung mit der besten Abdeckung bei zwei Preisen.
    """
    rows = risk_coverage(size, seed, steps=steps)
    found = {}
    for name, price in (("cheap", 0.05), ("expensive", 0.6)):
        best = min(rows, key=lambda row: row["risk"] * row["coverage"]
                   + price * (1.0 - row["coverage"]))
        found[name] = best["coverage"]
    return {"coverage at a cheap rejection": found["cheap"],
            "coverage at an expensive one": found["expensive"],
            "prices": (0.05, 0.6),
            "why": "eine abgelehnte Vorhersage kostet einen Menschen"}


def what_the_curve_is_good_for():
    """Sagt, warum diese Kurve die richtige Prüfung ist.

    Eine Unsicherheitsschätzung lässt sich nicht direkt gegen die
    Wahrheit halten, denn die wahre Unsicherheit steht nirgends. Was
    sich prüfen lässt, ist ihre Wirkung: sortiert man nach ihr, sollen
    die Fehler vorne stehen. Die Kurve misst genau das und braucht
    dafür nur die Marken, die ohnehin vorliegen.
    """
    return {"the problem": "die wahre Unsicherheit steht nirgends",
            "what can be checked": "ob die Fehler vorne stehen, wenn "
                                   "nach ihr sortiert wird",
            "what it needs": "nur die Marken",
            "what it does not settle": "wo geschnitten wird"}
