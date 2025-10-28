"""Die Merkmale eines (IT-)Projekts."""

CHARACTERISTICS = {
    "defined goal": "klare, ergebnisorientierte und messbare Ziele",
    "unique": "einzigartig, hohe Komplexität und Risiko, relativ neu und "
              "unsicher",
    "time limited": "zeitlich begrenzte Dauer mit Start und Ende",
    "own organisation": "temporäre, interdisziplinäre und "
                        "abteilungsübergreifende Organisation",
    "limited resources": "begrenzte Ressourcen an Personal, Material und "
                         "Budget",
}


def characteristics():
    """Nennt die fünf Merkmale."""
    return dict(CHARACTERISTICS)


def is_a_project(answers):
    """Beurteilt anhand der Merkmale, ob ein Vorhaben ein Projekt ist.

    Das entscheidende Merkmal ist die Einzigartigkeit: was im täglichen
    Betrieb wiederholt abläuft, ist kein Projekt, sondern ein Prozess, und
    gehört in die Linienorganisation. Die anderen vier folgen meist
    daraus.

    Args:
        answers: Abbildung von jedem Merkmal auf ja oder nein.

    Returns:
        Abbildung mit dem Urteil und den fehlenden Merkmalen.

    Raises:
        ValueError: wenn ein Merkmal unbeantwortet bleibt.
    """
    missing_answers = [name for name in CHARACTERISTICS
                       if name not in answers]
    if missing_answers:
        raise ValueError("unbeantwortet: %s" % ", ".join(missing_answers))
    missing = sorted(name for name in CHARACTERISTICS if not answers[name])
    return {"is a project": not missing, "missing": missing,
            "note": "ohne Einzigartigkeit ist es ein Prozess und gehört "
                    "in die Linie"}


def triangle():
    """Nennt die drei Grössen des magischen Dreiecks.

    Zeit, Kosten und Qualität hängen zusammen: wer eine davon festhält,
    verschiebt die anderen. Ein Projekt, dem alle drei fest vorgegeben
    werden, hat keinen Spielraum mehr und verliert ihn dann trotzdem, nur
    unkontrolliert.
    """
    return {"Zeit": "der Termin", "Kosten": "das Budget",
            "Qualität": "der Umfang und die Güte des Ergebnisses"}


def why_it_management_needs_the_portfolio():
    """Sagt, warum ein einzelnes Projekt nicht reicht.

    Unternehmen haben selten ein Projekt, sondern viele, und diese
    konkurrieren um dieselben Ressourcen. Das Portfoliomanagement
    entscheidet nicht, wie ein Projekt läuft, sondern welche überhaupt
    laufen und in welcher Reihenfolge.
    """
    return {"single project": "wie läuft es",
            "portfolio": "welche laufen überhaupt, und in welcher Folge",
            "lifecycle": ["Analysis", "Adaptation", "Communication",
                          "Steering"],
            "competition": "dieselben Menschen und dasselbe Budget"}
