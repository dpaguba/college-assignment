"""Der digitale Zwilling und seine Archetypen."""

LEVELS = {
    "digital model": {"data flows": "keine automatische Verbindung",
                      "changes in the real thing": "manuell übertragen",
                      "changes in the model": "manuell übertragen"},
    "digital shadow": {"data flows": "vom Ding zum Modell, automatisch",
                       "changes in the real thing": "erscheinen im Modell",
                       "changes in the model": "manuell übertragen"},
    "digital twin": {"data flows": "in beide Richtungen, automatisch",
                     "changes in the real thing": "erscheinen im Modell",
                     "changes in the model": "wirken auf das Ding"},
}


def levels():
    """Nennt die drei Stufen in aufsteigender Reihenfolge."""
    return ["digital model", "digital shadow", "digital twin"]


def describe(level):
    """Beschreibt eine Stufe.

    Raises:
        ValueError: bei einer unbekannten Stufe.
    """
    if level not in LEVELS:
        raise ValueError("unbekannte Stufe")
    return dict(LEVELS[level])


def classify(from_thing, to_thing):
    """Ordnet eine Anlage anhand der Datenflüsse ein.

    Die Einteilung hängt an genau zwei Fragen: fliessen Daten vom Ding
    zum Modell, und fliessen sie zurück. Alles andere, was in
    Prospekten unter dem Wort steht, ändert daran nichts.

    Args:
        from_thing: ob Daten vom Ding zum Modell fliessen.
        to_thing: ob Änderungen am Modell auf das Ding wirken.

    Returns:
        Abbildung mit der Stufe.
    """
    if from_thing and to_thing:
        level = "digital twin"
    elif from_thing:
        level = "digital shadow"
    else:
        level = "digital model"
    return {"level": level, "from the thing": bool(from_thing),
            "to the thing": bool(to_thing),
            "note": "die meisten Anlagen, die Zwilling heissen, sind "
                    "Schatten"}


def purposes():
    """Nennt, wofür ein Zwilling gebaut wird.

    Beobachten, was gerade geschieht; vorhersagen, was geschehen wird;
    ausprobieren, was geschähe; und steuern. Nur der letzte Zweck
    braucht den Rückkanal, und deshalb ist er der einzige, für den die
    volle Stufe nötig ist.
    """
    return {"monitor": "digital shadow genügt",
            "predict": "digital shadow genügt",
            "simulate": "digital shadow genügt",
            "control": "hier braucht es den Rückkanal",
            "consequence": "für drei von vier Zwecken reicht die "
                           "mittlere Stufe"}


def what_it_needs():
    """Nennt, was ein Zwilling braucht, damit er trägt.

    Sensoren, die genug messen; ein Modell, das die Wirklichkeit trifft;
    eine Verbindung, die schnell genug ist für den Zweck; und ein
    Verfahren, das Abweichungen zwischen Ding und Modell erkennt und
    nicht wegmittelt. Der letzte Punkt ist der, der in Vorführungen
    fehlt, und er ist derselbe, um den es in der Anomalieerkennung geht.
    """
    return ["Sensoren mit ausreichender Abdeckung",
            "ein Modell, das die Wirklichkeit trifft",
            "eine Verbindung, deren Verzögerung zum Zweck passt",
            "ein Verfahren, das Abweichung erkennt statt sie zu glätten"]


def the_latency_question(purpose):
    """Sagt, wie schnell die Verbindung für einen Zweck sein muss.

    Raises:
        ValueError: bei einem unbekannten Zweck.
    """
    needed = {"monitor": "Minuten bis Stunden",
              "predict": "Stunden bis Tage",
              "simulate": "keine, das Modell läuft für sich",
              "control": "Millisekunden bis Sekunden"}
    if purpose not in needed:
        raise ValueError("unbekannter Zweck")
    return {"purpose": purpose, "latency": needed[purpose],
            "why it matters": "die Verzögerung entscheidet über die "
                              "Technik und über die Kosten, nicht das "
                              "Wort Zwilling"}
