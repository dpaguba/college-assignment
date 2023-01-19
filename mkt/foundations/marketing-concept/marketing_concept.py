"""Was Marketing ist und wovon es sich abgrenzt."""

ORIENTATIONS = {
    "Produktionsorientierung": "verkauft wird, was hergestellt werden "
                               "kann; der Engpass ist die Produktion",
    "Produktorientierung": "das bessere Produkt setzt sich durch; der "
                          "Massstab ist die Technik",
    "Verkaufsorientierung": "was hergestellt wurde, muss verkauft "
                           "werden; der Druck liegt beim Vertrieb",
    "Marktorientierung": "hergestellt wird, was am Markt gebraucht "
                        "wird; der Ausgangspunkt ist der Kunde",
}


def orientations():
    """Nennt die Entwicklungsstufen der Unternehmensausrichtung."""
    return dict(ORIENTATIONS)


def definition():
    """Gibt die Definition wieder, mit der die Vorlesung arbeitet.

    Marketing ist die Ausrichtung des ganzen Unternehmens am Markt, nicht
    eine Abteilung neben Produktion und Vertrieb. Die enge Lesart, nach
    der Marketing Werbung heisst, ist die Verkaufsorientierung unter
    neuem Namen.
    """
    return {"marketing is": "die Ausrichtung des Unternehmens am Markt",
            "not": "eine Abteilung für Werbung",
            "the test": "wer entscheidet, was hergestellt wird",
            "under production orientation": "die Produktion",
            "under market orientation": "der Markt"}


def where_it_sits_in_business_studies():
    """Ordnet das Fach in die Betriebswirtschaftslehre ein.

    Die BWL beschreibt Entscheidungen über knappe Mittel im Unternehmen.
    Die Funktionslehren teilen sie nach Bereichen auf: Beschaffung,
    Produktion, Absatz, Finanzierung, Personal. Marketing ist die Lehre
    vom Absatz und greift von dort aus in alle anderen ein, weil der
    Absatz bestimmt, was die anderen tun müssen.
    """
    return {"BWL": "Entscheidungen über knappe Mittel",
            "Funktionslehren": ["Beschaffung", "Produktion", "Absatz",
                                "Finanzierung", "Personal"],
            "marketing": "die Lehre vom Absatz",
            "why it reaches into the others": "der Absatz bestimmt, was "
                                              "die anderen tun müssen"}


def needs_wants_demand():
    """Trennt drei Begriffe, die im Alltag zusammenfallen.

    Ein Bedürfnis ist ein Mangelgefühl und liegt vor jedem Angebot. Ein
    Bedarf ist ein Bedürfnis, das sich auf ein bestimmtes Angebot
    richtet. Nachfrage ist Bedarf mit Kaufkraft. Werbung schafft keine
    Bedürfnisse; sie lenkt Bedürfnisse auf Angebote und macht daraus
    Bedarf.
    """
    return {"Bedürfnis": "ein Mangelgefühl, liegt vor dem Angebot",
            "Bedarf": "ein Bedürfnis, das auf ein Angebot gerichtet ist",
            "Nachfrage": "Bedarf mit Kaufkraft",
            "what advertising does": "es lenkt, es erschafft nicht"}


def market_definition(same_needs, substitutes):
    """Grenzt einen Markt ab.

    Zum selben Markt gehört, was dasselbe Bedürfnis befriedigt und
    füreinander einspringen kann. Die Abgrenzung entscheidet über den
    Marktanteil und damit über fast jede Kennzahl, die daraufhin
    berechnet wird; sie ist deshalb keine Vorfrage, sondern die
    Entscheidung.

    Raises:
        ValueError: bei leeren Angaben.
    """
    if not same_needs or not substitutes:
        raise ValueError("beide Angaben werden gebraucht")
    return {"same market": sorted(set(same_needs) & set(substitutes)),
            "same need only": sorted(set(same_needs) - set(substitutes)),
            "why it matters": "die Abgrenzung bestimmt den Marktanteil "
                              "und damit jede Kennzahl darauf"}
