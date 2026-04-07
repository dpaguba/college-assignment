"""Die Kapitalflussrechnung nach der indirekten Methode."""

EXAMPLE = {
    "Jahresüberschuss": 60000.0,
    "Abschreibungen": 40000.0,
    "Zunahme Rückstellungen": 5000.0,
    "Zunahme Vorräte": 20000.0,
    "Zunahme Forderungen": 15000.0,
    "Zunahme Verbindlichkeiten aus L+L": 10000.0,
    "Auszahlungen für Anlagen": 70000.0,
    "Einzahlungen aus Anlagenabgang": 5000.0,
    "Aufnahme Darlehen": 30000.0,
    "Tilgung Darlehen": 12000.0,
    "Ausschüttung": 20000.0,
}


def operating(rows=None):
    """Der Cashflow aus der laufenden Geschäftstätigkeit.

    Ausgangspunkt ist der Jahresüberschuss. Zurückgerechnet wird alles,
    was den Erfolg verändert hat, ohne Geld zu bewegen: Abschreibungen
    hinzu, ebenso die Zunahme der Rückstellungen. Und alles, was Geld
    bewegt, ohne den Erfolg zu berühren: eine Zunahme der Vorräte und
    der Forderungen bindet Geld und wird abgezogen, eine Zunahme der
    Lieferantenschulden setzt Geld frei und wird addiert.

    Raises:
        ValueError: bei einer fehlenden Position.
    """
    rows = EXAMPLE if rows is None else rows
    needed = ("Jahresüberschuss", "Abschreibungen",
              "Zunahme Rückstellungen", "Zunahme Vorräte",
              "Zunahme Forderungen", "Zunahme Verbindlichkeiten aus L+L")
    missing = [name for name in needed if name not in rows]
    if missing:
        raise ValueError("es fehlen: %s" % ", ".join(missing))
    return (rows["Jahresüberschuss"] + rows["Abschreibungen"]
            + rows["Zunahme Rückstellungen"] - rows["Zunahme Vorräte"]
            - rows["Zunahme Forderungen"]
            + rows["Zunahme Verbindlichkeiten aus L+L"])


def investing(rows=None):
    """Der Cashflow aus der Investitionstätigkeit.

    Raises:
        ValueError: bei einer fehlenden Position.
    """
    rows = EXAMPLE if rows is None else rows
    for name in ("Auszahlungen für Anlagen", "Einzahlungen aus "
                 "Anlagenabgang"):
        if name not in rows:
            raise ValueError("es fehlt: %s" % name)
    return (rows["Einzahlungen aus Anlagenabgang"]
            - rows["Auszahlungen für Anlagen"])


def financing(rows=None):
    """Der Cashflow aus der Finanzierungstätigkeit.

    Raises:
        ValueError: bei einer fehlenden Position.
    """
    rows = EXAMPLE if rows is None else rows
    for name in ("Aufnahme Darlehen", "Tilgung Darlehen", "Ausschüttung"):
        if name not in rows:
            raise ValueError("es fehlt: %s" % name)
    return (rows["Aufnahme Darlehen"] - rows["Tilgung Darlehen"]
            - rows["Ausschüttung"])


def statement(rows=None):
    """Stellt die drei Bereiche zusammen.

    Die Summe der drei ist die Veränderung des Finanzmittelbestands, und
    das ist die Probe: sie muss dem Unterschied der Bankbestände zweier
    Bilanzen entsprechen. Stimmt sie nicht, fehlt eine Position, und die
    Differenz sagt welche Grössenordnung.

    Returns:
        Abbildung mit den drei Bereichen und der Summe.
    """
    rows = EXAMPLE if rows is None else rows
    first = operating(rows)
    second = investing(rows)
    third = financing(rows)
    return {"operating": first, "investing": second, "financing": third,
            "change in cash": first + second + third}


def reads_as(report=None):
    """Liest ein Vorzeichenmuster als Lage des Unternehmens.

    Die drei Vorzeichen zusammen erzählen mehr als jede einzelne Zahl.
    Positiv, negativ, negativ ist der gesunde Normalfall: das Geschäft
    trägt sich, es wird investiert und getilgt. Negativ, negativ,
    positiv ist das junge Unternehmen, das von Kapitalgebern lebt.
    Positiv, positiv, negativ ist oft ein Rückzug: es wird verkauft,
    was da ist, und damit werden Schulden getilgt.

    Returns:
        Abbildung mit dem Muster und seiner üblichen Deutung.
    """
    report = statement() if report is None else report
    pattern = tuple("+" if report[name] > 0 else "-"
                    for name in ("operating", "investing", "financing"))
    meanings = {
        ("+", "-", "-"): "der gesunde Normalfall: das Geschäft trägt "
                         "Investition und Tilgung",
        ("-", "-", "+"): "ein junges Unternehmen, das von Kapitalgebern "
                         "lebt",
        ("+", "+", "-"): "ein Rückzug: verkaufen und tilgen",
        ("+", "-", "+"): "starkes Wachstum, das aus beiden Quellen "
                         "finanziert wird",
    }
    return {"pattern": "".join(pattern),
            "reading": meanings.get(pattern, "kein übliches Muster"),
            "values": {name: report[name] for name in
                       ("operating", "investing", "financing")}}


def why_it_is_harder_to_dress_up():
    """Sagt, warum die Kapitalflussrechnung schwerer zu gestalten ist.

    Sie kennt keine Bewertungswahlrechte. Eine andere Abschreibung
    verändert den Jahresüberschuss und wird im selben Schritt wieder
    hinzugerechnet, sodass der Cashflow unverändert bleibt. Was ihn
    verändert, ist nur der Zeitpunkt von Zahlungen, und der lässt sich
    verschieben, aber nicht erfinden.

    Deshalb wird sie gelesen, wenn der Gewinn und die Zahlungsfähigkeit
    auseinanderlaufen, und deshalb ist die Kombination aus steigendem
    Gewinn und fallendem operativem Cashflow das bekannteste Warnzeichen
    der Bilanzanalyse.
    """
    return {"no valuation options": "eine andere Abschreibung hebt sich "
                                    "im selben Schritt wieder auf",
            "what can be moved": "der Zeitpunkt von Zahlungen",
            "warning sign": "steigender Gewinn bei fallendem operativem "
                            "Cashflow",
            "what it usually means": "der Erfolg steckt in Forderungen "
                                     "und Vorräten"}
