"""Modelle der Zugriffskontrolle: Listen, Rollen und Merkmale."""


def access_list(entries):
    """Baut ein Modell aus einer Zugriffsliste je Objekt.

    Args:
        entries: Abbildung von Objekt auf Benutzer auf erlaubte Aktionen.
    """
    return {"kind": "access list", "entries": entries}


def role_based(roles, assignment):
    """Baut ein Modell aus Rollen und ihrer Zuordnung.

    Args:
        roles: Abbildung von Rolle auf erlaubte Aktionen.
        assignment: Abbildung von Benutzer auf seine Rollen.
    """
    return {"kind": "role based", "roles": roles, "assignment": assignment}


def attribute_based(rule):
    """Baut ein Modell, das je Anfrage eine Regel auswertet."""
    return {"kind": "attribute based", "rule": rule}


def allowed(model, user, target, action, context=None):
    """Entscheidet eine Anfrage im gegebenen Modell.

    Raises:
        ValueError: bei einem unbekannten Modell.
    """
    kind = model["kind"]
    if kind == "access list":
        return action in model["entries"].get(target, {}).get(user, [])
    if kind == "role based":
        for role in model["assignment"].get(user, []):
            if action in model["roles"].get(role, []):
                return True
        return False
    if kind == "attribute based":
        request = dict(context or {})
        request.update({"user": user, "target": target, "action": action})
        return bool(model["rule"](request))
    raise ValueError("unbekanntes Modell")


def entry_count(users, objects, roles):
    """Zählt die Einträge, die jedes Modell zu pflegen hat.

    Eine Zugriffsliste braucht im schlimmsten Fall einen Eintrag je
    Benutzer und Objekt. Ein Rollenmodell braucht einen je Benutzer und
    Rolle sowie einen je Rolle und Objekt.

    Raises:
        ValueError: bei negativen Zahlen.
    """
    if min(users, objects, roles) < 0:
        raise ValueError("negative Anzahl")
    return {"access list": users * objects,
            "role based": users + roles * objects,
            "users": users, "objects": objects, "roles": roles}


def role_explosion(users=50):
    """Zeigt den Fall, in dem das Rollenmodell nichts spart.

    Braucht jeder Benutzer eine eigene Zusammenstellung von Rechten, so
    entsteht eine Rolle je Benutzer, und die Zahl der Rollen übersteigt
    die der Benutzer, sobald noch gemeinsame Rollen dazukommen.

    Returns:
        Abbildung mit der Zahl der Benutzer und der nötigen Rollen.
    """
    individual = users
    shared = 3
    return {"users": users, "roles needed": individual + shared,
            "reason": "every user needs an individual set of rights"}


def comparison():
    """Stellt die drei Modelle gegenüber."""
    return {"access list": "explicit, exact, grows with users times objects",
            "role based": "compact, needs the roles to fit the organisation",
            "attribute based": "decides at request time, hardest to audit"}
