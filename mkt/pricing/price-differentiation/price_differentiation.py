"""Preisdifferenzierung: verschiedene Preise für dasselbe Produkt."""

KINDS = {
    "personell": "nach Kundengruppe: Studierende, Senioren, Kinder",
    "zeitlich": "nach Zeitpunkt: Happy Hour, Nebensaison, Frühbucher",
    "räumlich": "nach Ort: Land, Region, Innenstadt gegen Rand",
    "mengenmässig": "nach Menge: Staffelpreise, Mehrstückpackungen",
    "leistungsbezogen": "nach Ausstattung: Basis, Komfort, Premium",
}


def kinds():
    """Nennt die Formen der Differenzierung."""
    return dict(KINDS)


def describe(kind):
    """Beschreibt eine Form.

    Raises:
        ValueError: bei einer unbekannten Form.
    """
    if kind not in KINDS:
        raise ValueError("unbekannte Form")
    return KINDS[kind]


def degrees():
    """Nennt die drei Grade nach Pigou.

    Beim ersten zahlt jeder Kunde genau seine Zahlungsbereitschaft; das
    schöpft die ganze Rente ab und ist praktisch kaum erreichbar. Beim
    zweiten wählt der Kunde selbst aus einem Menü, das so gebaut ist,
    dass die Wahl ihn verrät. Beim dritten teilt der Anbieter nach einem
    beobachtbaren Merkmal ein.
    """
    return {"erster Grad": "individueller Preis je Zahlungsbereitschaft",
            "zweiter Grad": "der Kunde wählt aus einem Menü und verrät "
                            "sich dabei",
            "dritter Grad": "Einteilung nach einem beobachtbaren Merkmal"}


def uniform_profit(segments, cost):
    """Der Gewinn bei einem einheitlichen Preis.

    Gesucht wird der beste einheitliche Preis über alle Segmente; wer
    mehr zahlen würde, zahlt ihn nicht, und wer weniger zahlen kann,
    kauft nicht.

    Args:
        segments: Paare aus Zahlungsbereitschaft und Zahl der Kunden.
        cost: die variablen Stückkosten.

    Returns:
        Abbildung mit dem besten Preis und dem Gewinn.

    Raises:
        ValueError: ohne Segmente.
    """
    if not segments:
        raise ValueError("keine Segmente")
    best = None
    for price, _ in segments:
        sold = sum(count for willing, count in segments if willing >= price)
        value = sold * (price - cost)
        if best is None or value > best[1]:
            best = (price, value)
    return {"price": best[0], "profit": best[1]}


def differentiated_profit(segments, cost):
    """Der Gewinn, wenn jedes Segment seinen eigenen Preis zahlt.

    Raises:
        ValueError: ohne Segmente.
    """
    if not segments:
        raise ValueError("keine Segmente")
    return {"prices": {willing: willing for willing, _ in segments},
            "profit": sum(count * (willing - cost)
                          for willing, count in segments
                          if willing > cost)}


def what_it_is_worth(segments=None, cost=10.0):
    """Vergleicht beide Wege an einem Beispiel.

    Drei Segmente mit Zahlungsbereitschaften von 60, 40 und 20 Euro und
    je hundert Kunden. Bei einem einheitlichen Preis ist die beste Wahl
    ein Kompromiss; bei getrennten Preisen wird jedes Segment
    abgeschöpft, und der Unterschied ist der Wert der Differenzierung.

    Returns:
        Abbildung mit beiden Gewinnen.
    """
    segments = [(60.0, 100), (40.0, 100), (20.0, 100)] if segments is None \
        else segments
    uniform = uniform_profit(segments, cost)
    apart = differentiated_profit(segments, cost)
    return {"uniform": uniform, "differentiated": apart,
            "gain": apart["profit"] - uniform["profit"],
            "share": (apart["profit"] - uniform["profit"])
            / apart["profit"] if apart["profit"] else 0.0}


def what_it_needs():
    """Nennt die Bedingungen, ohne die die Differenzierung zerfällt.

    Die Segmente müssen sich trennen lassen, und zwar nach einem
    Merkmal, das der Kunde nicht einfach vorgeben kann. Der Weiterverkauf
    vom billigen ins teure Segment muss ausgeschlossen sein, sonst
    übernimmt ihn ein Dritter. Und die Kunden dürfen die Trennung nicht
    als unfair empfinden, sonst kostet sie mehr, als sie einbringt.

    Der zweite Punkt ist der Grund, warum Dienstleistungen sich leichter
    differenzieren lassen als Waren: einen Haarschnitt kann man nicht
    weiterverkaufen.
    """
    return ["die Segmente müssen trennbar sein",
            "das Merkmal darf nicht frei wählbar sein",
            "der Weiterverkauf muss ausgeschlossen sein",
            "die Kunden dürfen es nicht als unfair empfinden",
            "deshalb sind Dienstleistungen leichter zu differenzieren"]
