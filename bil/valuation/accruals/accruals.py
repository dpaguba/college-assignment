"""Abgrenzung: Aufwand und Ertrag in die richtige Periode."""


def deferral(amount, months_paid, months_this_year=0,
             paid_in_advance=True):
    """Rechnet einen aktiven oder passiven Rechnungsabgrenzungsposten aus.

    Wer im Dezember die Miete für Januar bis März zahlt, hat drei
    Monate im Voraus bezahlt. Zwei davon gehören ins neue Jahr und
    stehen zum Stichtag als aktiver Abgrenzungsposten in der Bilanz.
    Der Aufwand folgt der Zeit, nicht der Zahlung.

    Args:
        amount: der gezahlte oder erhaltene Betrag.
        months_paid: für wie viele Monate er gilt.
        months_this_year: wie viele dieser Monate noch ins alte Jahr
            fallen.
        paid_in_advance: ob im Voraus gezahlt wurde.

    Returns:
        Abbildung mit der Aufteilung.

    Raises:
        ValueError: bei nicht positiven Angaben oder wenn mehr Monate
            ins alte Jahr fallen, als bezahlt wurden.
    """
    if amount <= 0 or months_paid <= 0:
        raise ValueError("Betrag und Monate müssen positiv sein")
    if not 0 <= months_this_year <= months_paid:
        raise ValueError("unzulässige Aufteilung der Monate")
    per_month = amount / months_paid
    this_year = months_this_year
    next_year = months_paid - this_year
    return {"per month": per_month,
            "this year": per_month * this_year,
            "carried forward": per_month * next_year,
            "position": "aktiver RAP" if paid_in_advance
                        else "passiver RAP",
            "why": "der Aufwand folgt der Zeit, nicht der Zahlung"}


def provision(likelihood, amount, reliable):
    """Beurteilt, ob eine Rückstellung zu bilden ist.

    Gebildet wird sie für eine Verpflichtung gegenüber einem Dritten,
    die wahrscheinlich ist und deren Höhe sich schätzen lässt. Fehlt die
    Wahrscheinlichkeit, so ist es ein Eventualverbindlichkeit für den
    Anhang; fehlt die Schätzbarkeit, ebenso.

    Args:
        likelihood: die Wahrscheinlichkeit der Inanspruchnahme.
        amount: der geschätzte Betrag.
        reliable: ob die Schätzung verlässlich ist.

    Returns:
        Abbildung mit dem Urteil.

    Raises:
        ValueError: bei einer Wahrscheinlichkeit ausserhalb von null bis
            eins oder einem negativen Betrag.
    """
    if not 0.0 <= likelihood <= 1.0:
        raise ValueError("Wahrscheinlichkeit ausserhalb von 0 bis 1")
    if amount < 0:
        raise ValueError("negativer Betrag")
    if likelihood > 0.5 and reliable:
        return {"book a provision": True, "amount": amount,
                "where": "Bilanz, Rückstellungen"}
    return {"book a provision": False, "amount": amount,
            "where": "Anhang, Eventualverbindlichkeit",
            "why": "nicht wahrscheinlich" if likelihood <= 0.5
                   else "nicht verlässlich schätzbar"}


def kinds_of_accrual():
    """Nennt die vier Fälle, die auseinandergehalten werden müssen.

    Zahlung und Erfolg fallen auf verschiedene Perioden, und je nachdem,
    welches zuerst kommt und in welche Richtung, entsteht ein anderer
    Posten. Die Tabelle ist klein und wird trotzdem regelmässig
    verwechselt.
    """
    return {
        "vor dem Stichtag gezahlt, Aufwand danach": "aktiver RAP",
        "vor dem Stichtag erhalten, Ertrag danach": "passiver RAP",
        "Aufwand vor dem Stichtag, Zahlung danach":
            "sonstige Verbindlichkeit oder Rückstellung",
        "Ertrag vor dem Stichtag, Zahlung danach": "Forderung",
    }


def matching(revenue_period, expense_period):
    """Prüft, ob Aufwand und Ertrag in derselben Periode stehen.

    Raises:
        ValueError: bei einer nicht positiven Periode.
    """
    if revenue_period < 1 or expense_period < 1:
        raise ValueError("die Periode muss positiv sein")
    return {"matched": revenue_period == expense_period,
            "gap": expense_period - revenue_period,
            "consequence": "der Erfolg wird in einer Periode zu hoch und "
                           "in der anderen zu niedrig ausgewiesen"
            if revenue_period != expense_period else "keine"}


def why_provisions_are_the_soft_spot():
    """Nennt, warum Rückstellungen die beweglichste Position sind.

    Sie beruhen auf einer Schätzung, und die Schätzung stammt vom
    Unternehmen. Wer den Erfolg dämpfen will, schätzt vorsichtig; wer
    ihn heben will, löst im Folgejahr auf. Beides ist im Rahmen
    vertretbar, beides ist schwer zu prüfen, und beides ist der Grund,
    warum die Entwicklung der Rückstellungen über mehrere Jahre gelesen
    wird und nicht ihr Stand.
    """
    return {"based on": "eine Schätzung des Unternehmens",
            "to lower profit": "vorsichtig schätzen",
            "to raise it later": "im Folgejahr auflösen",
            "how to read it": "die Entwicklung über Jahre, nicht den "
                              "Stand",
            "auditor's problem": "eine Schätzung lässt sich schwer "
                                 "widerlegen"}
