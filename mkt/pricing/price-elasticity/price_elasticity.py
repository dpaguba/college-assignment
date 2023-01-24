"""Die Preiselastizität der Nachfrage."""


def linear_demand(price, intercept=1000.0, slope=20.0):
    """Eine lineare Nachfragefunktion x(p) = a − b·p.

    Raises:
        ValueError: bei einer negativen Steigung oder einem negativen
            Preis.
    """
    if slope < 0 or price < 0:
        raise ValueError("negative Steigung oder negativer Preis")
    return max(0.0, intercept - slope * price)


def elasticity(price, intercept=1000.0, slope=20.0):
    """Die Elastizität an einer Stelle.

    Sie ist die prozentuale Mengenänderung je Prozent Preisänderung, also
    die Ableitung mal dem Verhältnis von Preis zu Menge. Bei linearer
    Nachfrage ist sie nicht konstant: sie geht von null beim Preis null
    bis minus unendlich am Prohibitivpreis, und genau in der Mitte ist
    sie minus eins.

    Raises:
        ValueError: bei einer Menge von null.
    """
    quantity = linear_demand(price, intercept, slope)
    if quantity <= 0:
        raise ValueError("die Menge ist null, die Elastizität ist nicht "
                         "definiert")
    return -slope * price / quantity


def by_difference(price, step=0.001, intercept=1000.0, slope=20.0):
    """Nähert die Elastizität über eine kleine Preisänderung.

    Das ist die Gegenrechnung zur Formel: die Ableitung wird durch einen
    Differenzenquotienten ersetzt, und beides muss übereinstimmen.

    Raises:
        ValueError: bei einer nicht positiven Schrittweite.
    """
    if step <= 0:
        raise ValueError("die Schrittweite muss positiv sein")
    first = linear_demand(price, intercept, slope)
    second = linear_demand(price + step, intercept, slope)
    if first <= 0:
        raise ValueError("die Menge ist null")
    return ((second - first) / first) / (step / price)


def classify(value):
    """Ordnet eine Elastizität ein.

    Raises:
        ValueError: bei einer positiven Elastizität, die für ein
            gewöhnliches Gut nicht vorkommt.
    """
    if value > 0:
        raise ValueError("eine positive Elastizität deutet auf ein "
                         "Giffen- oder Veblen-Gut")
    size = abs(value)
    if size > 1:
        return "elastisch"
    if size < 1:
        return "unelastisch"
    return "einheitselastisch"


def revenue_direction(value):
    """Sagt, wohin der Umsatz bei einer Preiserhöhung geht.

    Im elastischen Bereich fällt der Umsatz bei einer Preiserhöhung, im
    unelastischen steigt er, und beim Wert minus eins ist er im Maximum.
    Das ist der ganze praktische Gehalt der Kennzahl.

    Raises:
        ValueError: bei einer positiven Elastizität.
    """
    kind = classify(value)
    return {"elastisch": "der Umsatz fällt",
            "unelastisch": "der Umsatz steigt",
            "einheitselastisch": "der Umsatz bleibt, er ist im Maximum"
            }[kind]


def where_revenue_peaks(intercept=1000.0, slope=20.0):
    """Sucht den Preis mit dem höchsten Umsatz.

    Er liegt beim halben Prohibitivpreis, und dort ist die Elastizität
    genau minus eins. Beide Wege führen zur selben Stelle, und das ist
    die Probe.

    Returns:
        Abbildung mit dem Preis, dem Umsatz und der Elastizität dort.
    """
    best = None
    steps = 5000
    top = intercept / slope
    for index in range(1, steps):
        price = top * index / steps
        revenue = price * linear_demand(price, intercept, slope)
        if best is None or revenue > best[1]:
            best = (price, revenue)
    return {"price by search": best[0], "revenue": best[1],
            "price by formula": top / 2,
            "elasticity there": elasticity(top / 2, intercept, slope),
            "agree": abs(best[0] - top / 2) < top / steps * 2}


def why_the_number_is_hard_to_get():
    """Nennt, warum die Elastizität selten bekannt ist.

    Sie verlangt zu wissen, was bei einem anderen Preis geschehen wäre,
    und das lässt sich nur beobachten, wenn der Preis tatsächlich anders
    war. Historische Daten helfen wenig, weil sich mit dem Preis meist
    auch etwas anderes geändert hat; und ein Versuch mit verschiedenen
    Preisen ist möglich, aber sichtbar, und Kunden reagieren darauf.
    """
    return {"needs": "was bei einem anderen Preis geschehen wäre",
            "history": "mit dem Preis änderte sich meist noch etwas",
            "experiment": "möglich, aber sichtbar",
            "consequence": "die Zahl ist meist geschätzt, und die "
                           "Empfehlung ist so gut wie die Schätzung"}
