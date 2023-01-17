"""Die Wahl des Absatzweges."""

CHANNELS = {
    "direkt": {"steps": 0, "control": "hoch", "reach": "gering",
               "margin kept": 1.0},
    "einstufig": {"steps": 1, "control": "mittel", "reach": "mittel",
                  "margin kept": 0.7},
    "zweistufig": {"steps": 2, "control": "gering", "reach": "hoch",
                   "margin kept": 0.5},
}

FUNCTIONS = ("Überbrückung von Raum", "Überbrückung von Zeit",
             "Sortimentsbildung", "Mengenanpassung", "Beratung",
             "Kreditgewährung", "Werbung am Verkaufsort")


def channels():
    """Nennt die Absatzwege nach der Zahl der Handelsstufen."""
    return dict(CHANNELS)


def functions():
    """Nennt die Funktionen, die der Handel übernimmt.

    Sie sind der Grund, warum es ihn gibt. Wer direkt vertreibt,
    übernimmt sie alle selbst, und die Frage ist nicht, ob sie anfallen,
    sondern wer sie günstiger erbringt.
    """
    return list(FUNCTIONS)


def contacts(producers, customers, middlemen=0):
    """Zählt die nötigen Kontakte mit und ohne Handel.

    Ohne Handel muss jeder Hersteller jeden Kunden erreichen, das sind
    n·m Kontakte. Mit einem Händler dazwischen sind es n + m. Das ist
    das älteste Argument für den Handel und rechnet sich schon bei
    kleinen Zahlen.

    Raises:
        ValueError: bei negativen Zahlen.
    """
    if producers < 0 or customers < 0 or middlemen < 0:
        raise ValueError("negative Zahl")
    direct = producers * customers
    through = (producers + customers) * middlemen if middlemen else direct
    return {"direct": direct, "through middlemen": through,
            "saved": direct - through,
            "worthwhile": through < direct}


def intensity():
    """Nennt die drei Grade der Vertriebsintensität.

    Intensiv heisst überall, selektiv nach Kriterien, exklusiv einer je
    Gebiet. Die Wahl hängt am Produkt: Kaugummi will überall sein, eine
    Uhr will nicht überall sein, und ein Auto braucht eine Werkstatt.
    """
    return {"intensiv": "so viele Absatzstellen wie möglich",
            "selektiv": "nur Händler, die Kriterien erfüllen",
            "exklusiv": "einer je Gebiet, oft mit Gebietsschutz",
            "decided by": "das Produkt und die Kaufgewohnheit"}


def conflict():
    """Nennt den Konflikt, der in jedem mehrstufigen Weg steckt.

    Der Hersteller will Absatz und Markenbild, der Händler will Marge und
    Frequenz, und beide wollen die Kundenbeziehung. Sobald der Hersteller
    daneben direkt verkauft, wird aus dem Partner ein Wettbewerber, und
    das ist der Konflikt, den jeder Onlineshop eines Markenherstellers
    auslöst.
    """
    return {"manufacturer wants": ["Absatz", "Markenbild",
                                   "die Kundenbeziehung"],
            "retailer wants": ["Marge", "Frequenz",
                               "die Kundenbeziehung"],
            "trigger": "der eigene Onlineshop des Herstellers",
            "name": "Kanalkonflikt"}


def choose(margin_per_unit, own_cost, retail_share, volume_direct,
           volume_indirect):
    """Vergleicht den eigenen Vertrieb mit dem über den Handel.

    Der eigene Weg behält die ganze Marge und trägt die eigenen Kosten;
    der Handel nimmt einen Anteil und bringt Menge. Die Rechnung
    entscheidet sich fast immer an der Menge, nicht an der Marge.

    Raises:
        ValueError: bei einem Anteil ausserhalb von null bis eins oder
            negativen Mengen.
    """
    if not 0 <= retail_share <= 1:
        raise ValueError("Anteil ausserhalb von 0 bis 1")
    if volume_direct < 0 or volume_indirect < 0:
        raise ValueError("negative Menge")
    direct = volume_direct * margin_per_unit - own_cost
    indirect = volume_indirect * margin_per_unit * (1 - retail_share)
    return {"direct": direct, "indirect": indirect,
            "better": "direkt" if direct > indirect else "über den Handel",
            "break even volume": (own_cost / (margin_per_unit
                                              * retail_share)
                                  if retail_share else float("inf"))}
