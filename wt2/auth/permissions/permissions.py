"""Berechtigungen in der Schreibweise von Apache Shiro."""


def parse(permission):
    """Zerlegt eine Berechtigung in ihre Teile.

    Ein Teil ist durch Doppelpunkte abgetrennt und kann mehrere Werte
    durch Kommas enthalten; ein Stern steht für alle Werte.

    Returns:
        Liste von Mengen, je Ebene eine.

    Raises:
        ValueError: bei einer leeren Angabe.
    """
    if not permission or not permission.strip():
        raise ValueError("leere Berechtigung")
    parts = []
    for level in permission.split(":"):
        values = {value.strip() for value in level.split(",") if value.strip()}
        if not values:
            raise ValueError("leere Ebene in der Berechtigung")
        parts.append(values)
    return parts


def implies(held, wanted):
    """Sagt, ob eine gehaltene Berechtigung eine verlangte abdeckt.

    Eine fehlende Ebene auf der gehaltenen Seite gilt als Stern: wer
    ``printer:print`` hat, darf auf jedem Drucker drucken. Auf der
    verlangten Seite gilt eine fehlende Ebene dagegen nicht als
    unbestimmt, weshalb ``printer:print:lp7`` nicht ``printer:print``
    abdeckt.

    Raises:
        ValueError: bei einer leeren Angabe.
    """
    left = parse(held)
    right = parse(wanted)
    if len(left) > len(right):
        return False
    for index, needed in enumerate(right):
        if index >= len(left):
            return True
        granted = left[index]
        if "*" in granted:
            continue
        if not needed <= granted:
            return False
    return True


def permitted(held, wanted):
    """Prüft, ob eine der gehaltenen Berechtigungen die verlangte abdeckt."""
    return any(implies(entry, wanted) for entry in held)


def levels():
    """Nennt die übliche Bedeutung der drei Ebenen."""
    return {"first": "the resource kind", "second": "the action",
            "third": "the instance"}


def examples():
    """Stellt die Beispiele der Vorlesung zusammen.

    Returns:
        Liste von Tripeln (gehalten, verlangt, Antwort).
    """
    cases = [("printer:print:lp7", "printer:print:lp7", True),
             ("printer:print", "printer:print:lp7", True),
             ("printer:*", "printer:print:lp7", True),
             ("printer:*:lp7", "printer:print:lp7", True),
             ("printer:print:lp7", "printer:print", False),
             ("printer:query", "printer:print", False),
             ("printer:print,query", "printer:query:lp7", True),
             ("*", "printer:print:lp7", True)]
    return [(held, wanted, implies(held, wanted)) for held, wanted, _ in cases]


def why_not_only_roles():
    """Erklärt, warum Berechtigungen neben den Rollen stehen.

    Eine Prüfung auf eine Rolle bindet den Code an die Organisation: wird
    eine Rolle geteilt oder umbenannt, muss der Code geändert werden. Eine
    Prüfung auf eine Berechtigung fragt danach, was getan werden soll, und
    bleibt gültig, wenn sich die Rollen ändern.
    """
    return {"check a role": "couples the code to the organisation",
            "check a permission": "asks what is to be done",
            "roles hold permissions": True}
