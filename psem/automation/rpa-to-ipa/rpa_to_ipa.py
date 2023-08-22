"""Von der Robotic Process Automation zur intelligenten Automatisierung."""

STAGES = {
    "RPA": {"decides": "nichts, es folgt festen Regeln",
            "input": "strukturiert, feste Bildschirmpositionen",
            "breaks when": "sich die Oberfläche ändert",
            "needs": "einen stabilen, wiederholbaren Ablauf"},
    "cognitive RPA": {"decides": "einfache Fälle",
                      "input": "auch unstrukturiert, mit Erkennung",
                      "breaks when": "die Erkennung falsch liegt und "
                                     "niemand es merkt",
                      "needs": "Modelle für Text und Bild"},
    "IPA": {"decides": "auch Fälle, für die es keine Regel gibt",
            "input": "beliebig, mit Kontext",
            "breaks when": "der Fall ausserhalb der Trainingsdaten liegt",
            "needs": "Modelle, Daten und einen Weg zurück zum Menschen"},
}


def stages():
    """Nennt die Stufen in ihrer Reihenfolge."""
    return ["RPA", "cognitive RPA", "IPA"]


def describe(stage):
    """Beschreibt eine Stufe.

    Raises:
        ValueError: bei einer unbekannten Stufe.
    """
    if stage not in STAGES:
        raise ValueError("unbekannte Stufe")
    return dict(STAGES[stage])


def what_rpa_actually_is():
    """Sagt, was die Technik im Kern ist.

    Ein Roboter bedient die Oberfläche eines Systems so, wie ein Mensch
    sie bedienen würde: er klickt, tippt und liest ab. Er greift nicht
    auf Schnittstellen zu, und das ist zugleich sein Vorteil und sein
    Problem. Der Vorteil: er braucht keine Änderung am System, auch
    nicht an einem, das niemand mehr ändern kann. Das Problem: er hängt
    an der Oberfläche, und eine Oberfläche ändert sich.
    """
    return {"works on": "die Oberfläche, nicht die Schnittstelle",
            "advantage": "keine Änderung am Altsystem nötig",
            "cost": "jede Änderung der Oberfläche bricht den Roboter",
            "nickname": "Klebeband, das funktioniert",
            "the fair description": "eine Brücke, bis die Schnittstelle "
                                    "da ist"}


def brittleness(changes, robots, coverage=0.6):
    """Schätzt, wie viele Roboter eine Änderungsrunde bricht.

    Raises:
        ValueError: bei negativen Zahlen oder einem Anteil ausserhalb
            von null bis eins.
    """
    if changes < 0 or robots < 0:
        raise ValueError("negative Zahl")
    if not 0.0 <= coverage <= 1.0:
        raise ValueError("Anteil ausserhalb von 0 bis 1")
    affected = min(robots, round(changes * coverage))
    return {"changes": changes, "robots": robots,
            "expected broken": affected,
            "share": affected / robots if robots else 0.0,
            "note": "die Wartung wächst mit der Zahl der Roboter und der "
                    "Änderungsrate der Systeme"}


def when_to_stop_at_rpa():
    """Nennt, wann die einfache Stufe die richtige ist.

    Wenn der Ablauf stabil ist, die Eingaben strukturiert sind und es
    keine Entscheidung gibt, die ein Modell treffen müsste, bringt die
    nächste Stufe nichts ausser Aufwand und Unsicherheit. Die Frage ist
    nicht, wie viel Intelligenz möglich ist, sondern wie viel der Fall
    verlangt.
    """
    return {"stop when": ["der Ablauf ist stabil",
                          "die Eingaben sind strukturiert",
                          "es gibt keine echte Entscheidung"],
            "go further when": ["die Eingabe ist Text oder Bild",
                                "die Regeln decken die Fälle nicht ab",
                                "die Ausnahmen sind die Mehrheit"],
            "the trap": "eine Stufe zu weit gehen, weil die Technik da ist"}
