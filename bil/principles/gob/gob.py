"""Die Grundsätze ordnungsmäßiger Buchführung."""

PRINCIPLES = {
    "Richtigkeit und Willkürfreiheit": "die Buchung entspricht dem "
                                       "Vorgang und ist nicht gewählt",
    "Klarheit und Übersichtlichkeit": "die Aufzeichnungen sind lesbar "
                                      "und geordnet",
    "Vollständigkeit": "kein Geschäftsvorfall fehlt",
    "Einzelbewertung": "jeder Gegenstand wird für sich bewertet",
    "Vorsicht": "im Zweifel die ungünstigere Annahme",
    "Stetigkeit": "die Methoden bleiben von Jahr zu Jahr gleich",
    "Periodenabgrenzung": "Aufwand und Ertrag gehören in ihre Periode",
    "Going Concern": "das Unternehmen wird fortgeführt, solange nichts "
                     "dagegen spricht",
}


def principles():
    """Nennt die Grundsätze."""
    return dict(PRINCIPLES)


def purpose():
    """Nennt das Ziel, das die Grundsätze verfolgen.

    Nach § 238 HGB muss die Buchführung so beschaffen sein, dass sie
    einem sachverständigen Dritten in angemessener Zeit einen Überblick
    über die Geschäftsvorfälle und die Lage des Unternehmens vermitteln
    kann. Das ist der Massstab: nicht Gewinnmaximierung, nicht
    Steuerersparnis, sondern Nachvollziehbarkeit für jemanden, der nicht
    dabei war.
    """
    return {"goal": "Nachvollziehbarkeit und Prüfbarkeit für einen "
                    "sachverständigen Dritten",
            "not": ["Gewinnmaximierung", "Steueroptimierung",
                    "interne Steuerung"],
            "source": "§ 238 HGB",
            "time": "in angemessener Zeit"}


def check(entries):
    """Prüft eine Buchung gegen einige Grundsätze.

    Args:
        entries: Abbildung mit ``documented``, ``complete``, ``timely``
            und ``method_changed``.

    Returns:
        Abbildung mit den verletzten Grundsätzen.

    Raises:
        ValueError: bei einer fehlenden Angabe.
    """
    required = ("documented", "complete", "timely", "method_changed")
    missing = [name for name in required if name not in entries]
    if missing:
        raise ValueError("es fehlen: %s" % ", ".join(missing))
    broken = []
    if not entries["documented"]:
        broken.append("Richtigkeit und Willkürfreiheit")
    if not entries["complete"]:
        broken.append("Vollständigkeit")
    if not entries["timely"]:
        broken.append("Periodenabgrenzung")
    if entries["method_changed"]:
        broken.append("Stetigkeit")
    return {"broken": broken, "in order": not broken}


def no_entry_without_a_document():
    """Nennt den Satz, der die Buchführung prüfbar macht.

    Keine Buchung ohne Beleg. Der Beleg ist das, woran ein Dritter die
    Buchung nachvollziehen kann; ohne ihn ist die Buchung eine Behauptung
    des Buchhalters. Deshalb ist der Satz keine Formalie, sondern die
    Bedingung dafür, dass eine Prüfung überhaupt möglich ist.
    """
    return {"rule": "keine Buchung ohne Beleg",
            "why": "ohne Beleg ist die Buchung eine Behauptung",
            "consequence": "die Aufbewahrungsfrist gilt dem Beleg, nicht "
                           "nur dem Buch",
            "how long": "zehn Jahre für Bücher und Belege"}


def consistency_and_why_it_is_binding():
    """Erklärt, warum die Stetigkeit die schärfste der Regeln ist.

    Fast jede Bewertung lässt einen Spielraum, und ein einzelner
    Jahresabschluss ist deshalb kaum widerlegbar. Vergleichbar wird er
    erst über die Zeit, und das funktioniert nur, wenn die Methode
    dieselbe bleibt. Ein Methodenwechsel ist zulässig und muss im Anhang
    stehen, samt seiner Wirkung; ohne diese Angabe ist der Vergleich
    zweier Jahre wertlos, und der Leser merkt es nicht.
    """
    return {"why it binds": "ein einzelner Abschluss ist kaum "
                            "widerlegbar, erst der Vergleich trägt",
            "a change is allowed": True,
            "but": "sie muss im Anhang stehen, samt ihrer Wirkung",
            "without that": "der Vergleich zweier Jahre ist wertlos und "
                            "sieht trotzdem gültig aus"}
