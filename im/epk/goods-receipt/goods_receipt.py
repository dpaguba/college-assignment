"""Der Wareneingang, Aufgabe 2 des ersten Tutoriums."""

CHECKS = ("bestellt", "menge stimmt", "verpackung unbeschaedigt")


def accept(ordered, quantity_matches, packaging_intact):
    """Entscheidet über die Annahme einer Lieferung.

    Zuerst wird geprüft, ob das Material überhaupt bestellt wurde. Nur
    dann folgt die Mengenprüfung, und parallel dazu prüft ein zweiter
    Mitarbeiter die äussere Verpackung. Angenommen wird nur, wenn beide
    Prüfungen erfolgreich waren.

    Args:
        ordered: ob das Material bestellt war.
        quantity_matches: ob die Menge mit dem Lieferschein übereinstimmt.
        packaging_intact: ob die Verpackung unbeschädigt ist.

    Returns:
        Abbildung mit der Entscheidung und dem Grund.
    """
    if not ordered:
        return {"accepted": False, "reason": "nicht bestellt",
                "next": "Annahme verweigern"}
    reasons = []
    if not quantity_matches:
        reasons.append("Menge weicht vom Lieferschein ab")
    if not packaging_intact:
        reasons.append("Verpackung beschädigt")
    if reasons:
        return {"accepted": False, "reason": "; ".join(reasons),
                "next": "Annahme verweigern"}
    return {"accepted": True, "reason": "beide Prüfungen bestanden",
            "next": "Lieferung quittieren und Qualitätsprüfung beginnen"}


def after_quality_check(faultless):
    """Sagt, was nach der Qualitätsprüfung mit der Ware geschieht."""
    return {"next": "einlagern" if faultless else "beim Lieferanten "
            "reklamieren",
            "faultless": faultless}


def process():
    """Beschreibt den Ablauf und die Stellen, an denen parallel geprüft wird.

    Der Punkt der Aufgabe liegt im Teil c: die Verpackungsprüfung läuft
    gleichzeitig mit der Mengenprüfung und wird von einem anderen
    Mitarbeiter gemacht. Wer sie hintereinander modelliert, hat den
    Prozess beschrieben, den das Unternehmen nicht hat.

    Returns:
        Abbildung mit den Schritten und den Konnektoren.
    """
    return {
        "start": "Ware ist eingegangen",
        "steps": ["prüfen, ob das Material bestellt wurde",
                  "XOR: bestellt oder nicht bestellt",
                  "bestellt: AND aus Mengenprüfung und Verpackungsprüfung",
                  "AND-Zusammenführung beider Prüfungen",
                  "XOR: beide erfolgreich oder nicht",
                  "erfolgreich: AND aus Quittieren und Qualitätsprüfung",
                  "nicht erfolgreich: Annahme verweigern",
                  "XOR nach der Qualitätsprüfung: einlagern oder "
                  "reklamieren"],
        "connectors": {"nach der Bestellprüfung": "XOR",
                       "die beiden Prüfungen": "AND",
                       "nach den Prüfungen": "XOR",
                       "Quittieren und Qualitätsprüfung": "AND",
                       "nach der Qualitätsprüfung": "XOR"},
        "two people": "die Mengenprüfung und die Verpackungsprüfung machen "
                      "verschiedene Mitarbeiter, deshalb parallel",
    }


def outcomes():
    """Zählt alle acht Kombinationen der drei Prüfungen auf.

    Returns:
        Abbildung von den drei Wahrheitswerten auf die Entscheidung.
    """
    found = {}
    for ordered in (True, False):
        for quantity in (True, False):
            for packaging in (True, False):
                found[(ordered, quantity, packaging)] = accept(
                    ordered, quantity, packaging)["accepted"]
    return found


def the_short_circuit():
    """Nennt, was die erste Prüfung mit den anderen macht.

    War das Material nicht bestellt, wird die Annahme verweigert, ohne
    dass Menge oder Verpackung geprüft würden. In der Kette ist das eine
    exklusive Verzweigung vor der parallelen: von den acht Kombinationen
    der drei Prüfungen führen vier zum selben Ergebnis, weil die beiden
    anderen Prüfungen gar nicht stattfinden.
    """
    unordered = [key for key, accepted in outcomes().items()
                 if not key[0]]
    return {"combinations": 8, "decided by the first check": len(unordered),
            "why": "die beiden anderen Prüfungen laufen dann nicht",
            "in the model": "eine XOR-Verzweigung vor der AND-Verzweigung"}
