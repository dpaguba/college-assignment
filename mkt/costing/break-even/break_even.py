"""Die Break-Even-Analyse: ab welcher Menge der Verlust in Gewinn umschlägt."""

DANIELS = {"fixed": 500000.0, "variable": 4.0, "price": 14.0}


def unit_margin(price, variable):
    """Der Deckungsbeitrag je Stück: was nach den variablen Kosten bleibt.

    Raises:
        ValueError: wenn der Preis die variablen Kosten nicht übersteigt.
    """
    margin = price - variable
    if margin <= 0:
        raise ValueError("der Preis deckt nicht einmal die variablen "
                         "Kosten")
    return margin


def critical_quantity(fixed, variable, price, profit=0.0):
    """Die Menge, bei der die Kosten gedeckt sind.

    Aus ``Kf + kv·x = p·x`` folgt ``x = Kf/(p − kv)``. Mit einem
    Zielgewinn kommt er zu den Fixkosten hinzu: das Unternehmen muss ihn
    genauso verdienen wie seine festen Kosten.

    Args:
        fixed: die Fixkosten der Periode.
        variable: die variablen Kosten je Stück.
        price: der Preis je Stück.
        profit: der angestrebte Gewinn.

    Returns:
        Die kritische Menge.

    Raises:
        ValueError: bei negativen Fixkosten oder einem zu niedrigen Preis.
    """
    if fixed < 0:
        raise ValueError("negative Fixkosten")
    return (fixed + profit) / unit_margin(price, variable)


def profit_at(quantity, fixed, variable, price):
    """Der Gewinn bei einer Menge.

    Raises:
        ValueError: bei einer negativen Menge.
    """
    if quantity < 0:
        raise ValueError("negative Menge")
    return quantity * (price - variable) - fixed


def daniels_clear():
    """Die Übung: der alkoholfreie Whiskey.

    Fixkosten 500 000 Euro, variable Stückkosten 4 Euro, Preis 14 Euro.
    Die kritische Menge ist 50 000 Stück, mit einem Zielgewinn von
    600 000 Euro sind es 110 000, und der Deckungsbeitrag je Stück
    beträgt 10 Euro.

    Returns:
        Abbildung mit den drei Antworten.
    """
    row = DANIELS
    return {"unit margin": unit_margin(row["price"], row["variable"]),
            "break even": critical_quantity(row["fixed"], row["variable"],
                                            row["price"]),
            "for a profit of 600000":
                critical_quantity(row["fixed"], row["variable"],
                                  row["price"], 600000.0),
            "profit at the break even":
                profit_at(critical_quantity(row["fixed"], row["variable"],
                                            row["price"]),
                          row["fixed"], row["variable"], row["price"])}


def sensitivity(fixed=None, variable=None, price=None, change=0.1):
    """Zeigt, worauf die kritische Menge am stärksten reagiert.

    Der Preis steht im Nenner und wirkt deshalb stärker als die
    Fixkosten im Zähler: zehn Prozent weniger Preis heben die kritische
    Menge um mehr als zehn Prozent, zehn Prozent mehr Fixkosten heben
    sie um genau zehn.

    Returns:
        Abbildung mit der Änderung je Grösse.

    Raises:
        ValueError: bei einer nicht positiven Änderung.
    """
    if change <= 0:
        raise ValueError("die Änderung muss positiv sein")
    fixed = DANIELS["fixed"] if fixed is None else fixed
    variable = DANIELS["variable"] if variable is None else variable
    price = DANIELS["price"] if price is None else price
    base = critical_quantity(fixed, variable, price)
    return {"base": base,
            "fixed costs up": critical_quantity(fixed * (1 + change),
                                                variable, price) / base - 1,
            "price down": critical_quantity(fixed, variable,
                                            price * (1 - change)) / base - 1,
            "variable up": critical_quantity(fixed, variable * (1 + change),
                                             price) / base - 1,
            "change": change}


def what_the_analysis_assumes():
    """Nennt die Annahmen, unter denen die Rechnung gilt.

    Ein fester Preis unabhängig von der Menge, lineare variable Kosten,
    Fixkosten, die in der betrachteten Spanne wirklich fest sind, und
    ein Produkt. Jede davon fällt irgendwann: Mengenrabatte brechen die
    erste, Lernkurven die zweite, eine zweite Schicht die dritte, und
    bei mehreren Produkten muss erst geklärt werden, welche Fixkosten
    wem gehören.
    """
    return ["ein fester Preis, unabhängig von der Menge",
            "variable Kosten, die linear mit der Menge wachsen",
            "Fixkosten, die in der betrachteten Spanne fest bleiben",
            "ein Produkt, sonst ist die Zurechnung der Fixkosten offen"]
