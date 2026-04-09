"""Bilanzpolitik: was sich am Stichtag bewegen lässt."""

MEASURES = {
    "Sale and lease back": {"moves": "Anlagevermögen zu liquiden Mitteln",
                            "ratio improved": "Eigenkapitalquote und "
                                              "Liquidität",
                            "reality": "unverändert, die Miete kommt "
                                       "später"},
    "Factoring": {"moves": "Forderungen zu liquiden Mitteln",
                  "ratio improved": "Liquidität und Umschlagsdauer",
                  "reality": "die Gebühr mindert den Erfolg"},
    "Zahlungen verschieben": {"moves": "nichts, nur den Zeitpunkt",
                              "ratio improved": "der Kassenbestand am "
                                                "Stichtag",
                              "reality": "im Januar ist es wieder weg"},
    "Rückstellungen auflösen": {"moves": "Fremdkapital zu Eigenkapital",
                                "ratio improved": "Erfolg und "
                                                  "Eigenkapitalquote",
                                "reality": "der Anlass war schon vorher "
                                           "weg oder ist es nicht"},
    "Abschreibungsmethode wechseln": {"moves": "Erfolg zwischen Jahren",
                                      "ratio improved": "der Erfolg des "
                                                        "laufenden Jahres",
                                      "reality": "die Summe bleibt"},
}


def measures():
    """Nennt die üblichen Massnahmen."""
    return {name: dict(row) for name, row in MEASURES.items()}


def describe(name):
    """Beschreibt eine Massnahme.

    Raises:
        ValueError: bei einer unbekannten Massnahme.
    """
    if name not in MEASURES:
        raise ValueError("unbekannte Massnahme")
    return dict(MEASURES[name])


def sale_and_lease_back(sheet, book_value, price):
    """Rechnet die Wirkung eines Verkaufs mit Rückmiete vor.

    Das Anlagevermögen sinkt, die liquiden Mittel steigen, und der
    Unterschied zwischen Preis und Buchwert erhöht den Erfolg und damit
    das Eigenkapital. Die Bilanzsumme bleibt fast gleich, die
    Eigenkapitalquote steigt, und das Unternehmen benutzt dieselbe
    Maschine wie vorher.

    Args:
        sheet: die Bilanz.
        book_value: der Buchwert der verkauften Anlage.
        price: der Verkaufspreis.

    Returns:
        Abbildung mit der Bilanz vorher und nachher.

    Raises:
        ValueError: bei negativen Werten oder einem Buchwert über dem
            Anlagevermögen.
    """
    if book_value < 0 or price < 0:
        raise ValueError("negative Werte")
    if book_value > sheet["Anlagevermögen"]:
        raise ValueError("der Buchwert übersteigt das Anlagevermögen")
    after = dict(sheet)
    after["Anlagevermögen"] -= book_value
    after["liquide Mittel"] += price
    after["Eigenkapital"] += price - book_value
    return {"before": dict(sheet), "after": after,
            "gain": price - book_value,
            "what changed in the business": "nichts, die Anlage wird "
                                            "weiter genutzt",
            "what comes later": "die Miete, Jahr für Jahr"}


def factoring(sheet, receivables_sold, fee_rate=0.02):
    """Rechnet den Verkauf von Forderungen vor.

    Raises:
        ValueError: bei einem unzulässigen Satz oder mehr verkauften
            Forderungen als vorhanden.
    """
    if not 0 <= fee_rate < 1:
        raise ValueError("der Satz liegt zwischen null und eins")
    if receivables_sold > sheet["Forderungen"] or receivables_sold < 0:
        raise ValueError("unzulässige Menge an Forderungen")
    fee = receivables_sold * fee_rate
    after = dict(sheet)
    after["Forderungen"] -= receivables_sold
    after["liquide Mittel"] += receivables_sold - fee
    after["Eigenkapital"] -= fee
    return {"before": dict(sheet), "after": after, "fee": fee,
            "balance sheet shrinks by": fee,
            "note": "die Bilanzsumme sinkt, und das hebt jede Quote, die "
                    "die Bilanzsumme im Nenner hat"}


def what_to_look_for():
    """Nennt, woran ein Leser die Gestaltung erkennt.

    An der Häufung um den Stichtag, an einem Sprung in einer Quote ohne
    Sprung im Geschäft, an einem Methodenwechsel im Anhang, und an der
    Lücke zwischen Erfolg und operativem Cashflow. Keines davon beweist
    etwas; zusammen genommen sagen sie, wo genauer hinzusehen ist.
    """
    return ["eine Häufung von Vorgängen kurz vor dem Stichtag",
            "ein Sprung in einer Quote ohne Sprung im Geschäft",
            "ein Methodenwechsel im Anhang",
            "eine wachsende Lücke zwischen Erfolg und operativem "
            "Cashflow",
            "keines beweist etwas, zusammen sagen sie, wo hinzusehen ist"]


def the_line_to_fraud():
    """Zieht die Grenze, um die es geht.

    Bilanzpolitik nutzt Spielräume, die das Gesetz lässt, und ist
    zulässig; sie muss im Anhang stehen, soweit sie angabepflichtig ist.
    Bilanzfälschung erfindet Vorgänge oder verschweigt sie. Der
    Unterschied ist scharf und im Einzelfall schwer zu belegen, weil
    beides in denselben Zahlen ankommt und nur die Absicht und der
    Beleg sie trennen.
    """
    return {"Bilanzpolitik": "Spielräume nutzen, die das Gesetz lässt",
            "Bilanzfälschung": "Vorgänge erfinden oder verschweigen",
            "the difference": "scharf im Grundsatz, schwer im Beleg",
            "what separates them": "der Beleg und die Absicht, nicht die "
                                   "Zahl"}
