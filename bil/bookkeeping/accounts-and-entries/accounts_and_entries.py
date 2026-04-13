"""Konten, Buchungssätze und die vier Arten der Bilanzveränderung."""

KINDS = {
    "aktiv": {"increases on": "Soll", "decreases on": "Haben",
              "side of the balance sheet": "links"},
    "passiv": {"increases on": "Haben", "decreases on": "Soll",
               "side of the balance sheet": "rechts"},
    "aufwand": {"increases on": "Soll", "decreases on": "Haben",
                "side of the balance sheet": "GuV, mindert das "
                                              "Eigenkapital"},
    "ertrag": {"increases on": "Haben", "decreases on": "Soll",
               "side of the balance sheet": "GuV, mehrt das Eigenkapital"},
}

ACCOUNTS = {
    "Maschinen": "aktiv", "BGA": "aktiv", "Bank": "aktiv",
    "Kasse": "aktiv", "Vorräte": "aktiv", "Forderungen": "aktiv",
    "Eigenkapital": "passiv", "Darlehen": "passiv",
    "Verbindlichkeiten": "passiv",
    "Mietaufwand": "aufwand", "Löhne": "aufwand",
    "Abschreibungen": "aufwand", "Umsatzerlöse": "ertrag",
    "Zinserträge": "ertrag",
}


def kinds():
    """Nennt die Kontenarten und auf welcher Seite sie zunehmen."""
    return {name: dict(row) for name, row in KINDS.items()}


def kind_of(account):
    """Nennt die Art eines Kontos.

    Raises:
        ValueError: bei einem unbekannten Konto.
    """
    if account not in ACCOUNTS:
        raise ValueError("unbekanntes Konto: %s" % account)
    return ACCOUNTS[account]


def entry(debit, credit, amount):
    """Baut einen Buchungssatz «Soll an Haben».

    Die Reihenfolge ist die Regel und keine Konvention: zuerst steht,
    was im Soll gebucht wird, dann das Wörtchen «an», dann das Haben.
    Wer sie umdreht, schreibt eine andere Buchung.

    Args:
        debit: das Konto im Soll.
        credit: das Konto im Haben.
        amount: der Betrag.

    Returns:
        Abbildung mit dem Satz und den Kontenarten.

    Raises:
        ValueError: bei einem unbekannten Konto, einem nicht positiven
            Betrag oder wenn beide Seiten dasselbe Konto nennen.
    """
    if amount <= 0:
        raise ValueError("der Betrag muss positiv sein")
    if debit == credit:
        raise ValueError("Soll und Haben nennen dasselbe Konto")
    return {"debit": debit, "credit": credit, "amount": amount,
            "debit kind": kind_of(debit), "credit kind": kind_of(credit),
            "text": "%s an %s %s" % (debit, credit, amount)}


def change_kind(booking):
    """Benennt die Art der Bilanzveränderung.

    Vier Fälle: ein Aktivtausch verschiebt innerhalb der linken Seite und
    lässt die Summe gleich; ein Passivtausch dasselbe rechts; eine
    Bilanzverlängerung mehrt beide Seiten; eine Bilanzverkürzung mindert
    beide. Wer die Summe im Blick behält, sieht am Satz schon, was
    passiert.

    Returns:
        Die Art, oder ``erfolgswirksam``, wenn ein Erfolgskonto beteiligt
        ist.

    Raises:
        ValueError: bei einem unbekannten Konto.
    """
    left = kind_of(booking["debit"])
    right = kind_of(booking["credit"])
    if left in ("aufwand", "ertrag") or right in ("aufwand", "ertrag"):
        return "erfolgswirksam"
    if left == "aktiv" and right == "aktiv":
        return "Aktivtausch"
    if left == "passiv" and right == "passiv":
        return "Passivtausch"
    if left == "aktiv" and right == "passiv":
        return "Bilanzverlängerung"
    return "Bilanzverkürzung"


def computer_purchase(amount=500.0):
    """Der Buchungssatz aus der Tutoriumsaufgabe.

    Ein Computer für 500 Euro per Banküberweisung: die Ausstattung
    nimmt zu, das Bankguthaben ab, also ``BGA an Bank``. Die umgekehrte
    Richtung wäre der Verkauf, und die Antwort, es müsse nichts gebucht
    werden, verwechselt die gleichbleibende Bilanzsumme mit dem
    Ausbleiben eines Vorgangs.

    Returns:
        Abbildung mit dem Satz und der Art der Veränderung.
    """
    booking = entry("BGA", "Bank", amount)
    booking["change"] = change_kind(booking)
    booking["why not the other way"] = ("Bank an BGA wäre der Verkauf des "
                                        "Computers")
    return booking


def machine_and_furniture(machine=100000.0, furniture=1500.0):
    """Die zweite Tutoriumsaufgabe: zwei Vorgänge, zwei Sätze.

    Die Maschine wird überwiesen, die Möbel bar bezahlt. Es sind zwei
    getrennte Geschäftsvorfälle mit verschiedenen Gegenkonten, und ein
    zusammengesetzter Satz mit einem einzigen Gegenkonto wäre falsch.

    Returns:
        Liste der beiden Sätze.
    """
    return [entry("Maschinen", "Bank", machine),
            entry("BGA", "Kasse", furniture)]


def private_withdrawal(amount=1000.0):
    """Zeigt, was eine Privatentnahme wirklich ist.

    Der Unternehmer nimmt Bargeld heraus: die Kasse sinkt, das
    Eigenkapital sinkt. Beide Seiten der Bilanz werden kleiner, also ist
    es eine Bilanzverkürzung und kein Aktiv-Passiv-Tausch, wie die
    Tutoriumsaufgabe als falsche Antwort anbietet.

    Returns:
        Abbildung mit dem Satz und der Art.
    """
    booking = entry("Eigenkapital", "Kasse", amount)
    booking["change"] = change_kind(booking)
    return booking
