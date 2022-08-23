"""Fliessbänder der fortlaufenden Integration."""


def example_stages(fail_at=None):
    """Baut ein Fliessband aus fünf Stufen.

    Args:
        fail_at: Name der Stufe, die scheitern soll.

    Returns:
        Liste der Stufen mit Namen, Dauer und Ergebnis.
    """
    stages = [("lint", 5), ("build", 60), ("test", 300), ("package", 40),
              ("deploy", 20)]
    return [{"name": name, "duration": duration,
             "succeeds": name != fail_at} for name, duration in stages]


def run(stages):
    """Führt die Stufen der Reihe nach aus und hält beim ersten Fehler an.

    Returns:
        Abbildung mit den ausgeführten Stufen, der Gesamtdauer und dem
        Ergebnis.

    Raises:
        ValueError: bei einem leeren Fliessband.
    """
    if not stages:
        raise ValueError("leeres Fliessband")
    executed = []
    total = 0
    for stage in stages:
        executed.append(stage)
        total += stage["duration"]
        if not stage["succeeds"]:
            return {"executed": executed, "duration": total,
                    "succeeded": False, "failed at": stage["name"]}
    return {"executed": executed, "duration": total, "succeeded": True,
            "failed at": None}


def ordering_report():
    """Misst, was es kostet, die schnelle Prüfung ans Ende zu stellen.

    Scheitert die kurze Prüfung, so ist es billiger, sie zuerst laufen zu
    lassen: die lange Prüfung wird dann gar nicht erst gestartet.

    Returns:
        Abbildung mit der Dauer bis zum Fehlschlag in beiden Anordnungen.
    """
    fast = {"name": "lint", "duration": 5, "succeeds": False}
    slow = {"name": "test", "duration": 300, "succeeds": True}
    return {"fast first": run([fast, slow])["duration"],
            "slow first": run([slow, fast])["duration"]}


def parallel_report():
    """Vergleicht die Dauer bei Reihenfolge und bei Gleichzeitigkeit.

    Stufen, die einander nicht brauchen, können nebeneinander laufen; die
    Dauer ist dann die der längsten statt der Summe.

    Returns:
        Abbildung mit beiden Dauern.
    """
    independent = [{"name": "unit tests", "duration": 120, "succeeds": True},
                   {"name": "static analysis", "duration": 90,
                    "succeeds": True},
                   {"name": "licence check", "duration": 30,
                    "succeeds": True}]
    return {"sequential": sum(stage["duration"] for stage in independent),
            "parallel": max(stage["duration"] for stage in independent),
            "stages": len(independent)}


def continuous_practices():
    """Unterscheidet die drei Begriffe, die oft vermengt werden.

    Fortlaufende Integration heisst, dass jede Änderung gebaut und geprüft
    wird. Fortlaufende Auslieferung heisst, dass jede geprüfte Änderung
    ausgeliefert werden könnte; die Freigabe bleibt eine Entscheidung.
    Fortlaufende Bereitstellung heisst, dass sie es ohne Entscheidung
    wird.
    """
    return {"continuous integration": {"builds every change": True,
                                       "automatic release": False},
            "continuous delivery": {"builds every change": True,
                                    "ready to release": True,
                                    "automatic release": False},
            "continuous deployment": {"builds every change": True,
                                      "ready to release": True,
                                      "automatic release": True}}


def what_a_pipeline_needs():
    """Nennt, was ein Fliessband voraussetzt."""
    return ["everything in version control, the configuration included",
            "a build that runs the same way on every machine",
            "tests that either pass or say why not",
            "a fast first stage, so a mistake is cheap",
            "the same artefact through every stage"]
