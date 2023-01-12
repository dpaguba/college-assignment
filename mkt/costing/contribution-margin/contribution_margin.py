"""Die einstufige Deckungsbeitragsrechnung."""

PRODUCTS = (
    {"name": "Standmixer", "quantity": 300, "price": 40.0,
     "variable": 24.0, "area": "A"},
    {"name": "Stabmixer", "quantity": 405, "price": 50.0,
     "variable": 29.0, "area": "A"},
    {"name": "Universalzerkleinerer", "quantity": 200, "price": 100.0,
     "variable": 7.0, "area": "A"},
    {"name": "Handrührer", "quantity": 100, "price": 30.0,
     "variable": 37.0, "area": "B"},
    {"name": "Küchenmaschine", "quantity": 150, "price": 90.0,
     "variable": 42.0, "area": "B"},
)

TOTAL_FIXED = 25000.0


def unit_margin(product):
    """Der Deckungsbeitrag je Stück eines Produktes."""
    return product["price"] - product["variable"]


def product_margin(product):
    """Der Deckungsbeitrag eines Produktes über seine Absatzmenge."""
    return product["quantity"] * unit_margin(product)


def single_stage(products=PRODUCTS, fixed=TOTAL_FIXED):
    """Rechnet den Erfolg einstufig aus.

    Alle Deckungsbeiträge werden addiert und die gesamten Fixkosten in
    einem Zug abgezogen. Das Ergebnis ist richtig und sagt nichts
    darüber, wo das Geld verdient wird.

    Returns:
        Abbildung mit den Beiträgen und dem Erfolg.
    """
    margins = {product["name"]: product_margin(product)
               for product in products}
    return {"margins": margins, "sum": sum(margins.values()),
            "fixed": fixed, "profit": sum(margins.values()) - fixed}


def loss_makers(products=PRODUCTS):
    """Nennt die Produkte mit negativem Deckungsbeitrag.

    Ein negativer Deckungsbeitrag heisst, dass jedes verkaufte Stück
    Geld kostet, bevor irgendwelche Fixkosten verteilt sind. Das ist
    etwas anderes als ein Produkt, das seine anteiligen Fixkosten nicht
    trägt, und nur der erste Fall ist ein zwingender Grund, es aus dem
    Programm zu nehmen.
    """
    return [product["name"] for product in products
            if product_margin(product) < 0]


def if_dropped(name, products=PRODUCTS, fixed=TOTAL_FIXED):
    """Rechnet aus, was der Wegfall eines Produktes ändert.

    Die Fixkosten bleiben, denn sie sind fix; wegfällt nur der
    Deckungsbeitrag. Ein Produkt mit positivem Beitrag zu streichen
    verschlechtert den Erfolg um genau diesen Beitrag, auch wenn eine
    Vollkostenrechnung es als Verlustbringer ausweist.

    Raises:
        ValueError: bei einem unbekannten Produkt.
    """
    names = [product["name"] for product in products]
    if name not in names:
        raise ValueError("unbekanntes Produkt")
    kept = [product for product in products if product["name"] != name]
    before = single_stage(products, fixed)["profit"]
    after = single_stage(kept, fixed)["profit"]
    return {"before": before, "after": after, "change": after - before,
            "worth dropping": after > before}


def the_full_cost_trap(products=PRODUCTS, fixed=TOTAL_FIXED):
    """Zeigt, was eine Vollkostenrechnung hier anrichtet.

    Verteilt man die Fixkosten nach der Absatzmenge auf die Produkte, so
    erscheint jedes Produkt mit einem Vollkostenergebnis, und mehrere
    stehen im Minus. Wer sie daraufhin streicht, verliert ihre
    Deckungsbeiträge, die Fixkosten bleiben, und die verbleibenden
    Produkte tragen sie allein: die Rechnung wiederholt sich und heisst
    Todesspirale.

    Returns:
        Abbildung mit den Vollkostenergebnissen und dem Vergleich.
    """
    total = sum(product["quantity"] for product in products)
    share = {product["name"]: fixed * product["quantity"] / total
             for product in products}
    full = {product["name"]: product_margin(product) - share[product["name"]]
            for product in products}
    negative = sorted(name for name, value in full.items() if value < 0)
    kept = [product for product in products if product["name"] not in negative]
    return {"full cost result": full,
            "negative under full costing": negative,
            "profit now": single_stage(products, fixed)["profit"],
            "profit after dropping them":
                single_stage(kept, fixed)["profit"] if kept else -fixed,
            "the name for it": "Todesspirale"}
