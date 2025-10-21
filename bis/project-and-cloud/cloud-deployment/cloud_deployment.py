"""Die Bereitstellungsmodelle und die wesentlichen Merkmale."""

MODELS = {
    "public": {"tenants": "beliebige Kunden",
               "operated by": "ein Anbieter",
               "combined": False,
               "argument": "günstig, weil die Kosten geteilt werden"},
    "private": {"tenants": "eine Organisation",
                "operated by": "die Organisation selbst oder ein "
                               "Dienstleister für sie",
                "combined": False,
                "argument": "Kontrolle über Daten und Standort"},
    "community": {"tenants": "mehrere Organisationen mit gemeinsamem "
                             "Anliegen",
                  "operated by": "eine davon oder ein Dienstleister",
                  "combined": False,
                  "argument": "gemeinsame Anforderungen, etwa an "
                              "Regulierung"},
    "hybrid": {"tenants": "beides",
               "operated by": "zwei Umgebungen, die verbunden sind",
               "combined": True,
               "argument": "die Spitzenlast nach aussen, die Kerndaten "
                           "nach innen"},
}

CHARACTERISTICS = {
    "On-demand self-service": "der Kunde bestellt ohne Zutun des "
                              "Anbieters",
    "Broad network access": "erreichbar über das Netz mit üblichen "
                            "Geräten",
    "Resource pooling": "die Ressourcen werden geteilt und dynamisch "
                        "zugeteilt",
    "Rapid elasticity": "die Menge passt sich schnell an, in beide "
                        "Richtungen",
    "Measured service": "die Nutzung wird gemessen und danach abgerechnet",
}


def characteristics():
    """Nennt die fünf wesentlichen Merkmale nach NIST."""
    return dict(CHARACTERISTICS)


def describe(model):
    """Beschreibt ein Bereitstellungsmodell.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    if model not in MODELS:
        raise ValueError("unbekanntes Bereitstellungsmodell")
    return dict(MODELS[model])


def virtualisation():
    """Nennt die Zahlen, die die Vorlesung der Virtualisierung gibt.

    Ohne Virtualisierung steht ein Server die meiste Zeit fast still;
    Unternehmen geben inzwischen oft mehr für Strom und Kühlung aus als
    vorher für die Hardware. Mit Virtualisierung lässt sich der
    durchschnittliche Nutzungsgrad auf siebzig Prozent oder mehr steigern,
    und es braucht weniger Rechner für dieselbe Arbeit.
    """
    return {"utilisation reached": 0.70,
            "spends more on": "Strom und Kühlung als vorher auf die "
                              "Hardware",
            "also enables": ["Drittsystem-Anwendungen auf demselben Server",
                             "ältere Betriebssystemversionen weiterbetreiben",
                             "zentrale Hardwareverwaltung"],
            "is the basis of": "die Ressourcenteilung in der Cloud"}


def choose(sensitive_data, load_peaks, budget):
    """Schlägt ein Bereitstellungsmodell vor.

    Args:
        sensitive_data: ob besonders schützenswerte Daten verarbeitet
            werden.
        load_peaks: ob die Last stark schwankt.
        budget: ob das Budget knapp ist.

    Returns:
        Abbildung mit dem Vorschlag und der Begründung.
    """
    if sensitive_data and load_peaks:
        return {"model": "hybrid",
                "why": "die Kerndaten bleiben innen, die Spitzen gehen "
                       "nach aussen"}
    if sensitive_data:
        return {"model": "private", "why": "Kontrolle über die Daten"}
    if budget:
        return {"model": "public", "why": "geteilte Kosten"}
    return {"model": "public",
            "why": "ohne besondere Anforderung ist das geteilte Modell "
                   "das einfachste"}
