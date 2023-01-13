"""Die Preisuntergrenze, kurzfristig und langfristig."""


def short_run(variable):
    """Die kurzfristige Untergrenze: die variablen Stückkosten.

    Solange der Preis über den variablen Kosten liegt, trägt jedes
    verkaufte Stück etwas zu den Fixkosten bei. Die Fixkosten fallen
    ohnehin an, also ist ein kleiner Beitrag besser als keiner, und ein
    Auftrag unter Vollkosten kann richtig sein.

    Raises:
        ValueError: bei negativen variablen Kosten.
    """
    if variable < 0:
        raise ValueError("negative variable Kosten")
    return variable


def long_run(variable, fixed, quantity):
    """Die langfristige Untergrenze: die Vollkosten je Stück.

    Auf Dauer müssen auch die Fixkosten verdient werden, sonst ist das
    Unternehmen nur langsamer unterwegs in dieselbe Richtung.

    Raises:
        ValueError: bei einer nicht positiven Menge oder negativen
            Kosten.
    """
    if quantity <= 0:
        raise ValueError("die Menge muss positiv sein")
    if variable < 0 or fixed < 0:
        raise ValueError("negative Kosten")
    return variable + fixed / quantity


def additional_order(price, variable, fixed_of_the_order=0.0,
                     quantity=1):
    """Beurteilt einen Zusatzauftrag.

    Gefragt wird nicht, ob der Preis die Vollkosten deckt, sondern ob er
    das deckt, was der Auftrag zusätzlich kostet. Auftragsfixe Kosten
    gehören dazu, allgemeine Fixkosten nicht.

    Returns:
        Abbildung mit dem Beitrag und dem Urteil.

    Raises:
        ValueError: bei einer nicht positiven Menge.
    """
    if quantity <= 0:
        raise ValueError("die Menge muss positiv sein")
    contribution = quantity * (price - variable) - fixed_of_the_order
    return {"contribution": contribution, "accept": contribution > 0,
            "price": price, "short run floor": short_run(variable),
            "note": "allgemeine Fixkosten gehören nicht in diese Rechnung"}


def why_the_short_run_floor_is_dangerous():
    """Nennt, was gegen die kurzfristige Untergrenze spricht.

    Sie ist rechnerisch richtig und praktisch riskant. Ein Preis unter
    Vollkosten setzt einen Referenzpreis beim Kunden, den man nicht mehr
    los wird; er lockt die eigenen Vollzahler in denselben Kanal; und
    was als Ausnahme gedacht war, wird zur Regel, sobald die Kapazität
    daran hängt. Kurzfristig heisst kurzfristig, und die Frage ist, ob
    das durchgehalten wird.
    """
    return ["der niedrige Preis wird zum Referenzpreis",
            "die eigenen Vollzahler wandern in denselben Kanal",
            "die Ausnahme wird zur Regel, wenn die Kapazität daran hängt",
            "kurzfristig heisst kurzfristig, und das muss jemand "
            "durchsetzen"]


def the_full_cost_price(variable, fixed, quantity, markup=0.2):
    """Rechnet einen Preis nach Vollkosten plus Aufschlag.

    Das ist die verbreitetste Preisbildung und die, die den Markt gar
    nicht erwähnt. Ihre Schwäche steckt in der Menge: sie steht im
    Nenner, und sie hängt vom Preis ab, den man gerade erst ausrechnen
    will. Fällt die Menge, steigt der Preis, und dann fällt die Menge
    weiter.

    Raises:
        ValueError: bei einer nicht positiven Menge oder einem
            unzulässigen Aufschlag.
    """
    if markup < 0:
        raise ValueError("negativer Aufschlag")
    return {"full cost": long_run(variable, fixed, quantity),
            "price": long_run(variable, fixed, quantity) * (1 + markup),
            "circularity": "die Menge im Nenner hängt vom Preis ab",
            "what is missing": "die Zahlungsbereitschaft und der "
                               "Wettbewerb"}
