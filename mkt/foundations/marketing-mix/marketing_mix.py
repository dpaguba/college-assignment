"""Der Marketing-Mix und das Zusammenspiel seiner Teile."""

INSTRUMENTS = {
    "Produktpolitik": "was angeboten wird: Eigenschaften, Qualität, "
                      "Sortiment, Marke, Service",
    "Preispolitik": "zu welchen Bedingungen: Preis, Rabatte, "
                    "Zahlungsziele",
    "Distributionspolitik": "auf welchem Weg: Absatzkanäle, Logistik, "
                            "Verfügbarkeit",
    "Kommunikationspolitik": "wie es bekannt wird: Werbung, "
                             "Verkaufsförderung, Öffentlichkeitsarbeit, "
                             "persönlicher Verkauf",
}

EXTENDED = {"Personal": "wer die Leistung erbringt",
            "Prozesse": "wie die Leistung abläuft",
            "Ausstattung": "was der Kunde vom Unsichtbaren sieht"}


def instruments():
    """Nennt die vier klassischen Instrumente."""
    return dict(INSTRUMENTS)


def extended():
    """Nennt die drei Instrumente, die bei Dienstleistungen dazukommen.

    Eine Dienstleistung wird erbracht, während der Kunde dabei ist, und
    lässt sich vorher nicht ansehen. Deshalb werden die Menschen, der
    Ablauf und die sichtbare Ausstattung selbst zu Instrumenten: sie sind
    das, woran der Kunde die Qualität ablesen kann, bevor er sie erlebt.
    """
    return dict(EXTENDED)


def describe(name):
    """Beschreibt ein Instrument.

    Raises:
        ValueError: bei einem unbekannten Instrument.
    """
    if name in INSTRUMENTS:
        return INSTRUMENTS[name]
    if name in EXTENDED:
        return EXTENDED[name]
    raise ValueError("unbekanntes Instrument")


def consistency(decisions):
    """Prüft, ob die Entscheidungen zueinander passen.

    Der Mix wirkt als Ganzes: ein hoher Preis verlangt ein Produkt, das
    ihn trägt, einen Weg, der zu ihm passt, und eine Ansprache, die ihn
    erklärt. Ein Premiumpreis im Discounter ist kein kühner Schritt,
    sondern ein Widerspruch, und der Kunde löst ihn auf, indem er den
    Preis für den Fehler hält.

    Args:
        decisions: Abbildung mit ``Preisniveau``, ``Qualität``,
            ``Kanal`` und ``Ansprache``, je als Wert von eins bis fünf.

    Returns:
        Abbildung mit der Spannweite und dem Urteil.

    Raises:
        ValueError: bei einer fehlenden Angabe oder einem Wert
            ausserhalb der Skala.
    """
    required = ("Preisniveau", "Qualität", "Kanal", "Ansprache")
    for name in required:
        if name not in decisions:
            raise ValueError("es fehlt: %s" % name)
        if not 1 <= decisions[name] <= 5:
            raise ValueError("Wert ausserhalb der Skala von 1 bis 5")
    values = [decisions[name] for name in required]
    spread = max(values) - min(values)
    return {"spread": spread, "consistent": spread <= 1,
            "weakest link": min(required, key=lambda name: decisions[name]),
            "why": "der Kunde liest den Mix als Ganzes und löst einen "
                   "Widerspruch zu Ungunsten des Anbieters auf"}


def why_the_price_is_special():
    """Nennt, was den Preis von den anderen drei unterscheidet.

    Er ist das einzige Instrument, das Einnahmen erzeugt; alle anderen
    verursachen zunächst Kosten. Er ist das flexibelste, weil er sich
    über Nacht ändern lässt. Er wirkt am schnellsten auf Absatz und
    Marktanteil. Und er ist am schlechtesten zurückzunehmen, weil eine
    Senkung den Referenzpreis des Kunden mit senkt und die Erwartung
    bleibt.
    """
    return {"earns": "als einziges Instrument",
            "flexible": "über Nacht änderbar",
            "fast": "wirkt sofort auf Absatz und Marktanteil",
            "hard to undo": "eine Senkung senkt den Referenzpreis mit",
            "consequence": "Preissenkung ist die billigste Massnahme "
                           "heute und die teuerste über die Zeit"}
