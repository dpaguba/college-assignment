"""Gestaltung der Adressen: Ressourcen statt Aufrufe."""

import re

VERBS = ("get", "post", "create", "delete", "update", "fetch", "list",
         "remove", "add", "edit", "find", "search", "do")


def is_restful(path):
    """Prüft, ob ein Pfad eine Ressource benennt statt einer Handlung.

    Verworfen wird ein Pfad, dessen Bestandteile ein Verb enthalten, und
    einer, dessen Sammlung im Singular steht.

    Raises:
        ValueError: bei einem leeren Pfad.
    """
    if not path:
        raise ValueError("leerer Pfad")
    address = path.split("?", 1)[0]
    parts = [part for part in address.split("/") if part]
    if not parts:
        return False
    for index, part in enumerate(parts):
        lowered = part.lower()
        for verb in VERBS:
            if lowered == verb or lowered.startswith(verb) and \
                    len(lowered) > len(verb) and lowered[len(verb)].isupper():
                return False
        if index % 2 == 0 and not lowered.endswith("s"):
            return False
    return True


def parent(path):
    """Nennt die übergeordnete Ressource eines Pfads.

    Returns:
        Der Pfad ohne die letzten zwei Bestandteile, oder None an der
        Wurzel.
    """
    parts = [part for part in path.split("/") if part]
    if len(parts) <= 2:
        return None
    return "/" + "/".join(parts[:-2])


def rewrite(path):
    """Übersetzt einen aufrufartigen Pfad in Methode und Ressource.

    Returns:
        Abbildung mit ``method`` und ``path``.

    Raises:
        ValueError: wenn kein Verb zu erkennen ist.
    """
    address, _, query = path.partition("?")
    name = address.strip("/")
    match = re.match(r"(get|create|update|delete|list)([A-Z]\w*)", name)
    if not match:
        raise ValueError("kein Aufruf zu erkennen")
    verb, noun = match.groups()
    methods = {"get": "GET", "list": "GET", "create": "POST",
               "update": "PUT", "delete": "DELETE"}
    collection = "/" + noun.lower() + "s"
    identifier = None
    for pair in query.split("&"):
        if pair.startswith("id="):
            identifier = pair[3:]
    return {"method": methods[verb],
            "path": collection + ("/" + identifier if identifier else "")}


def naming_rules():
    """Nennt die Regeln, nach denen Adressen gebildet werden."""
    return ["nouns for resources, verbs come from the method",
            "plural for collections",
            "hierarchy for containment",
            "query string for filtering, sorting and paging",
            "no file extensions, the media type says the format"]
