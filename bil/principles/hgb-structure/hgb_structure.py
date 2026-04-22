"""Die Gliederung der Bilanz und die Grössenklassen."""

ASSETS = (
    ("A. Anlagevermögen", ("I. Immaterielle Vermögensgegenstände",
                           "II. Sachanlagen", "III. Finanzanlagen")),
    ("B. Umlaufvermögen", ("I. Vorräte",
                           "II. Forderungen und sonstige "
                           "Vermögensgegenstände", "III. Wertpapiere",
                           "IV. Kassenbestand und Guthaben")),
    ("C. Rechnungsabgrenzungsposten", ()),
)

EQUITY = (
    ("A. Eigenkapital", ("I. Gezeichnetes Kapital", "II. Kapitalrücklage",
                         "III. Gewinnrücklagen", "IV. Gewinnvortrag",
                         "V. Jahresüberschuss")),
    ("B. Rückstellungen", ()),
    ("C. Verbindlichkeiten", ()),
    ("D. Rechnungsabgrenzungsposten", ()),
)

CLASSES = {
    "klein": {"balance sheet": 6000000, "revenue": 12000000,
              "employees": 50},
    "mittelgross": {"balance sheet": 20000000, "revenue": 40000000,
                    "employees": 250},
    "gross": {"balance sheet": float("inf"), "revenue": float("inf"),
              "employees": float("inf")},
}


def assets():
    """Nennt die Aktivseite nach § 266 HGB."""
    return [(name, list(parts)) for name, parts in ASSETS]


def equity_and_liabilities():
    """Nennt die Passivseite nach § 266 HGB."""
    return [(name, list(parts)) for name, parts in EQUITY]


def ordering_principle():
    """Nennt, wonach die Posten geordnet sind.

    Die Aktivseite steht nach steigender Liquidierbarkeit: zuerst, was
    dem Betrieb dauernd dient, zuletzt das Bargeld. Die Passivseite
    steht nach fallender Fristigkeit: zuerst das Eigenkapital, das gar
    nicht fällig wird, dann die Rückstellungen und die Verbindlichkeiten.
    Wer die Ordnung kennt, liest aus der Reihenfolge schon die
    Fristenstruktur.
    """
    return {"assets": "nach steigender Liquidierbarkeit",
            "equity and liabilities": "nach fallender Fristigkeit",
            "what it tells you": "die Fristenstruktur steht schon in der "
                                 "Reihenfolge"}


def size_class(balance_sheet, revenue, employees):
    """Bestimmt die Grössenklasse einer Kapitalgesellschaft.

    Eine Gesellschaft fällt in eine Klasse, wenn sie an zwei aufeinander
    folgenden Stichtagen mindestens zwei der drei Schwellen nicht
    überschreitet. Die Klasse entscheidet über den Umfang der
    Offenlegung und über die Prüfungspflicht, und deshalb liegt in ihrer
    Nähe eine handfeste Gestaltungsfrage.

    Raises:
        ValueError: bei negativen Werten.
    """
    for value in (balance_sheet, revenue, employees):
        if value < 0:
            raise ValueError("negativer Wert")
    for name in ("klein", "mittelgross"):
        limits = CLASSES[name]
        under = sum(1 for value, limit in
                    ((balance_sheet, limits["balance sheet"]),
                     (revenue, limits["revenue"]),
                     (employees, limits["employees"]))
                    if value <= limit)
        if under >= 2:
            return {"class": name, "criteria met": under,
                    "rule": "mindestens zwei von drei, an zwei "
                            "Stichtagen"}
    return {"class": "gross", "criteria met": 0,
            "rule": "mindestens zwei von drei, an zwei Stichtagen"}


def what_the_class_decides():
    """Nennt, was von der Grössenklasse abhängt.

    Der Umfang der Bilanz und der Gewinn- und Verlustrechnung, die
    Angaben im Anhang, ob ein Lagebericht nötig ist, ob geprüft werden
    muss und was offengelegt wird. Eine kleine Gesellschaft legt eine
    verkürzte Bilanz offen und keine Gewinn- und Verlustrechnung; wer
    also über einen Wettbewerber recherchiert, findet dort meist genau
    das nicht, was ihn interessiert.
    """
    return {"depends on the class": ["Umfang von Bilanz und GuV",
                                     "Anhangangaben", "Lagebericht",
                                     "Prüfungspflicht",
                                     "Umfang der Offenlegung"],
            "a small company discloses": "eine verkürzte Bilanz, keine GuV",
            "consequence": "über kleine Wettbewerber steht wenig im "
                           "Bundesanzeiger"}
