"""Theoretische Kapazität und Auslastung eines Ressourcenpools."""


def theoretical_capacity(units, unit_load):
    """Wie viele Fälle ein Pool je Zeiteinheit schaffen kann.

    Die Formel der Vorlesung ist μ = uc/ul: die Zahl der verfügbaren
    Einheiten geteilt durch die Zeit, die eine Einheit für einen Fall
    braucht. Acht Sachbearbeiter mit je einer halben Stunde je Fall
    schaffen sechzehn Fälle in der Stunde.

    Args:
        units: die Zahl der Einheiten im Pool.
        unit_load: die Bearbeitungszeit eines Falles je Einheit.

    Raises:
        ValueError: bei einer nicht positiven Bearbeitungszeit oder einer
            negativen Zahl von Einheiten.
    """
    if unit_load <= 0:
        raise ValueError("die Bearbeitungszeit muss positiv sein")
    if units < 0:
        raise ValueError("negative Zahl von Einheiten")
    return units / unit_load


def utilisation(arrival, capacity):
    """Der Anteil der Kapazität, den die Nachfrage bindet.

    Raises:
        ValueError: bei einer nicht positiven Kapazität.
    """
    if capacity <= 0:
        raise ValueError("die Kapazität muss positiv sein")
    return arrival / capacity


def assess(arrival, capacity):
    """Beurteilt eine Auslastung.

    Über eins ist der Pool überlastet: es kommt mehr herein, als
    herausgeht, und die Warteschlange wächst ohne Grenze. Aber auch knapp
    darunter wird es unangenehm, weil die Wartezeit mit 1/(1 − ρ) wächst
    und in der Nähe von eins jede kleine Schwankung durchschlägt.

    Returns:
        Abbildung mit der Auslastung, der Beurteilung und der Folge.
    """
    value = utilisation(arrival, capacity)
    if value >= 1.0:
        return {"utilisation": value, "sustainable": False,
                "consequence": "the queue grows without bound"}
    if value > 0.9:
        return {"utilisation": value, "sustainable": True,
                "consequence": "every fluctuation shows up as waiting time"}
    return {"utilisation": value, "sustainable": True,
            "consequence": "the pool copes"}


def bottleneck(pools):
    """Nennt den Pool mit der höchsten Auslastung.

    Raises:
        ValueError: bei einer leeren Abbildung.
    """
    if not pools:
        raise ValueError("keine Pools")
    return max(sorted(pools), key=lambda name: pools[name])


def why_utilisation_is_not_a_target():
    """Sagt, warum volle Auslastung kein Ziel ist.

    Eine Ressource, die zu hundert Prozent ausgelastet ist, hat keine
    Reserve; jeder Ausfall und jede Schwankung schlägt unmittelbar auf die
    Wartezeit durch. In der Warteschlangenrechnung geht die Wartezeit bei
    ρ gegen eins gegen unendlich, lange bevor die Auslastung eins
    erreicht.
    """
    return {"looks efficient": True,
            "actually": "no reserve for variation or failure",
            "queueing says": "waiting time grows like 1/(1 - rho)",
            "practical ceiling": "around 0.8 for people"}
