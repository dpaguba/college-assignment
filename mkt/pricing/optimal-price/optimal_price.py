"""Der gewinnmaximale Preis nach Cournot."""


def demand(price, intercept=1000.0, slope=20.0):
    """Die lineare Nachfrage x(p) = a − b·p.

    Raises:
        ValueError: bei einer nicht positiven Steigung.
    """
    if slope <= 0:
        raise ValueError("die Steigung muss positiv sein")
    return max(0.0, intercept - slope * price)


def profit(price, cost, intercept=1000.0, slope=20.0, fixed=0.0):
    """Der Gewinn bei einem Preis.

    Raises:
        ValueError: bei einer nicht positiven Steigung.
    """
    return (price - cost) * demand(price, intercept, slope) - fixed


def cournot_price(cost, intercept=1000.0, slope=20.0):
    """Der gewinnmaximale Preis.

    Aus ``G(p) = (p − k)(a − b·p)`` folgt durch Ableiten
    ``p* = (a/b + k)/2``: der Preis liegt genau in der Mitte zwischen den
    Stückkosten und dem Prohibitivpreis. Die Fixkosten kommen darin nicht
    vor, und das ist das Ergebnis, das am meisten überrascht: sie ändern
    den Gewinn, nicht den optimalen Preis.

    Raises:
        ValueError: bei einer nicht positiven Steigung oder wenn die
            Kosten über dem Prohibitivpreis liegen.
    """
    if slope <= 0:
        raise ValueError("die Steigung muss positiv sein")
    prohibitive = intercept / slope
    if cost >= prohibitive:
        raise ValueError("die Stückkosten liegen über dem Prohibitivpreis")
    return (prohibitive + cost) / 2


def by_search(cost, intercept=1000.0, slope=20.0, fixed=0.0, steps=20000):
    """Sucht das Maximum über ein Preisraster.

    Das ist die Gegenrechnung zur Formel und braucht keine Analysis.

    Raises:
        ValueError: bei einer nicht positiven Zahl von Schritten.
    """
    if steps < 2:
        raise ValueError("zu wenige Schritte")
    top = intercept / slope
    best = None
    for index in range(steps + 1):
        price = top * index / steps
        value = profit(price, cost, intercept, slope, fixed)
        if best is None or value > best[1]:
            best = (price, value)
    return {"price": best[0], "profit": best[1]}


def fixed_costs_do_not_move_it(cost=10.0, intercept=1000.0, slope=20.0):
    """Zeigt, dass die Fixkosten den optimalen Preis nicht ändern.

    Sie sind eine Konstante im Gewinn und verschwinden beim Ableiten. Wer
    einen Preis erhöht, weil die Miete gestiegen ist, handelt gegen die
    Rechnung: die Miete ändert, ob sich das Geschäft lohnt, nicht wie
    teuer verkauft werden sollte.

    Returns:
        Abbildung mit dem Preis bei verschiedenen Fixkosten.
    """
    found = {}
    for fixed in (0.0, 5000.0, 50000.0):
        found[fixed] = by_search(cost, intercept, slope, fixed)
    return {"prices": {fixed: round(row["price"], 4)
                       for fixed, row in found.items()},
            "profits": {fixed: round(row["profit"], 2)
                        for fixed, row in found.items()},
            "same price": len({round(row["price"], 4)
                               for row in found.values()}) == 1,
            "by formula": cournot_price(cost, intercept, slope)}


def amoroso_robinson(cost, intercept=1000.0, slope=20.0):
    """Prüft die Beziehung zwischen optimalem Preis und Elastizität.

    Im Optimum gilt ``p = k / (1 + 1/ε)``. Daraus folgt zweierlei: der
    optimale Preis liegt immer im elastischen Bereich, und je
    unelastischer die Nachfrage, desto höher der Aufschlag auf die
    Kosten. Bei Kosten von null ist die Elastizität im Optimum genau
    minus eins.

    Returns:
        Abbildung mit dem Preis, der Elastizität dort und der Probe.

    Raises:
        ValueError: bei unzulässigen Werten.
    """
    price = cournot_price(cost, intercept, slope)
    quantity = demand(price, intercept, slope)
    if quantity <= 0:
        raise ValueError("die Menge im Optimum ist null")
    value = -slope * price / quantity
    rebuilt = cost / (1 + 1 / value) if value != -1 else float("inf")
    return {"price": price, "elasticity": value,
            "price from the relation": rebuilt,
            "agree": cost == 0 or abs(rebuilt - price) < 1e-9,
            "always elastic": abs(value) > 1 or cost == 0}


def what_the_formula_hides():
    """Nennt, was zwischen der Formel und einer Preisentscheidung liegt.

    Sie setzt eine bekannte Nachfragefunktion voraus, einen Anbieter ohne
    Wettbewerber, ein Produkt ohne Nachbarn im eigenen Sortiment und
    Kunden, die den Preis nicht als Qualitätssignal lesen. Jede dieser
    Annahmen ist im Marketing gerade die Frage, um die es geht.
    """
    return ["die Nachfragefunktion ist bekannt",
            "es gibt keinen Wettbewerber, der reagiert",
            "das Produkt steht allein im Sortiment",
            "der Preis wird nicht als Qualitätssignal gelesen"]
