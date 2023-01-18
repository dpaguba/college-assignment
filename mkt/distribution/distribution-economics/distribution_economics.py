"""Die Rechnung hinter der Wahl des Absatzweges."""


def margin_chain(producer_price, steps):
    """Rechnet den Endpreis über die Handelsspannen aus.

    Jede Stufe schlägt ihre Spanne auf den Preis auf, den sie zahlt. Die
    Aufschläge wirken deshalb multiplikativ und nicht additiv: zwei
    Stufen mit je dreissig Prozent ergeben nicht sechzig, sondern
    neunundsechzig.

    Args:
        producer_price: der Abgabepreis des Herstellers.
        steps: die Spannen der Stufen als Anteile.

    Returns:
        Abbildung mit dem Endpreis und den Preisen je Stufe.

    Raises:
        ValueError: bei einem negativen Preis oder einer Spanne
            ausserhalb von null bis unter eins.
    """
    if producer_price < 0:
        raise ValueError("negativer Preis")
    price = producer_price
    prices = [price]
    for share in steps:
        if not 0 <= share < 1:
            raise ValueError("Spanne ausserhalb von 0 bis unter 1")
        price = price / (1 - share)
        prices.append(price)
    additive = producer_price * (1 + sum(steps))
    return {"prices": prices, "final": price,
            "if the margins were added": additive,
            "difference": price - additive,
            "why": "jede Stufe schlägt auf den Preis auf, den sie zahlt"}


def what_the_producer_keeps(final_price, steps):
    """Rechnet zurück, was beim Hersteller ankommt.

    Raises:
        ValueError: bei einem negativen Preis oder einer unzulässigen
            Spanne.
    """
    if final_price < 0:
        raise ValueError("negativer Preis")
    price = final_price
    for share in reversed(list(steps)):
        if not 0 <= share < 1:
            raise ValueError("Spanne ausserhalb von 0 bis unter 1")
        price = price * (1 - share)
    return {"producer price": price, "share of the final price":
            price / final_price if final_price else 0.0,
            "steps": list(steps)}


def break_even_volume(own_cost, margin_per_unit, retail_share):
    """Die Menge, ab der sich der eigene Vertrieb rechnet.

    Der eigene Vertrieb kostet fest und spart je Stück die Handelsspanne.
    Die Schwelle ist deshalb die feste Ausgabe geteilt durch die
    Ersparnis je Stück, und sie liegt in der Regel höher, als der
    Bauchentscheid vermutet.

    Raises:
        ValueError: bei einer Spanne von null oder negativen Werten.
    """
    if own_cost < 0 or margin_per_unit <= 0:
        raise ValueError("unzulässige Werte")
    if not 0 < retail_share < 1:
        raise ValueError("die Spanne liegt zwischen null und eins")
    return own_cost / (margin_per_unit * retail_share)


def compare(volume, own_cost, margin_per_unit, retail_share):
    """Vergleicht beide Wege bei einer Menge.

    Raises:
        ValueError: bei einer negativen Menge oder unzulässigen Werten.
    """
    if volume < 0:
        raise ValueError("negative Menge")
    threshold = break_even_volume(own_cost, margin_per_unit, retail_share)
    direct = volume * margin_per_unit - own_cost
    indirect = volume * margin_per_unit * (1 - retail_share)
    return {"direct": direct, "indirect": indirect,
            "threshold": threshold,
            "better": "direkt" if volume > threshold else "über den Handel",
            "consistent": (direct > indirect) == (volume > threshold)}


def the_reach_is_not_free():
    """Nennt, was die Rechnung unterschlägt.

    Sie vergleicht dieselbe Menge auf beiden Wegen, und das ist genau
    die Annahme, die nicht gilt. Der Handel bringt Reichweite; ohne ihn
    fällt die Menge, oft um mehr, als die gesparte Spanne wert ist. Die
    Frage lautet deshalb nicht, ob der eigene Vertrieb günstiger ist,
    sondern bei welcher Menge er es wäre und ob diese Menge ohne den
    Handel erreichbar bleibt.
    """
    return {"the calculation assumes": "dieselbe Menge auf beiden Wegen",
            "reality": "der Handel bringt Reichweite",
            "the right question": "welche Menge bleibt ohne ihn",
            "second cost": "der Aufbau der eigenen Reichweite dauert und "
                           "kostet, bevor er wirkt"}
