"""Die Granularität eines Modells für die Ausführung."""

RULES = ("zu abstrakt: eine Aktivität braucht mehr als eine Ressource",
         "zu detailliert: aufeinander folgende Aktivitäten hängen an "
         "derselben Ressource")


def rules():
    """Nennt die beiden Faustformeln."""
    return list(RULES)


def assess(activities):
    """Prüft ein Modell auf die richtige Schnitthöhe.

    Eine Aktivität, an der mehr als eine Ressource arbeitet, ist zu grob:
    sie verbirgt eine Übergabe, und eine Übergabe ist genau die Stelle,
    an der ein Fall liegen bleibt. Zwei aufeinander folgende Aktivitäten
    derselben Ressource sind zu fein: zwischen ihnen passiert nichts, was
    das System wissen müsste.

    Args:
        activities: Liste von Abbildungen mit ``name`` und ``resources``,
            in der Reihenfolge des Ablaufs.

    Returns:
        Abbildung mit den Aktivitäten zum Zerlegen und den Paaren zum
        Zusammenfassen.

    Raises:
        ValueError: bei einer Aktivität ohne Ressource.
    """
    for activity in activities:
        if not activity.get("resources"):
            raise ValueError("Aktivität ohne Ressource: %s"
                             % activity.get("name"))
    decompose = [activity["name"] for activity in activities
                 if len(set(activity["resources"])) > 1]
    aggregate = []
    for first, second in zip(activities, activities[1:]):
        if (len(set(first["resources"])) == 1
                and set(first["resources"]) == set(second["resources"])):
            aggregate.append((first["name"], second["name"]))
    return {"decompose": decompose, "aggregate": aggregate,
            "activities": len(activities)}


def why_it_matters():
    """Sagt, was die falsche Schnitthöhe kostet.

    Zu grob heisst: das System sieht die Übergabe nicht und kann sie
    weder messen noch beschleunigen. Zu fein heisst: der Mensch quittiert
    fünf Schritte, wo einer genügt, und die Kennzahlen ertrinken in
    Ereignissen, die niemand braucht.
    """
    return {"too coarse": "the handover is invisible and unmeasurable",
            "too fine": "the user confirms five steps instead of one",
            "the right cut": "one activity, one resource, one sitting"}


def one_sitting():
    """Nennt die dritte, praktische Probe.

    Neben den beiden Faustformeln hilft die Frage, ob die Aktivität in
    einem Zug erledigt wird. Was zwischendurch unterbrochen und später
    fortgesetzt wird, sind in Wahrheit zwei Aktivitäten mit einer
    Wartezeit dazwischen.
    """
    return {"question": "is it done in one sitting",
            "if not": "there are two activities and a wait between them",
            "sign": "the case is put aside and picked up again"}
