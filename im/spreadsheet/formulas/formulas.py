"""Ein kleines Rechenblatt: Formeln, Bereiche und die Summe."""

import re

ADDRESS = re.compile(r"\$?([A-Z]{1,3})\$?([1-9][0-9]*)")
AREA = re.compile(r"(\$?[A-Z]{1,3}\$?[1-9][0-9]*):(\$?[A-Z]{1,3}\$?"
                  r"[1-9][0-9]*)")

VAT = 0.19

RECEIPT = {
    "C6": 2.49, "C7": 1.19, "C8": 0.89, "C9": 3.49, "C10": 1.99,
    "C11": 0.99, "C12": 4.29, "C13": 2.09,
    "C17": 12.99, "C18": 24.90,
    "D22": VAT,
}


def _key(letters, digits):
    """Baut den Schlüssel einer Zelle ohne Dollarzeichen."""
    return "%s%s" % (letters, digits)


def _cells_of(area):
    """Zählt die Zellen eines Bereichs auf."""
    first, second = AREA.fullmatch(area).groups()
    first = ADDRESS.fullmatch(first).groups()
    second = ADDRESS.fullmatch(second).groups()

    def number(letters):
        """Rechnet Buchstaben in eine Spaltennummer um."""
        value = 0
        for character in letters:
            value = value * 26 + (ord(character) - ord("A") + 1)
        return value

    def text(value):
        """Rechnet eine Spaltennummer zurück in Buchstaben."""
        letters = ""
        while value:
            value, rest = divmod(value - 1, 26)
            letters = chr(ord("A") + rest) + letters
        return letters

    columns = range(min(number(first[0]), number(second[0])),
                    max(number(first[0]), number(second[0])) + 1)
    rows = range(min(int(first[1]), int(second[1])),
                 max(int(first[1]), int(second[1])) + 1)
    return [_key(text(column), row) for row in rows for column in columns]


def evaluate(formula, sheet, names=None):
    """Wertet eine Formel über einem Blatt aus.

    Unterstützt werden Zahlen, Zellbezüge, Bereiche in ``SUMME``, die
    vier Grundrechenarten und Klammern. Ein Name steht für einen Bereich
    oder eine Zelle und wird vor der Auswertung ersetzt.

    Args:
        formula: die Formel, mit oder ohne führendes Gleichheitszeichen.
        sheet: Abbildung von der Zelle auf ihren Wert.
        names: Abbildung von Namen auf Bereiche.

    Returns:
        Der Wert.

    Raises:
        ValueError: bei einer Formel, die sich nicht auswerten lässt.
    """
    text = str(formula).strip().upper()
    if text.startswith("="):
        text = text[1:]
    for name, area in sorted((names or {}).items(),
                             key=lambda pair: -len(pair[0])):
        text = text.replace(name.upper(), area.upper())

    def sum_of(match):
        """Ersetzt eine Summe über einen Bereich durch ihren Wert."""
        return repr(sum(sheet.get(cell, 0.0)
                        for cell in _cells_of(match.group(1))))

    text = re.sub(r"SUMME\((%s)\)" % AREA.pattern, sum_of, text)
    text = re.sub(r"SUM\((%s)\)" % AREA.pattern, sum_of, text)

    def value_of(match):
        """Ersetzt einen Zellbezug durch seinen Wert."""
        return repr(sheet.get(_key(*match.groups()), 0.0))

    text = ADDRESS.sub(value_of, text)
    if not re.fullmatch(r"[0-9.+\-*/() eE]+", text):
        raise ValueError("die Formel enthält Unbekanntes: %s" % formula)
    try:
        return eval(text, {"__builtins__": {}}, {})
    except (SyntaxError, ZeroDivisionError) as problem:
        raise ValueError("die Formel lässt sich nicht auswerten: %s"
                         % problem)


def receipt(sheet=None):
    """Rechnet den Kassenzettel aus Aufgabe 2 des achten Tutoriums.

    Die Bruttopreise entstehen aus den Nettopreisen und dem Steuersatz in
    D22, und der Bezug auf D22 muss absolut sein, damit das Ausfüllen
    nach unten ihn stehen lässt.

    Returns:
        Abbildung mit den Brutto-Einzelwerten, den beiden Summen, der
        Gesamtsumme und dem Anteil der Lebensmittel.
    """
    values = dict(RECEIPT if sheet is None else sheet)
    food = ["C%d" % row for row in range(6, 14)]
    other = ["C17", "C18"]
    for source in food + other:
        target = "D" + source[1:]
        values[target] = evaluate("=%s*(1+$D$22)" % source, values)
    values["D14"] = evaluate("=SUMME(D6:D13)", values)
    values["D19"] = evaluate("=SUMME(D17:D18)", values)
    values["D20"] = values["D14"] + values["D19"]
    net = sum(values[cell] for cell in food + other)
    return {"gross per item": {cell: values["D" + cell[1:]]
                               for cell in food + other},
            "gross food": values["D14"], "gross other": values["D19"],
            "gross total": values["D20"], "net total": net,
            "food share": values["D14"] / values["D20"],
            "vat": values["D22"]}


def three_ways_to_the_total(values=None):
    """Zeigt die drei Wege zur Gesamtsumme aus Teil e der Aufgabe.

    Die Summe der beiden Teilsummen, die Summe über alle Bruttopreise,
    und der Nettobetrag mal eins plus Steuersatz. Alle drei müssen
    denselben Wert liefern; tun sie es nicht, ist ein Bereich falsch
    abgegrenzt, und dieser Vergleich findet den Fehler ohne dass jemand
    nachrechnet.

    Returns:
        Abbildung mit den drei Werten und dem Befund.
    """
    report = receipt(values)
    first = report["gross food"] + report["gross other"]
    second = sum(report["gross per item"].values())
    third = report["net total"] * (1 + report["vat"])
    spread = max(first, second, third) - min(first, second, third)
    return {"sum of the two subtotals": first,
            "sum over all gross prices": second,
            "net total times one plus the rate": third,
            "agree": spread < 1e-9, "spread": spread}


def why_the_third_way_is_the_check():
    """Sagt, welcher der drei Wege etwas prüft.

    Die ersten beiden benutzen dieselben Bruttowerte und gehen deshalb
    gemeinsam falsch, wenn eine Formel falsch ist. Der dritte rechnet am
    Bruttoblock vorbei, vom Netto aus. Nur er merkt, wenn eine
    Bruttoformel den falschen Nettopreis benutzt.
    """
    return {"first two": "benutzen dieselben Bruttowerte",
            "third": "rechnet vom Netto aus und geht an ihnen vorbei",
            "so": "der dritte ist die Probe, die ersten beiden sind zwei "
                  "Schreibweisen derselben Rechnung"}
