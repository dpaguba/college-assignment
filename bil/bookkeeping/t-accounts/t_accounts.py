"""Das T-Konto und der Weg von den Buchungen zum Abschluss."""


def account(name, opening=0.0, side="aktiv"):
    """Legt ein T-Konto an.

    Raises:
        ValueError: bei einer unbekannten Seite.
    """
    if side not in ("aktiv", "passiv", "aufwand", "ertrag"):
        raise ValueError("unbekannte Kontenart")
    return {"name": name, "side": side, "debit": [], "credit": [],
            "opening": opening}


def post(built, amount, to="debit"):
    """Bucht einen Betrag auf eine Seite des Kontos.

    Raises:
        ValueError: bei einer unbekannten Seite oder einem nicht
            positiven Betrag.
    """
    if to not in ("debit", "credit"):
        raise ValueError("die Seite ist Soll oder Haben")
    if amount <= 0:
        raise ValueError("der Betrag muss positiv sein")
    built[to].append(amount)
    return built


def balance(built):
    """Rechnet den Saldo eines Kontos aus.

    Das Anfangsbestandsvorzeichen hängt von der Kontenart ab: bei einem
    Aktivkonto und bei einem Aufwand steht der Anfangsbestand im Soll,
    bei einem Passivkonto und einem Ertrag im Haben. Der Saldo wird auf
    der schwächeren Seite eingetragen, damit beide Seiten gleich sind;
    dieser Eintrag heisst Saldo und geht in den Abschluss.
    """
    opening_debit = built["opening"] if built["side"] in ("aktiv",
                                                          "aufwand") else 0.0
    opening_credit = built["opening"] if built["side"] in ("passiv",
                                                           "ertrag") else 0.0
    debit = opening_debit + sum(built["debit"])
    credit = opening_credit + sum(built["credit"])
    return {"debit total": debit, "credit total": credit,
            "balance": debit - credit,
            "closes on": "Haben" if debit > credit else "Soll",
            "amount": abs(debit - credit)}


def close_to(built, target="Schlussbilanzkonto"):
    """Schliesst ein Konto ab und nennt das Gegenkonto.

    Bestandskonten gehen in das Schlussbilanzkonto, Erfolgskonten in die
    Gewinn- und Verlustrechnung. Das ist der ganze Unterschied zwischen
    den beiden Kontengruppen, und er entscheidet, ob ein Betrag in der
    Bilanz stehen bleibt oder in den Erfolg wandert.
    """
    report = balance(built)
    goes_to = ("Gewinn- und Verlustrechnung"
               if built["side"] in ("aufwand", "ertrag")
               else target)
    return {"account": built["name"], "amount": report["amount"],
            "entered on": report["closes on"], "goes to": goes_to}


def example():
    """Ein Bankkonto mit Anfangsbestand und vier Bewegungen.

    Returns:
        Das Konto.
    """
    built = account("Bank", 50000.0, "aktiv")
    post(built, 15000.0, "debit")
    post(built, 2000.0, "credit")
    post(built, 5000.0, "credit")
    post(built, 100000.0, "credit")
    return built


def why_the_balance_goes_on_the_weaker_side():
    """Erklärt den Eintrag, der Anfängern regelmässig falsch herum gerät.

    Ein T-Konto wird abgeschlossen, indem beide Seiten gleich gemacht
    werden. Der fehlende Betrag steht deshalb auf der Seite, die kleiner
    ist, und heisst dort Saldo. Er ist keine Buchung im üblichen Sinn,
    sondern eine Rechenhilfe, und deshalb steht er auf der Seite, auf
    der der Bestand gerade nicht ist.
    """
    return {"rule": "der Saldo steht auf der kleineren Seite",
            "why": "beide Seiten werden gleich gemacht",
            "an asset account": "hat Bestand im Soll, der Saldo steht im "
                                "Haben",
            "confusion": "der Saldo im Haben heisst nicht, dass das Konto "
                         "ein Passivkonto wäre"}
