"""Die Gewinn- und Verlustrechnung in beiden Verfahren."""

TOTAL_COST = (
    ("Umsatzerlöse", 500000.0, "ertrag"),
    ("Bestandserhöhung", 20000.0, "ertrag"),
    ("Materialaufwand", 210000.0, "aufwand"),
    ("Personalaufwand", 150000.0, "aufwand"),
    ("Abschreibungen", 40000.0, "aufwand"),
    ("sonstige betriebliche Aufwendungen", 60000.0, "aufwand"),
)

SALES_COST = (
    ("Umsatzerlöse", 500000.0, "ertrag"),
    ("Herstellungskosten der verkauften Leistungen", 330000.0, "aufwand"),
    ("Vertriebskosten", 70000.0, "aufwand"),
    ("Verwaltungskosten", 40000.0, "aufwand"),
)


def result(rows):
    """Rechnet den Erfolg aus Erträgen und Aufwendungen.

    Raises:
        ValueError: bei einer unbekannten Art oder leeren Aufstellung.
    """
    if not rows:
        raise ValueError("leere Aufstellung")
    income = 0.0
    expense = 0.0
    for name, amount, kind in rows:
        if kind == "ertrag":
            income += amount
        elif kind == "aufwand":
            expense += amount
        else:
            raise ValueError("unbekannte Art: %s" % kind)
    return {"income": income, "expense": expense,
            "result": income - expense,
            "profit": income > expense}


def both_methods():
    """Vergleicht Gesamtkosten- und Umsatzkostenverfahren.

    Beide kommen zum selben Erfolg; sie ordnen die Aufwendungen nur
    anders. Das Gesamtkostenverfahren gliedert nach Kostenarten, also
    Material, Personal, Abschreibungen, und muss deshalb die
    Bestandsveränderung als Ertrag mitführen, weil sonst Aufwand für
    Erzeugnisse gezeigt würde, die noch im Lager liegen. Das
    Umsatzkostenverfahren gliedert nach Funktionen und stellt den
    Umsätzen nur die Herstellungskosten der verkauften Leistungen
    gegenüber, weshalb es die Bestandsveränderung gar nicht braucht.

    Returns:
        Abbildung mit beiden Erfolgen und dem Vergleich.
    """
    first = result(TOTAL_COST)
    second = result(SALES_COST)
    return {"Gesamtkostenverfahren": first["result"],
            "Umsatzkostenverfahren": second["result"],
            "same": abs(first["result"] - second["result"]) < 1e-9,
            "why the first needs the inventory change":
                "sonst stünde Aufwand für Erzeugnisse im Lager ohne "
                "Gegenposten",
            "what the second hides": "die Kostenarten, also wie viel "
                                     "Personal und wie viel Material"}


def inventory_change_matters(produced, sold, unit_cost):
    """Zeigt, was die Bestandsveränderung im Gesamtkostenverfahren tut.

    Wird mehr produziert als verkauft, so entsteht Aufwand für
    Erzeugnisse, die noch nicht verkauft sind. Ohne die Gegenbuchung
    sänke der Erfolg, obwohl nichts verloren ging. Die
    Bestandserhöhung ist deshalb kein Kunstgriff, sondern die
    Anwendung des Realisationsprinzips: der Aufwand wird dorthin
    verschoben, wo der Ertrag entsteht.

    Raises:
        ValueError: bei negativen Mengen oder Kosten.
    """
    if produced < 0 or sold < 0 or unit_cost < 0:
        raise ValueError("negative Menge oder Kosten")
    change = (produced - sold) * unit_cost
    return {"produced": produced, "sold": sold,
            "inventory change": change,
            "direction": "Erhöhung" if change > 0 else
                         "Minderung" if change < 0 else "keine",
            "why": "der Aufwand folgt dem Ertrag, nicht der Produktion"}


def structure():
    """Nennt die Gliederung nach § 275 HGB in Stichworten."""
    return ["Umsatzerlöse",
            "Bestandsveränderung und andere aktivierte Eigenleistungen",
            "sonstige betriebliche Erträge",
            "Materialaufwand",
            "Personalaufwand",
            "Abschreibungen",
            "sonstige betriebliche Aufwendungen",
            "Finanzergebnis",
            "Steuern",
            "Jahresüberschuss oder Jahresfehlbetrag"]


def why_the_result_is_not_the_cash():
    """Nennt den Unterschied, der die Kapitalflussrechnung nötig macht.

    Ein Erfolg entsteht, wenn ein Ertrag realisiert ist, und nicht, wenn
    Geld fliesst. Eine Abschreibung mindert den Erfolg ohne Zahlung,
    eine Tilgung zahlt ohne Aufwand, und eine Rechnung auf Ziel bringt
    Ertrag ohne Geld. Ein Unternehmen kann deshalb gewinnbringend
    zahlungsunfähig werden, und genau das kommt vor.
    """
    return {"depreciation": "Aufwand ohne Zahlung",
            "repayment": "Zahlung ohne Aufwand",
            "invoice on credit": "Ertrag ohne Zahlung",
            "consequence": "gewinnbringend und zahlungsunfähig zugleich "
                           "ist möglich",
            "the answer": "die Kapitalflussrechnung"}
