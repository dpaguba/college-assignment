"""Die mehrstufige Deckungsbeitragsrechnung."""

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

AREA_FIXED = {"A": 12000.0, "B": 7000.0}
TOTAL_FIXED = 25000.0


def levels():
    """Nennt die Stufen der Rechnung von unten nach oben."""
    return ["Deckungsbeitrag der Produkte",
            "Deckungsbeitrag der Bereiche",
            "Deckungsbeitrag des Unternehmens",
            "Betriebserfolg"]


def calculate(products=PRODUCTS, area_fixed=None, total_fixed=TOTAL_FIXED):
    """Rechnet den Erfolg über die Stufen.

    Die Fixkosten werden nicht verteilt, sondern dort abgezogen, wo sie
    entstehen: die Bereichsfixkosten beim Bereich, der Rest beim
    Unternehmen. Damit bleibt jede Zahl eine Aussage darüber, was
    wegfiele, wenn die Stufe wegfiele, und genau das macht sie
    entscheidungstauglich.

    Args:
        products: die Produkte.
        area_fixed: die Fixkosten je Bereich.
        total_fixed: die gesamten Fixkosten des Unternehmens.

    Returns:
        Abbildung mit allen Stufen.

    Raises:
        ValueError: wenn die Bereichsfixkosten die gesamten übersteigen.
    """
    area_fixed = AREA_FIXED if area_fixed is None else area_fixed
    if sum(area_fixed.values()) > total_fixed:
        raise ValueError("die Bereichsfixkosten übersteigen die gesamten")
    by_product = {product["name"]: product["quantity"]
                  * (product["price"] - product["variable"])
                  for product in products}
    by_area = {}
    for product in products:
        by_area.setdefault(product["area"], 0.0)
        by_area[product["area"]] += by_product[product["name"]]
    after_area = {area: value - area_fixed.get(area, 0.0)
                  for area, value in by_area.items()}
    company = sum(after_area.values())
    remaining = total_fixed - sum(area_fixed.values())
    return {"products": by_product, "areas before their fixed costs": by_area,
            "areas": after_area, "company": company,
            "company fixed costs": remaining,
            "operating result": company - remaining}


def the_negative_product(products=PRODUCTS):
    """Nennt das Produkt, das die Übung enthält, und was daran hängt.

    Der Handrührer hat einen negativen Deckungsbeitrag: er wird für
    dreissig Euro verkauft und kostet siebenunddreissig an variablen
    Kosten. Jedes verkaufte Stück verliert sieben Euro, bevor irgendeine
    Fixkostenverteilung stattgefunden hat.

    Das ist der eine Fall, in dem die Rechnung eine klare Antwort gibt:
    ohne einen Grund ausserhalb der Zahlen gehört das Produkt aus dem
    Programm. Gründe ausserhalb der Zahlen gibt es, und sie sind genau
    das, was die Rechnung nicht sieht.

    Returns:
        Abbildung mit dem Produkt und der Wirkung seines Wegfalls.
    """
    negative = [product for product in products
                if product["price"] < product["variable"]]
    kept = [product for product in products
            if product["price"] >= product["variable"]]
    return {"negative": [product["name"] for product in negative],
            "loss per unit": {product["name"]:
                              product["price"] - product["variable"]
                              for product in negative},
            "operating result now":
                calculate(products)["operating result"],
            "without it": calculate(kept)["operating result"]}


def when_it_does_not_help():
    """Nennt die Fälle, in denen die Rechnung nicht steuern kann.

    Sie setzt voraus, dass sich der Deckungsbeitrag eines Produktes
    unabhängig von den anderen ändern lässt. Das gilt nicht, wenn
    Produkte einander bedingen (wer den Drucker kauft, kauft die Patrone),
    wenn ein Produkt ein Sortiment vollständig macht, wenn ein Engpass
    die Mengen bindet, oder wenn die Fixkosten sich bei einer Änderung
    doch bewegen. Der letzte Fall ist der häufigste: was auf ein Jahr
    fix ist, ist auf drei Jahre nicht fix.
    """
    return ["Produkte, die einander bedingen",
            "ein Produkt, das das Sortiment vollständig macht",
            "ein Engpass, der die Mengen aneinander bindet",
            "Fixkosten, die auf längere Sicht doch beweglich sind",
            "die letzte ist die häufigste"]


def single_against_multi(products=PRODUCTS):
    """Vergleicht beide Vorgehensweisen.

    Der Betriebserfolg ist derselbe; er muss es sein, denn beide ziehen
    dieselben Fixkosten ab, nur an verschiedenen Stellen. Der Unterschied
    liegt darin, was zwischendrin sichtbar wird: die einstufige Rechnung
    zeigt eine Zahl, die mehrstufige zeigt, dass Bereich B seine eigenen
    Fixkosten nicht deckt.

    Returns:
        Abbildung mit beiden Ergebnissen.
    """
    multi = calculate(products)
    single = sum(multi["products"].values()) - TOTAL_FIXED
    return {"single stage": single,
            "multi stage": multi["operating result"],
            "same": abs(single - multi["operating result"]) < 1e-9,
            "what only the multi stage shows":
                {area: value for area, value in multi["areas"].items()
                 if value < 0}}
