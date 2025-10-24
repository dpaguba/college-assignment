"""IT-Outsourcing: die drei Bezugsquellen und die Rechnung dahinter."""

SOURCES = {
    "Kauf": "Software oder Softwarepakete von Händlern und "
            "Dienstleistern",
    "Software as a Service": "Onlinenutzung von Software bei einem "
                             "IT-Dienstleister",
    "Software-Outsourcing": "die individuelle Entwicklung an eine externe "
                            "Softwareschmiede verlagern",
}

ADVANTAGES = ("Kosteneinsparung", "Risikosenkung",
              "Konzentration auf Kernkompetenzen",
              "vermiedene Investitionen in neue Informationstechnologien",
              "Zugang zu Know-how und Experten")

DISADVANTAGES = ("Abhängigkeit vom Dienstleister",
                 "Herrschaftswissen wird abgegeben",
                 "Kontrollverlust und Kontrollkosten", "Qualitätsmängel",
                 "Ängste und Widerstände im Personal",
                 "Gefahr der Problemverlagerung")


def sources():
    """Nennt die drei externen Bezugsquellen."""
    return dict(SOURCES)


def assessment():
    """Stellt Vorteile und Nachteile gegenüber."""
    return {"advantages": list(ADVANTAGES),
            "disadvantages": list(DISADVANTAGES),
            "note": "die Gefahr der Problemverlagerung ist die stillste: "
                    "ein schlecht beherrschter Prozess wird nicht besser, "
                    "wenn ihn jemand anderes ausführt"}


def break_even(internal_fixed, internal_per_unit, external_per_unit):
    """Rechnet aus, ab welcher Menge der eigene Betrieb günstiger wird.

    Der eigene Betrieb kostet einen festen Betrag plus einen Satz je
    Einheit, der Dienstleister nur einen Satz je Einheit. Solange der
    externe Satz höher ist, gibt es eine Schwelle; ist er niedriger, gibt
    es keine, und dann entscheidet nicht der Preis.

    Args:
        internal_fixed: die Fixkosten des eigenen Betriebs.
        internal_per_unit: die eigenen Kosten je Einheit.
        external_per_unit: der Preis des Dienstleisters je Einheit.

    Returns:
        Abbildung mit der Schwelle.

    Raises:
        ValueError: bei negativen Beträgen oder wenn der externe Satz
            nicht über dem internen liegt.
    """
    for value in (internal_fixed, internal_per_unit, external_per_unit):
        if value < 0:
            raise ValueError("negativer Betrag")
    difference = external_per_unit - internal_per_unit
    if difference <= 0:
        raise ValueError("ohne Preisvorteil je Einheit gibt es keine "
                         "Schwelle")
    return {"units": internal_fixed / difference,
            "saving per unit": difference,
            "note": "unterhalb der Schwelle ist der Dienstleister "
                    "günstiger, oberhalb der eigene Betrieb"}


def compare(units, internal_fixed, internal_per_unit, external_per_unit):
    """Vergleicht beide Wege für eine bestimmte Menge.

    Raises:
        ValueError: bei einer negativen Menge oder einem negativen Betrag.
    """
    if units < 0:
        raise ValueError("negative Menge")
    for value in (internal_fixed, internal_per_unit, external_per_unit):
        if value < 0:
            raise ValueError("negativer Betrag")
    internal = internal_fixed + units * internal_per_unit
    external = units * external_per_unit
    return {"internal": internal, "external": external,
            "cheaper": "internal" if internal < external else "external",
            "difference": abs(internal - external)}


def what_the_calculation_leaves_out():
    """Nennt die Posten, die in der Rechnung fehlen.

    Der Preisvergleich erfasst die Rechnung des Dienstleisters, nicht die
    Kosten, ihn zu steuern: Verträge, Abnahmen, Eskalationen und das
    Wissen, das im eigenen Haus fehlt, sobald es dort niemand mehr
    braucht. Diese Kosten fallen später an und stehen in keinem Angebot.
    """
    return ["die Kosten der Steuerung des Dienstleisters",
            "der Aufwand für Verträge und Abnahmen",
            "das eigene Wissen, das ohne Übung verschwindet",
            "die Kosten eines späteren Wechsels",
            "alle vier fallen später an als die Einsparung"]
