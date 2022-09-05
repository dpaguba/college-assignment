"""Die HTTP-Methoden, ihre Sicherheit und ihre Idempotenz."""

SAFE = {"GET", "HEAD", "OPTIONS", "TRACE"}
IDEMPOTENT = SAFE | {"PUT", "DELETE"}
KNOWN = IDEMPOTENT | {"POST", "PATCH"}


def is_safe(method):
    """Sagt, ob eine Methode den Zustand des Servers unverändert lässt.

    Raises:
        ValueError: bei einer unbekannten Methode.
    """
    if method not in KNOWN:
        raise ValueError("unbekannte Methode")
    return method in SAFE


def is_idempotent(method):
    """Sagt, ob mehrfaches Ausführen denselben Zustand ergibt wie einmaliges.

    Raises:
        ValueError: bei einer unbekannten Methode.
    """
    if method not in KNOWN:
        raise ValueError("unbekannte Methode")
    return method in IDEMPOTENT


def apply(state, method, path, body=None):
    """Wendet eine Anfrage auf ein einfaches Zustandsmodell an.

    Args:
        state: Abbildung von Pfad auf Inhalt.
        method: die HTTP-Methode.
        path: die Zielressource; bei POST die Sammlung.
        body: der Inhalt.

    Returns:
        Der neue Zustand.

    Raises:
        ValueError: bei einer unbekannten Methode.
    """
    result = dict(state)
    if method in SAFE:
        return result
    if method == "PUT":
        result[path] = body
    elif method == "DELETE":
        result.pop(path, None)
    elif method == "POST":
        number = 1
        while "%s/%d" % (path, number) in result:
            number += 1
        result["%s/%d" % (path, number)] = body
    elif method == "PATCH":
        current = dict(result.get(path) or {})
        for name, value in (body or {}).items():
            if isinstance(value, dict) and "increase by" in value:
                current[name] = current.get(name, 0) + value["increase by"]
            else:
                current[name] = value
        result[path] = current
    else:
        raise ValueError("unbekannte Methode")
    return result


def idempotence_holds():
    """Prüft die Behauptung am Zustandsmodell.

    Für jede Methode ausser der Teiländerung wird die Anfrage einmal und
    zweimal ausgeführt und verglichen; die Antwort muss mit der Tabelle
    übereinstimmen. Die Teiländerung bleibt aussen vor, weil ihr Verhalten
    vom Inhalt abhängt und nicht von der Methode.
    """
    for method in KNOWN - {"PATCH"}:
        state = {"/books/1": {"title": "a"}}
        once = apply(state, method, "/books/1", {"title": "b"})
        twice = apply(once, method, "/books/1", {"title": "b"})
        if (once == twice) != is_idempotent(method):
            return False
    return True


def patch_depends_on_the_body():
    """Misst beide Arten der Teiländerung am Zustandsmodell.

    Eine absolute Teiländerung setzt einen Wert und ist damit
    wiederholbar; eine relative erhöht ihn und ist es nicht. Die
    Spezifikation verlangt von der Methode keine Idempotenz, gerade weil
    beides erlaubt ist.

    Returns:
        Abbildung mit dem Ergebnis nach einer und nach zwei Anfragen für
        beide Arten.
    """
    state = {"/books/1": {"title": "a", "views": 5}}
    absolute_once = apply(state, "PATCH", "/books/1", {"title": "b"})
    absolute_twice = apply(absolute_once, "PATCH", "/books/1",
                           {"title": "b"})
    relative_once = apply(state, "PATCH", "/books/1",
                          {"views": {"increase by": 1}})
    relative_twice = apply(relative_once, "PATCH", "/books/1",
                           {"views": {"increase by": 1}})
    return {"absolute is idempotent": absolute_once == absolute_twice,
            "relative is idempotent": relative_once == relative_twice,
            "views after one": relative_once["/books/1"]["views"],
            "views after two": relative_twice["/books/1"]["views"]}


def repeated_post():
    """Zählt die Ressourcen nach einer und nach zwei gleichen Anfragen.

    Returns:
        Abbildung mit beiden Zählungen.
    """
    state = {}
    once = apply(state, "POST", "/books", {"title": "a"})
    twice = apply(once, "POST", "/books", {"title": "a"})
    return {"after one": len(once), "after two": len(twice)}


def repeated_put():
    """Dasselbe für eine Methode, die eine benannte Ressource setzt."""
    state = {}
    once = apply(state, "PUT", "/books/1", {"title": "a"})
    twice = apply(once, "PUT", "/books/1", {"title": "a"})
    return {"after one": len(once), "after two": len(twice)}


def safe_implies_idempotent():
    """Prüft, dass jede sichere Methode auch idempotent ist.

    Die Umkehrung gilt nicht: eine Löschung ändert den Zustand und ist
    trotzdem wiederholbar.
    """
    return all(is_idempotent(method) for method in SAFE) \
        and not is_safe("DELETE") and is_idempotent("DELETE")


def patch_is_not_idempotent_in_general():
    """Erklärt, warum eine Teiländerung nicht als idempotent gilt.

    Eine Teiländerung darf relativ formuliert sein, etwa als Erhöhung
    eines Zählers; zweimal angewandt ergibt sie dann etwas anderes als
    einmal.
    """
    return {"absolute patch": "idempotent in practice",
            "relative patch": "not idempotent",
            "specification": "not required to be idempotent"}
