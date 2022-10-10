"""Durchlaufzeiteffizienz: wie viel von der Zeit Arbeit ist."""

HOURS_OF_A_DAY = 8


def hours_of_a_day():
    """Die Länge eines Arbeitstages, wie sie die Übung setzt."""
    return HOURS_OF_A_DAY


def efficiency(work, cycle):
    """Der Anteil der Bearbeitungszeit an der Durchlaufzeit.

    Args:
        work: die theoretische Bearbeitungszeit.
        cycle: die Durchlaufzeit, in derselben Einheit.

    Raises:
        ValueError: bei einer nicht positiven Durchlaufzeit oder wenn
            gearbeitet länger als gedauert wird.
    """
    if cycle <= 0:
        raise ValueError("die Durchlaufzeit muss positiv sein")
    if work > cycle:
        raise ValueError("die Bearbeitungszeit übersteigt die Durchlaufzeit")
    return work / cycle


def report(work_hours, cycle_days):
    """Stellt beide Zeiten in Stunden nebeneinander.

    Die Übung gibt die Durchlaufzeiten in Tagen und die Bearbeitungszeiten
    in Stunden an; verglichen werden darf erst nach der Umrechnung.

    Returns:
        Abbildung mit beiden Zeiten, der Wartezeit und der Effizienz.
    """
    cycle_hours = cycle_days * HOURS_OF_A_DAY
    return {"theoretical cycle time": work_hours,
            "cycle time": cycle_hours,
            "waiting": cycle_hours - work_hours,
            "efficiency": efficiency(work_hours, cycle_hours),
            "unit": "hours"}


def expose():
    """Der Exposé-Prozess aus Zettel 4.

    Durchlaufzeit 2 + 4 Tage plus die Schleife aus Fehlersuche und
    Überarbeitung, die im Mittel 1.25 mal läuft; Bearbeitungszeit
    4.5 + 14 Stunden plus 1.25 mal 8 Stunden.
    """
    repetitions = 1.0 / (1.0 - 0.2)
    cycle_days = 2 + 4 + repetitions * (1 + 1)
    work_hours = 4.5 + 14 + repetitions * (2 + 6)
    return report(work_hours, cycle_days)


def loan_application():
    """Der Darlehensantrag mit Schleife aus Übungsaufgabe 2.

    Die Zahlen stammen aus derselben Rechnung wie in der
    Durchlaufzeitanalyse: 8.65 Tage Durchlaufzeit gegen 8.9 Stunden
    Arbeit.
    """
    repetitions = 1.0 / (1.0 - 0.2)
    cycle_days = repetitions * 1 + max(1, 3) + 3 + (0.6 * 1 + 0.4 * 2)
    work_hours = (repetitions * 2 + max(0.5, 3) + 2
                  + (0.6 * 2 + 0.4 * 0.5))
    return report(work_hours, cycle_days)


def what_the_number_says():
    """Sagt, was eine niedrige Effizienz bedeutet.

    Ein Wert von einem Achtel heisst, dass ein Fall sieben Achtel seiner
    Zeit liegt und wartet. Verbesserung setzt dann nicht bei der Arbeit
    an, sondern bei den Übergaben: eine Aktivität um die Hälfte zu
    beschleunigen bringt hier ein Sechzehntel der Durchlaufzeit.
    """
    return {"low value means": "the case mostly waits",
            "where to look": "handovers, batching, queues before resources",
            "what does not help much": "making the work itself faster",
            "typical values": "in administrative processes often under 0.2"}
