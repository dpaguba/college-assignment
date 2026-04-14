"""Die Probe der doppelten Buchführung."""

OPENING = {"Maschinen": 100000.0, "Vorräte": 20000.0, "Bank": 50000.0,
           "Kasse": 5000.0, "Eigenkapital": 120000.0,
           "Verbindlichkeiten": 55000.0}

KINDS = {"Maschinen": "aktiv", "Vorräte": "aktiv", "Bank": "aktiv",
         "Kasse": "aktiv", "Forderungen": "aktiv", "BGA": "aktiv",
         "Eigenkapital": "passiv", "Verbindlichkeiten": "passiv",
         "Darlehen": "passiv", "Umsatzerlöse": "ertrag",
         "Mietaufwand": "aufwand", "Abschreibungen": "aufwand"}


def _side(account):
    """Nennt die Bilanzseite eines Kontos.

    Raises:
        ValueError: bei einem unbekannten Konto.
    """
    if account not in KINDS:
        raise ValueError("unbekanntes Konto: %s" % account)
    return KINDS[account]


def apply_entry(balances, debit, credit, amount):
    """Verbucht einen Satz auf den Beständen.

    Ein Aktivkonto wächst im Soll und schrumpft im Haben, ein
    Passivkonto umgekehrt. Erfolgskonten werden hier unmittelbar gegen
    das Eigenkapital gebucht, damit die Gleichung nach jedem Schritt
    stimmt und nicht erst nach dem Abschluss.

    Aufwand und Ertrag brauchen dabei dieselbe Formel, was auf den
    ersten Blick falsch aussieht: der Aufwand mindert das Eigenkapital
    und der Ertrag mehrt es. Die Richtung steckt aber schon in der
    Position, denn ein Aufwand steht im Soll und ein Ertrag im Haben,
    und das Vorzeichen der Position erledigt den Rest.

    Returns:
        Die neuen Bestände.

    Raises:
        ValueError: bei einem unbekannten Konto oder einem nicht
            positiven Betrag.
    """
    if amount <= 0:
        raise ValueError("der Betrag muss positiv sein")
    changed = dict(balances)
    for account, sign in ((debit, 1), (credit, -1)):
        kind = _side(account)
        if kind == "aktiv":
            changed[account] = changed.get(account, 0.0) + sign * amount
        elif kind == "passiv":
            changed[account] = changed.get(account, 0.0) - sign * amount
        else:
            changed["Eigenkapital"] = (changed.get("Eigenkapital", 0.0)
                                       - sign * amount)
    return changed


def totals(balances):
    """Summiert die beiden Bilanzseiten.

    Raises:
        ValueError: bei einem unbekannten Konto.
    """
    assets = sum(value for account, value in balances.items()
                 if _side(account) == "aktiv")
    liabilities = sum(value for account, value in balances.items()
                      if _side(account) == "passiv")
    return {"assets": assets, "equity and liabilities": liabilities,
            "balanced": abs(assets - liabilities) < 1e-9,
            "difference": assets - liabilities}


def run(entries, opening=None):
    """Verbucht eine Folge von Sätzen und prüft nach jedem Schritt.

    Die Gleichung muss nach jedem einzelnen Satz stimmen, nicht erst am
    Ende. Das ist die eigentliche Leistung der doppelten Buchführung:
    ein Fehler fällt an der Stelle auf, an der er gemacht wurde, und
    nicht drei Monate später.

    Args:
        entries: Tripel aus Soll, Haben und Betrag.
        opening: die Anfangsbestände.

    Returns:
        Abbildung mit den Endbeständen und der Prüfung je Schritt.

    Raises:
        ValueError: bei einem unbekannten Konto oder unzulässigem Betrag.
    """
    balances = dict(OPENING if opening is None else opening)
    checks = [totals(balances)["balanced"]]
    for debit, credit, amount in entries:
        balances = apply_entry(balances, debit, credit, amount)
        checks.append(totals(balances)["balanced"])
    return {"balances": balances, "totals": totals(balances),
            "balanced after every step": all(checks),
            "steps": len(entries)}


def example_entries():
    """Eine Folge von Geschäftsvorfällen für die Probe."""
    return [("Vorräte", "Verbindlichkeiten", 8000.0),
            ("Bank", "Umsatzerlöse", 15000.0),
            ("Mietaufwand", "Bank", 2000.0),
            ("Verbindlichkeiten", "Bank", 5000.0),
            ("Abschreibungen", "Maschinen", 10000.0)]


def a_one_sided_entry_breaks_it(opening=None):
    """Zeigt, was eine einseitige Buchung anrichtet.

    Wird nur eine Seite gebucht, so geht die Gleichung um genau den
    Betrag auseinander, und die Differenz nennt die fehlende Buchung.
    Deshalb ist die Summenprobe kein Ritual: sie zeigt nicht nur, dass
    etwas fehlt, sondern auch wie viel.

    Returns:
        Abbildung mit der Differenz.
    """
    balances = dict(OPENING if opening is None else opening)
    balances["Bank"] = balances["Bank"] + 3000.0
    report = totals(balances)
    return {"difference": report["difference"], "balanced": report["balanced"],
            "what it tells you": "die Differenz ist der Betrag der "
                                 "fehlenden Gegenbuchung"}


def why_it_catches_only_some_errors():
    """Nennt die Fehler, die die Probe nicht findet.

    Sie prüft, dass beide Seiten gleich sind, und nicht, dass die
    richtigen Konten getroffen wurden. Eine Buchung auf das falsche
    Konto, ein doppelt erfasster Vorgang, ein ganz vergessener Vorgang
    und zwei Fehler, die einander aufheben, bleiben alle unbemerkt.
    """
    return ["eine Buchung auf das falsche Konto",
            "ein doppelt erfasster Geschäftsvorfall",
            "ein vergessener Geschäftsvorfall",
            "zwei Fehler, die einander gerade aufheben",
            "die Probe prüft die Form, nicht die Zuordnung"]
