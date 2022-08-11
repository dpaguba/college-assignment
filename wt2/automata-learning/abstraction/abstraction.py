"""Abstraktion: von der Anwendung zum Alphabet, mit dem gelernt wird."""

LOGIN_ALPHABET = ("l", "o", "v")

ACTIONS = {
    ("/login", "POST"): "l",
    ("/logout", "POST"): "o",
    ("/profile", "GET"): "v",
    ("/settings", "GET"): "v",
    ("/orders", "GET"): "v",
}


def login_language(word):
    """Beschreibt die Sprache eines kleinen Anmeldeverfahrens.

    Ein Wort gehört dazu, wenn jede Ansicht nach einer Anmeldung und vor
    der nächsten Abmeldung angefordert wird. Eine Anmeldung im
    angemeldeten Zustand und eine Abmeldung im abgemeldeten sind Fehler,
    aus denen es kein Zurück gibt.

    Args:
        word: Folge aus ``l``, ``o`` und ``v``.

    Returns:
        Wahr, wenn die Folge zulässig ist.
    """
    logged_in = False
    for letter in word:
        if letter == "l":
            if logged_in:
                return False
            logged_in = True
        elif letter == "o":
            if not logged_in:
                return False
            logged_in = False
        elif letter == "v":
            if not logged_in:
                return False
        else:
            return False
    return True


def mapper():
    """Liefert die Zuordnung von Aufrufen auf Buchstaben."""
    return dict(ACTIONS)


def abstract(mapping, action):
    """Bildet einen Aufruf auf einen Buchstaben ab.

    Args:
        mapping: die Zuordnung.
        action: Abbildung mit ``path`` und ``method``.

    Returns:
        Der Buchstabe.

    Raises:
        KeyError: wenn der Aufruf nicht zugeordnet ist.
    """
    key = (action["path"], action["method"])
    if key not in mapping:
        raise KeyError("nicht zugeordnet: %s" % (key,))
    return mapping[key]


def alphabet_reduction():
    """Misst, wie stark die Abstraktion das Alphabet verkleinert.

    Returns:
        Abbildung mit der Zahl der Aufrufe und der Buchstaben.
    """
    mapping = mapper()
    return {"concrete": len(mapping), "abstract": len(set(mapping.values())),
            "letters": sorted(set(mapping.values()))}


def too_coarse():
    """Zeigt, was eine zu grobe Abstraktion anrichtet.

    Werden Anmeldung und Abmeldung auf denselben Buchstaben abgebildet, so
    führt dieselbe Folge einmal in den einen und einmal in den anderen
    Zustand: das abstrahierte System verhält sich nicht mehr
    deterministisch, und kein Automat kann es beschreiben.

    Returns:
        Abbildung mit dem Befund und dem widersprüchlichen Wort.
    """
    coarse = {("/login", "POST"): "x", ("/logout", "POST"): "x"}
    first = login_language("l")
    second = login_language("o")
    return {"deterministic": first == second, "word": "x",
            "concrete meanings": sorted(set(coarse.values())),
            "reason": "two actions with different effects share a letter"}


def parameter_abstraction():
    """Beschreibt, wie Werte in den Aufrufen behandelt werden.

    Ein Bezeichner in der Adresse macht aus einer Handlung unendlich viele
    Buchstaben. Üblich ist, ihn auf wenige Klassen abzubilden: der eigene,
    ein fremder, ein nicht vorhandener.
    """
    return {"problem": "an identifier in the path yields infinitely many "
                       "letters",
            "answer": "map it to a few classes",
            "classes": ["own", "other", "missing"]}


def what_is_learned():
    """Hält fest, wovon das gelernte Modell ein Modell ist.

    Gelernt wird nicht die Anwendung, sondern ihr Bild unter der
    Abstraktion. Was die Abstraktion zusammenwirft, kann das Modell nicht
    unterscheiden, und was sie unterschlägt, taucht darin nicht auf.
    """
    return {"model of": "the abstracted system",
            "not a model of": "the application itself",
            "consequence": "a wrong mapper produces a model that is "
                           "consistent and useless"}
