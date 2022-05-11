"""Die Lagerverwaltung aus Aufgabe 2 des vierten Übungsblattes."""

import random

START = 3
WORKERS = 3


def _store(state, message):
    """Das Verhalten des Lagers.

    Es hält den Bestand und beantwortet zwei Nachrichten. Beim Einlagern
    steigt der Bestand, beim Auslagern sinkt er, sofern etwas da ist;
    ist das Lager leer, geht eine Fehlernachricht zurück. Der Bestand
    kann deshalb nie negativ werden, und zwar ohne Sperre: das Lager
    bearbeitet immer nur eine Nachricht.
    """
    kind, sender = message
    if kind == "put":
        return state + 1, [(sender, ("ok", "put"))]
    if state > 0:
        return state - 1, [(sender, ("ok", "take"))]
    return state, [(sender, ("error", "leer"))]


def run(seed=0, start=START, workers=WORKERS, limit=200):
    """Spielt das System durch.

    Drei Lageristen entscheiden sich zufällig für Einlagern oder
    Auslagern und schicken ihre Anfrage an das Lager. Nach einer
    erfolgreichen Aktion entscheiden sie erneut; auf eine
    Fehlernachricht hin hören sie auf.

    Args:
        seed: Startwert des Zufallsgenerators.
        start: der Anfangsbestand.
        workers: die Zahl der Lageristen.
        limit: obere Schranke der Nachrichten.

    Returns:
        Abbildung mit dem Verlauf, dem Endbestand und den Lageristen,
        die aufgehört haben.

    Raises:
        ValueError: bei einem negativen Anfangsbestand oder einer nicht
            positiven Zahl von Lageristen.
    """
    if start < 0:
        raise ValueError("negativer Anfangsbestand")
    if workers < 1:
        raise ValueError("mindestens ein Lagerist")
    generator = random.Random(seed)
    state = start
    active = {index: True for index in range(workers)}
    queue = [("store", (generator.choice(["put", "take"]), index))
             for index in active]
    history = [state]
    handled = 0
    lowest = state
    while queue and handled < limit:
        target, message = queue.pop(0)
        handled += 1
        if target == "store":
            state, replies = _store(state, message)
            history.append(state)
            lowest = min(lowest, state)
            queue.extend(replies)
            continue
        kind = message[0]
        if kind == "error":
            active[target] = False
            continue
        if active[target]:
            queue.append(("store",
                          (generator.choice(["put", "take"]), target)))
    return {"final": state, "lowest": lowest, "history": history,
            "messages": handled,
            "stopped": sorted(index for index, alive in active.items()
                              if not alive),
            "still active": sorted(index for index, alive in active.items()
                                   if alive),
            "never negative": lowest >= 0}


def invariant_holds(seeds=range(40)):
    """Prüft über viele Läufe, dass der Bestand nie negativ wird.

    Das ist die Zusicherung, die die Aufgabe verlangt, und sie hängt an
    einer einzigen Eigenschaft des Modells: das Lager bearbeitet eine
    Nachricht zur Zeit. Zwei Lageristen können nicht gleichzeitig das
    letzte Stück nehmen, weil ihre Anfragen nacheinander bearbeitet
    werden.

    Returns:
        Abbildung mit dem Befund und dem tiefsten je erreichten Stand.
    """
    lowest = None
    for seed in seeds:
        report = run(seed=seed)
        lowest = report["lowest"] if lowest is None else min(
            lowest, report["lowest"])
    return {"runs": len(list(seeds)), "lowest ever": lowest,
            "never negative": lowest >= 0,
            "why": "das Lager bearbeitet eine Nachricht zur Zeit"}


def what_would_break_it():
    """Nennt, was passieren müsste, damit die Zusicherung fällt.

    Ein Lagerist müsste den Bestand selbst lesen und danach entscheiden.
    Zwischen dem Lesen und dem Entnehmen könnte ein anderer zugreifen,
    und beide nähmen das letzte Stück. Das Modell verhindert das nicht
    von sich aus: es verhindert nur, dass zwei Nachrichten gleichzeitig
    bearbeitet werden. Wer die Entscheidung aus dem Lager herausnimmt,
    hat wieder genau das Problem, das er vermeiden wollte.
    """
    return {"breaks when": "die Entscheidung ausserhalb des Lagers fällt",
            "pattern": "erst den Bestand abfragen, dann entnehmen",
            "why": "zwischen Frage und Entnahme liegt eine Lücke",
            "rule": "die Entscheidung gehört dorthin, wo der Zustand "
                    "liegt"}


def message_count(seeds=range(10)):
    """Zählt, wie lange das System läuft, bis alle aufgehört haben.

    Der Ausgang hängt an den Zufallsentscheidungen: solange mehr
    eingelagert als entnommen wird, hört niemand auf. Deshalb erreichen
    manche Läufe die Schranke, ohne dass alle Lageristen gestoppt haben,
    und das ist kein Fehler, sondern das Verhalten des Systems.

    Returns:
        Abbildung vom Startwert auf die Zahl der Nachrichten und die
        Zahl der noch aktiven Lageristen.
    """
    return {seed: {"messages": run(seed=seed)["messages"],
                   "still active": len(run(seed=seed)["still active"])}
            for seed in seeds}
