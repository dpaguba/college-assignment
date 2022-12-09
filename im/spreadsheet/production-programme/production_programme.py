"""Die operative Programmplanung bei einem Engpass."""

CAPACITY = 500.0

PRODUCTS = (
    {"name": "A", "margin": 30.0, "usage": 2.0, "demand": 80},
    {"name": "B", "margin": 24.0, "usage": 3.0, "demand": 60},
    {"name": "C", "margin": 45.0, "usage": 5.0, "demand": 50},
    {"name": "D", "margin": 12.0, "usage": 1.0, "demand": 100},
    {"name": "E", "margin": 36.0, "usage": 6.0, "demand": 40},
)


def relative_margin(product):
    """Der Deckungsbeitrag je Engpasseinheit.

    Das ist die ganze Idee der Aufgabe: nicht der absolute Beitrag
    entscheidet, sondern der Beitrag je Einheit des knappen Faktors. Ein
    Produkt mit hohem Beitrag, das viel Kapazität frisst, verdrängt zwei
    Produkte, die zusammen mehr bringen.

    Raises:
        ValueError: bei einer nicht positiven Beanspruchung.
    """
    if product["usage"] <= 0:
        raise ValueError("die Engpassbeanspruchung muss positiv sein")
    return product["margin"] / product["usage"]


def ranking(products=PRODUCTS):
    """Ordnet die Produkte nach ihrem relativen Deckungsbeitrag."""
    return sorted(products, key=lambda row: (-relative_margin(row),
                                             row["name"]))


def programme(products=PRODUCTS, capacity=CAPACITY):
    """Stellt das Produktionsprogramm auf.

    Der Reihe nach wird jedes Produkt bis zur Absatzgrenze aufgenommen,
    solange Kapazität übrig ist; beim letzten reicht sie meist nur für
    einen Teil. Produkte, die nicht mehr hineinpassen, erscheinen mit
    Menge null, so wie die Aufgabe leere Ergebniszellen verlangt.

    Args:
        products: die Produkte.
        capacity: die Kapazitätsgrenze.

    Returns:
        Abbildung mit den Mengen, dem Deckungsbeitrag und der
        verbrauchten Kapazität.

    Raises:
        ValueError: bei einer negativen Kapazität.
    """
    if capacity < 0:
        raise ValueError("negative Kapazität")
    left = capacity
    quantities = {}
    total = 0.0
    for product in ranking(products):
        possible = int(min(product["demand"], left // product["usage"]))
        quantities[product["name"]] = possible
        left -= possible * product["usage"]
        total += possible * product["margin"]
    return {"quantities": quantities, "margin": total,
            "capacity used": capacity - left, "capacity left": left,
            "order": [product["name"] for product in ranking(products)]}


def exceeds_capacity(products=PRODUCTS, capacity=CAPACITY):
    """Teil a der Aufgabe: prüft, ob die volle Nachfrage passt.

    Gefragt wird, ob die Summe der Kapazitätsbeanspruchungen über der
    Grenze liegt, wenn jedes Produkt in seiner maximalen Absatzmenge
    gefertigt würde. Genau weil sie es tut, gibt es überhaupt etwas zu
    planen.

    Returns:
        Abbildung mit dem Bedarf, der Grenze und dem Urteil.
    """
    needed = sum(row["demand"] * row["usage"] for row in products)
    return {"needed": needed, "capacity": capacity,
            "exceeds": needed > capacity, "short by": needed - capacity}


def by_absolute_margin(products=PRODUCTS, capacity=CAPACITY):
    """Stellt das Programm nach dem absoluten Beitrag auf.

    Das ist die Reihenfolge, die sich aufdrängt und die falsche ist. Sie
    dient hier als Vergleich: der Unterschied zwischen beiden
    Ergebnissen ist der Wert der Kennzahl, um die es in der Aufgabe geht.
    """
    ordered = sorted(products, key=lambda row: (-row["margin"],
                                                row["name"]))
    left = capacity
    total = 0.0
    quantities = {}
    for product in ordered:
        possible = int(min(product["demand"], left // product["usage"]))
        quantities[product["name"]] = possible
        left -= possible * product["usage"]
        total += possible * product["margin"]
    return {"quantities": quantities, "margin": total,
            "order": [product["name"] for product in ordered]}


def what_the_right_order_is_worth(products=PRODUCTS, capacity=CAPACITY):
    """Vergleicht beide Reihenfolgen.

    Returns:
        Abbildung mit beiden Deckungsbeiträgen und dem Abstand.
    """
    right = programme(products, capacity)["margin"]
    wrong = by_absolute_margin(products, capacity)["margin"]
    return {"by relative margin": right, "by absolute margin": wrong,
            "difference": right - wrong,
            "share": (right - wrong) / right if right else 0.0}


def variable_capacity(steps=(300.0, 400.0, 500.0, 600.0, 700.0)):
    """Teil b: die Grenze soll sich ändern lassen, ohne die Formel zu ändern.

    Der Sinn der Aufgabe ist, die Kapazität in eine eigene Zelle zu legen
    und in der Formel darauf zu verweisen. Hier ist sie ein Parameter,
    und die Tabelle zeigt, was daran hängt.

    Returns:
        Abbildung von der Grenze auf den Deckungsbeitrag.
    """
    return {capacity: programme(PRODUCTS, capacity)["margin"]
            for capacity in steps}
