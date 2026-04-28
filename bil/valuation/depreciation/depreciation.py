"""Abschreibungsverfahren und der Wechsel zwischen ihnen."""


def linear(cost, salvage, years):
    """Die lineare Abschreibung: gleiche Beträge über die Nutzungsdauer.

    Raises:
        ValueError: bei einer nicht positiven Dauer oder einem
            Restwert über den Anschaffungskosten.
    """
    if years < 1:
        raise ValueError("die Nutzungsdauer muss mindestens ein Jahr sein")
    if salvage > cost or salvage < 0:
        raise ValueError("der Restwert liegt ausserhalb")
    amount = (cost - salvage) / years
    return [amount] * years


def declining(cost, salvage, years, rate):
    """Die geometrisch-degressive Abschreibung.

    Abgeschrieben wird ein fester Anteil des Restbuchwerts, nicht der
    Anschaffungskosten. Die Beträge werden deshalb jedes Jahr kleiner
    und erreichen die Null nie; im letzten Jahr wird auf den Restwert
    aufgefüllt.

    Raises:
        ValueError: bei einem Satz ausserhalb von null bis eins.
    """
    if not 0 < rate < 1:
        raise ValueError("der Satz liegt zwischen null und eins")
    if years < 1:
        raise ValueError("die Nutzungsdauer muss mindestens ein Jahr sein")
    value = cost
    amounts = []
    for year in range(years):
        amount = value * rate
        if year == years - 1 or value - amount < salvage:
            amount = value - salvage
        amounts.append(amount)
        value -= amount
    return amounts


def units_of_production(cost, salvage, total_units, used):
    """Die Leistungsabschreibung nach tatsächlicher Nutzung.

    Raises:
        ValueError: bei einer nicht positiven Gesamtleistung oder wenn
            mehr genutzt als vorgesehen wird.
    """
    if total_units <= 0:
        raise ValueError("die Gesamtleistung muss positiv sein")
    if sum(used) > total_units:
        raise ValueError("die Nutzung übersteigt die Gesamtleistung")
    per_unit = (cost - salvage) / total_units
    return [per_unit * amount for amount in used]


def switch_year(cost, salvage, years, rate):
    """Sucht das Jahr, in dem der Wechsel auf linear günstiger wird.

    Solange der degressive Betrag über dem liegt, was eine lineare
    Verteilung des Restbuchwerts auf die Restlaufzeit ergäbe, bleibt man
    degressiv; danach wird gewechselt. Der Wechsel ist steuerlich
    erlaubt und in der Gegenrichtung nicht.

    Returns:
        Abbildung mit dem Jahr und beiden Verläufen.

    Raises:
        ValueError: bei unzulässigen Werten.
    """
    if not 0 < rate < 1 or years < 1:
        raise ValueError("unzulässige Werte")
    value = cost
    found = None
    amounts = []
    for year in range(years):
        remaining = years - year
        degressive = value * rate
        straight = (value - salvage) / remaining
        if straight >= degressive and found is None:
            found = year + 1
        amount = max(degressive, straight) if found else degressive
        if year == years - 1:
            amount = value - salvage
        amounts.append(amount)
        value -= amount
    return {"switch in year": found, "amounts": amounts,
            "total": sum(amounts),
            "book value at the end": cost - sum(amounts)}


def totals_agree(cost=100000.0, salvage=10000.0, years=5, rate=0.4):
    """Prüft, dass alle Verfahren dieselbe Summe abschreiben.

    Wie verteilt wird, ist eine Frage des Verfahrens; wie viel verteilt
    wird, ist keine. Über die ganze Nutzungsdauer schreibt jedes
    Verfahren genau die Anschaffungskosten minus dem Restwert ab, und
    ein Verfahren, bei dem das nicht herauskommt, ist falsch gerechnet.

    Returns:
        Abbildung mit den Summen je Verfahren.
    """
    base = cost - salvage
    straight = sum(linear(cost, salvage, years))
    falling = sum(declining(cost, salvage, years, rate))
    switched = switch_year(cost, salvage, years, rate)["total"]
    usage = sum(units_of_production(cost, salvage, 1000,
                                    [200, 300, 200, 200, 100]))
    return {"base": base, "linear": straight, "declining": falling,
            "with switch": switched, "by usage": usage,
            "all agree": all(abs(value - base) < 1e-6
                             for value in (straight, falling, switched,
                                           usage))}


def why_the_method_matters_anyway():
    """Sagt, was sich mit dem Verfahren doch ändert.

    Die Summe bleibt, die Verteilung nicht, und daran hängen der
    ausgewiesene Erfolg der einzelnen Jahre, die Steuerzahlung in diesen
    Jahren und jede Kennzahl, die auf dem Buchwert aufbaut. Bei
    gleichbleibendem Geschäft verschiebt die degressive Abschreibung
    Gewinn nach hinten und damit Steuer, was einen Zinsvorteil ergibt,
    ohne dass ein Euro mehr verdient wird.
    """
    return {"same": "die Summe über die Nutzungsdauer",
            "different": ["der Erfolg je Jahr", "die Steuer je Jahr",
                          "jeder Buchwert und jede Kennzahl darauf"],
            "the gain from declining": "ein Zinsvorteil aus der späteren "
                                       "Steuer, kein zusätzlicher Gewinn"}
