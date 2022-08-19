"""Wege, eine neue Fassung in Betrieb zu nehmen."""

STRATEGIES = ("recreate", "blue green", "rolling", "canary")


def simulate(strategy, instances, step=1):
    """Rechnet eine Umstellung durch.

    Args:
        strategy: eine der bekannten Vorgehensweisen.
        instances: Zahl der laufenden Einheiten.
        step: wie viele Einheiten je Schritt getauscht werden.

    Returns:
        Abbildung mit der Ausfallzeit in Schritten, dem grössten Bedarf an
        Einheiten und dem Anteil der Benutzer auf der neuen Fassung zu
        Beginn.

    Raises:
        ValueError: bei einer unbekannten Vorgehensweise oder zu wenigen
            Einheiten.
    """
    if strategy not in STRATEGIES:
        raise ValueError("unbekannte Vorgehensweise")
    if instances < 1:
        raise ValueError("mindestens eine Einheit")
    if strategy == "recreate":
        return {"downtime": 1, "peak instances": instances,
                "users on the new version at first": 1.0,
                "steps": 2}
    if strategy == "blue green":
        return {"downtime": 0, "peak instances": 2 * instances,
                "users on the new version at first": 1.0,
                "steps": 2}
    if strategy == "rolling":
        return {"downtime": 0, "peak instances": instances + step,
                "users on the new version at first": step / instances,
                "steps": instances // step + 1}
    return {"downtime": 0, "peak instances": instances + 1,
            "users on the new version at first": 1.0 / (instances + 1),
            "steps": instances + 1}


def rollback_cost():
    """Schätzt, wie teuer die Rücknahme jeder Vorgehensweise ist.

    Bei der Umschaltung zwischen zwei Umgebungen steht die alte noch und
    die Rücknahme ist ein Schalter. Beim schrittweisen Tausch muss jede
    getauschte Einheit einzeln zurückgesetzt werden.

    Returns:
        Abbildung mit der Zahl der Schritte je Vorgehensweise.
    """
    return {"blue green": 1, "canary": 1, "rolling": 4, "recreate": 2}


def choose(constraints):
    """Empfiehlt eine Vorgehensweise anhand der Randbedingungen.

    Args:
        constraints: Abbildung mit ``downtime allowed``,
            ``spare capacity`` und ``wants gradual exposure``.

    Returns:
        Der Name der passenden Vorgehensweise.
    """
    if constraints.get("wants gradual exposure"):
        return "canary"
    if constraints.get("spare capacity", 0) >= 1.0:
        return "blue green"
    if constraints.get("downtime allowed"):
        return "recreate"
    return "rolling"


def what_they_share():
    """Nennt, was jede der Vorgehensweisen voraussetzt."""
    return ["the new version must run beside the old one",
            "the database schema has to fit both for a while",
            "a health check that says whether an instance is ready",
            "a way back that is practised, not only planned"]
