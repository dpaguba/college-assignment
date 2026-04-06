"""Kennzahlen aus der Bilanz."""

EXAMPLE = {
    "Anlagevermögen": 600000.0, "Vorräte": 200000.0,
    "Forderungen": 150000.0, "liquide Mittel": 50000.0,
    "Eigenkapital": 400000.0, "langfristiges Fremdkapital": 350000.0,
    "kurzfristiges Fremdkapital": 250000.0,
}


POSITIONS = ("Anlagevermögen", "Vorräte", "Forderungen",
             "liquide Mittel", "Eigenkapital",
             "langfristiges Fremdkapital", "kurzfristiges Fremdkapital")


def total(sheet=None):
    """Die Bilanzsumme.

    Raises:
        ValueError: bei einer fehlenden Position oder wenn die beiden
            Seiten nicht übereinstimmen.
    """
    sheet = EXAMPLE if sheet is None else sheet
    missing = [name for name in POSITIONS if name not in sheet]
    if missing:
        raise ValueError("es fehlen: %s" % ", ".join(missing))
    assets = (sheet["Anlagevermögen"] + sheet["Vorräte"]
              + sheet["Forderungen"] + sheet["liquide Mittel"])
    capital = (sheet["Eigenkapital"] + sheet["langfristiges Fremdkapital"]
               + sheet["kurzfristiges Fremdkapital"])
    if abs(assets - capital) > 1e-6:
        raise ValueError("die Bilanz geht nicht auf")
    return assets


def equity_ratio(sheet=None):
    """Die Eigenkapitalquote.

    Sie misst, welcher Anteil des Vermögens ohne Rückzahlungspflicht
    finanziert ist, und damit, wie viel Verlust das Unternehmen tragen
    kann, bevor es überschuldet ist.

    Raises:
        ValueError: wenn die Bilanz nicht aufgeht.
    """
    sheet = EXAMPLE if sheet is None else sheet
    return sheet["Eigenkapital"] / total(sheet)


def asset_coverage(sheet=None, degree=2):
    """Die Anlagendeckung im ersten oder zweiten Grad.

    Die goldene Bilanzregel verlangt, dass langfristig gebundenes
    Vermögen auch langfristig finanziert ist. Im ersten Grad zählt nur
    das Eigenkapital, im zweiten auch das langfristige Fremdkapital; der
    zweite Grad sollte über hundert Prozent liegen, sonst finanziert
    kurzfristiges Geld dauerhaftes Vermögen.

    Raises:
        ValueError: bei einem unbekannten Grad.
    """
    sheet = EXAMPLE if sheet is None else sheet
    if degree not in (1, 2):
        raise ValueError("der Grad ist eins oder zwei")
    capital = sheet["Eigenkapital"]
    if degree == 2:
        capital += sheet["langfristiges Fremdkapital"]
    return capital / sheet["Anlagevermögen"]


def liquidity(sheet=None, degree=1):
    """Die Liquidität ersten, zweiten oder dritten Grades.

    Der erste Grad stellt nur die flüssigen Mittel den kurzfristigen
    Schulden gegenüber, der zweite nimmt die Forderungen dazu, der
    dritte auch die Vorräte. Der zweite Grad sollte etwa hundert Prozent
    erreichen; der dritte deutlich mehr, weil Vorräte sich nicht auf
    Zuruf verkaufen.

    Raises:
        ValueError: bei einem unbekannten Grad.
    """
    sheet = EXAMPLE if sheet is None else sheet
    if degree not in (1, 2, 3):
        raise ValueError("der Grad liegt zwischen eins und drei")
    liquid = sheet["liquide Mittel"]
    if degree >= 2:
        liquid += sheet["Forderungen"]
    if degree >= 3:
        liquid += sheet["Vorräte"]
    return liquid / sheet["kurzfristiges Fremdkapital"]


def working_capital(sheet=None):
    """Das Nettoumlaufvermögen.

    Es ist der Teil des Umlaufvermögens, der nicht kurzfristig
    finanziert ist, und damit dieselbe Aussage wie die Liquidität
    dritten Grades, nur als Betrag statt als Verhältnis. Ein negativer
    Wert heisst, dass kurzfristiges Geld im Anlagevermögen steckt.

    Raises:
        ValueError: wenn die Bilanz nicht aufgeht.
    """
    sheet = EXAMPLE if sheet is None else sheet
    total(sheet)
    current = (sheet["Vorräte"] + sheet["Forderungen"]
               + sheet["liquide Mittel"])
    return {"working capital": current - sheet["kurzfristiges Fremdkapital"],
            "same statement as": "die Liquidität dritten Grades",
            "negative means": "kurzfristiges Geld finanziert das "
                              "Anlagevermögen"}


def report(sheet=None):
    """Rechnet alle Kennzahlen für eine Bilanz aus."""
    sheet = EXAMPLE if sheet is None else sheet
    return {"Bilanzsumme": total(sheet),
            "Eigenkapitalquote": equity_ratio(sheet),
            "Anlagendeckung I": asset_coverage(sheet, 1),
            "Anlagendeckung II": asset_coverage(sheet, 2),
            "Liquidität I": liquidity(sheet, 1),
            "Liquidität II": liquidity(sheet, 2),
            "Liquidität III": liquidity(sheet, 3),
            "Working Capital": working_capital(sheet)["working capital"]}


def why_a_ratio_needs_a_comparison():
    """Sagt, warum eine einzelne Kennzahl nichts aussagt.

    Eine Eigenkapitalquote von dreissig Prozent ist für einen
    Maschinenbauer solide und für eine Bank undenkbar. Ohne Vergleich
    bleibt nur die Bilanzsumme, und die sagt gar nichts. Verglichen wird
    mit dem eigenen Vorjahr, mit der Branche, und mit dem, was der
    Kreditvertrag verlangt.
    """
    return {"a number alone": "sagt nichts",
            "compare with": ["dem eigenen Vorjahr", "der Branche",
                             "den Auflagen des Kreditvertrags"],
            "example": "dreissig Prozent Eigenkapital sind im "
                       "Maschinenbau solide und bei einer Bank "
                       "undenkbar"}
