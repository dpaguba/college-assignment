"""Die einheitliche Theorie der Annahme von Technik."""

CONSTRUCTS = {
    "Leistungserwartung": "der Nutzen, den der Benutzer erwartet",
    "Aufwandserwartung": "wie leicht die Benutzung ihm fällt",
    "sozialer Einfluss": "was andere, die ihm wichtig sind, erwarten",
    "erleichternde Bedingungen": "ob die nötige Unterstützung da ist",
}

MODERATORS = ("Geschlecht", "Alter", "Erfahrung", "Freiwilligkeit")

WEIGHTS = {"Leistungserwartung": 0.4, "Aufwandserwartung": 0.2,
           "sozialer Einfluss": 0.2, "erleichternde Bedingungen": 0.2}


def constructs():
    """Nennt die vier Bestimmungsgrössen."""
    return dict(CONSTRUCTS)


def moderators():
    """Nennt die vier Grössen, die die Wirkung der anderen verändern."""
    return list(MODERATORS)


def intention(scores, weights=None):
    """Rechnet die Absicht zur Nutzung aus den vier Grössen.

    Das Modell von Venkatesh sagt: die ersten drei Grössen bestimmen die
    Absicht, die vierte bestimmt das Verhalten unmittelbar. Hier wird
    vereinfacht gewichtet summiert; das Gewicht der Leistungserwartung
    ist doppelt so hoch, weil sie in der Arbeit der stärkste Prädiktor
    ist.

    Args:
        scores: Abbildung von der Grösse auf einen Wert zwischen eins
            und sieben.
        weights: eigene Gewichte.

    Returns:
        Abbildung mit der Absicht und den Beiträgen.

    Raises:
        ValueError: bei einer fehlenden Grösse oder einem Wert
            ausserhalb der Skala.
    """
    weights = WEIGHTS if weights is None else weights
    for name in CONSTRUCTS:
        if name not in scores:
            raise ValueError("es fehlt: %s" % name)
        if not 1 <= scores[name] <= 7:
            raise ValueError("Wert ausserhalb der Skala von 1 bis 7")
    contributions = {name: weights[name] * scores[name]
                     for name in CONSTRUCTS}
    return {"intention": sum(contributions.values()),
            "contributions": contributions,
            "strongest": max(contributions,
                             key=lambda name: contributions[name])}


def facilitating_conditions_act_directly():
    """Nennt die Besonderheit der vierten Grösse.

    Die erleichternden Bedingungen wirken nicht über die Absicht,
    sondern unmittelbar auf das Verhalten. Der Unterschied ist
    praktisch: wer will und nicht kann, hat eine hohe Absicht und nutzt
    trotzdem nicht. Eine Umfrage, die nur die Absicht misst, sieht das
    Problem nicht.
    """
    return {"acts on": "das Verhalten unmittelbar",
            "not on": "die Absicht",
            "consequence": "hohe Absicht und keine Nutzung ist kein "
                           "Widerspruch",
            "what to do": "nach den Bedingungen fragen, nicht nur nach "
                          "der Absicht"}


def where_the_effort_matters(experience):
    """Sagt, wann die Aufwandserwartung noch zählt.

    Die Arbeit findet, dass ihr Einfluss mit der Erfahrung verschwindet:
    was man kann, fällt einem leicht, und dann sagt die Frage nach der
    Leichtigkeit nichts mehr über die Nutzung. Für eine Einführung
    heisst das, dass die Bedienbarkeit am Anfang entscheidet und später
    nicht mehr, und dass eine Messung nach einem Jahr das falsche
    Ergebnis liefert.

    Raises:
        ValueError: bei einer negativen Erfahrung.
    """
    if experience < 0:
        raise ValueError("negative Erfahrung")
    return {"months of experience": experience,
            "effort still matters": experience < 6,
            "why": "was man kann, fällt einem leicht",
            "consequence for a study": "früh messen, sonst misst man "
                                       "die Gewöhnung"}


def what_the_model_does_not_say():
    """Nennt die Grenze des Modells.

    Es erklärt Absicht und Nutzung; es sagt nichts darüber, ob die
    Nutzung dem Unternehmen nützt. Ein System kann angenommen werden und
    schaden, und eines kann abgelehnt werden und richtig sein. Die
    Annahme ist eine Beschreibung des Verhaltens, kein Gütemass.
    """
    return {"explains": "Absicht und Nutzung",
            "does not explain": "ob die Nutzung nützt",
            "misuse": "die Annahme als Erfolgsmass nehmen",
            "variance explained in the paper": "rund 70 Prozent der "
                                               "Absicht"}
