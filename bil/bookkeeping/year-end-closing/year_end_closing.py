"""Der Jahresabschluss und die Eröffnung des neuen Jahres."""

STEPS = ("Inventur", "Abschlussbuchungen", "Erfolgskonten über die GuV",
         "GuV über das Eigenkapital",
         "Bestandskonten über das Schlussbilanzkonto",
         "Bilanz aufstellen",
         "Eröffnungsbilanzkonto im neuen Jahr")


def steps():
    """Nennt die Schritte in ihrer Reihenfolge."""
    return list(STEPS)


def close(opening_equity, income, expense, withdrawals=0.0,
          contributions=0.0):
    """Führt das Eigenkapital über das Jahr fort.

    Das Eigenkapital am Ende ist das am Anfang, vermehrt um den Erfolg
    und die Einlagen, vermindert um die Entnahmen. Damit ist der Erfolg
    auch ohne Gewinn- und Verlustrechnung bestimmbar, und die Probe
    lautet: beide Wege müssen dasselbe ergeben.

    Raises:
        ValueError: bei negativen Erträgen, Aufwendungen, Einlagen oder
            Entnahmen.
    """
    for value in (income, expense, withdrawals, contributions):
        if value < 0:
            raise ValueError("negativer Betrag")
    result = income - expense
    closing = opening_equity + result + contributions - withdrawals
    return {"opening equity": opening_equity, "result": result,
            "closing equity": closing,
            "by comparison": closing - opening_equity - contributions
            + withdrawals,
            "agrees": abs((closing - opening_equity - contributions
                           + withdrawals) - result) < 1e-9}


def the_mirror(closing_balances):
    """Prüft, dass das Eröffnungsbilanzkonto das Spiegelbild ist.

    Die Bestände des Schlussbilanzkontos werden im neuen Jahr auf der
    jeweils anderen Seite wieder eröffnet: was im Schlussbilanzkonto im
    Haben stand, steht im Eröffnungsbilanzkonto im Soll. Das ist der
    Grund, warum die Aufgabe im Tutorium von einem Spiegelbild spricht,
    und zugleich die Stelle, an der die Aussage in der Aufgabe verdreht
    ist: das Eröffnungsbilanzkonto spiegelt das Schlussbilanzkonto des
    **vorherigen** Jahres, nicht des folgenden.

    Args:
        closing_balances: Abbildung vom Konto auf Betrag und Seite.

    Returns:
        Abbildung mit der Eröffnung.

    Raises:
        ValueError: bei einer unbekannten Seite.
    """
    opened = {}
    for name, (amount, side) in closing_balances.items():
        if side not in ("Soll", "Haben"):
            raise ValueError("unbekannte Seite: %s" % side)
        opened[name] = (amount, "Haben" if side == "Soll" else "Soll")
    return {"closing": dict(closing_balances), "opening": opened,
            "which year": "das Eröffnungsbilanzkonto spiegelt das "
                          "Schlussbilanzkonto des vorherigen Jahres"}


def inventory_first():
    """Sagt, warum die Inventur am Anfang des Abschlusses steht.

    Die Buchführung führt Sollbestände fort; die Inventur stellt die
    Istbestände fest. Erst der Vergleich zeigt Schwund, Bruch und
    Fehlbuchungen, und erst danach lassen sich die Bestände in die
    Bilanz übernehmen. Wer die Reihenfolge umdreht, schreibt die
    Buchführung in die Bilanz und prüft sie nie.
    """
    return {"Buchführung": "der Sollbestand, fortgeschrieben",
            "Inventur": "der Istbestand, festgestellt",
            "the difference shows": ["Schwund", "Bruch", "Fehlbuchungen"],
            "order matters": "erst feststellen, dann übernehmen"}


def difference(book_value, counted):
    """Bewertet eine Abweichung zwischen Buch- und Istbestand.

    Raises:
        ValueError: bei negativen Beständen.
    """
    if book_value < 0 or counted < 0:
        raise ValueError("negativer Bestand")
    gap = counted - book_value
    return {"book": book_value, "counted": counted, "difference": gap,
            "entry": "Aufwand an Vorräte" if gap < 0
                     else "Vorräte an Ertrag" if gap > 0 else "keine",
            "note": "eine Mehrmenge ist verdächtiger als eine Fehlmenge, "
                    "weil sie meist auf eine vergessene Buchung deutet"}
