"""Das Niederstwertprinzip und sein Gegenstück auf der Passivseite."""


def strict_lower(cost, market):
    """Das strenge Niederstwertprinzip für das Umlaufvermögen.

    Angesetzt wird der niedrigere von Anschaffungskosten und Marktwert,
    und zwar bei jeder Minderung, gleich ob sie dauerhaft ist. Das
    Umlaufvermögen wird bald wieder zu Geld, deshalb zählt der Wert
    heute.

    Raises:
        ValueError: bei negativen Werten.
    """
    if cost < 0 or market < 0:
        raise ValueError("negative Werte")
    return {"value": min(cost, market), "cost": cost, "market": market,
            "write down": max(0.0, cost - market),
            "rule": "streng: jede Minderung wirkt"}


def moderate_lower(cost, market, permanent):
    """Das gemilderte Niederstwertprinzip für das Anlagevermögen.

    Abgeschrieben wird nur bei einer dauerhaften Minderung; eine
    vorübergehende bleibt aussen vor. Das Anlagevermögen dient dem
    Betrieb auf Dauer, also ist der Tageswert weniger aussagekräftig als
    beim Umlaufvermögen.

    Raises:
        ValueError: bei negativen Werten.
    """
    if cost < 0 or market < 0:
        raise ValueError("negative Werte")
    value = min(cost, market) if permanent else cost
    return {"value": value, "cost": cost, "market": market,
            "permanent": bool(permanent),
            "write down": max(0.0, cost - value),
            "rule": "gemildert: nur bei dauerhafter Minderung"}


def highest_value(amount, market):
    """Das Höchstwertprinzip für Verbindlichkeiten.

    Auf der Passivseite kehrt sich die Vorsicht um: angesetzt wird der
    höhere Wert. Eine Fremdwährungsschuld, die teurer geworden ist, wird
    aufgewertet; eine, die billiger geworden ist, nicht. Beides folgt
    derselben Regel, nämlich sich nicht reicher zu rechnen.

    Raises:
        ValueError: bei negativen Werten.
    """
    if amount < 0 or market < 0:
        raise ValueError("negative Werte")
    return {"value": max(amount, market), "booked": amount,
            "market": market,
            "increase": max(0.0, market - amount),
            "rule": "Höchstwert: die Schuld wird nicht kleingerechnet"}


def asymmetry():
    """Zeigt, dass Gewinne und Verluste ungleich behandelt werden.

    Ein nicht realisierter Verlust wird gebucht, ein nicht realisierter
    Gewinn nicht. Das ist das Imparitätsprinzip, und es ist keine
    Nachlässigkeit, sondern Absicht: das Handelsrecht schützt den
    Gläubiger, und dafür wird das Vermögen lieber zu klein als zu gross
    gezeigt.

    Die Kehrseite steht selten dabei: stille Reserven entstehen
    systematisch, das ausgewiesene Eigenkapital ist zu niedrig, und
    jede Kennzahl darauf ist verzerrt, und zwar in eine bekannte
    Richtung.

    Returns:
        Abbildung mit beiden Fällen.
    """
    loss = strict_lower(100.0, 70.0)
    gain = strict_lower(100.0, 130.0)
    return {"unrealised loss booked": loss["write down"],
            "unrealised gain booked": max(0.0, gain["value"] - 100.0),
            "principle": "Imparitätsprinzip",
            "purpose": "Gläubigerschutz",
            "side effect": "stille Reserven und ein zu niedriges "
                           "Eigenkapital"}


def hidden_reserve(cost, market):
    """Misst die stille Reserve eines Postens.

    Raises:
        ValueError: bei negativen Werten.
    """
    if cost < 0 or market < 0:
        raise ValueError("negative Werte")
    booked = min(cost, market)
    return {"booked": booked, "market": market,
            "hidden reserve": max(0.0, market - booked),
            "visible in the balance sheet": False}


def write_up(previous_value, cost, recovered):
    """Behandelt die Wertaufholung nach einer Abschreibung.

    Fällt der Grund für eine Abschreibung weg, so muss zugeschrieben
    werden, aber höchstens bis zu den Anschaffungskosten. Die
    Anschaffungskosten sind die Obergrenze jeder Bewertung, und daran
    ändert auch ein gestiegener Marktwert nichts.

    Raises:
        ValueError: bei negativen Werten.
    """
    if previous_value < 0 or cost < 0 or recovered < 0:
        raise ValueError("negative Werte")
    value = min(cost, max(previous_value, recovered))
    return {"value": value, "capped at cost": value == cost
            and recovered > cost,
            "write up": value - previous_value,
            "rule": "die Anschaffungskosten sind die Obergrenze"}
