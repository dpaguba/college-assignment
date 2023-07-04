"""Wiederanlauf nach einem Fehler: Protokoll, Undo, Redo, Sicherungspunkt."""


def example_log():
    """Liefert ein Protokoll mit einer beendeten und einer offenen Transaktion.

    Returns:
        Liste von Einträgen mit den Schlüsseln ``kind`` und
        ``transaction``; Änderungseinträge tragen zusätzlich ``before``
        und ``after``.
    """
    return [
        {"kind": "begin", "transaction": "t1"},
        {"kind": "update", "transaction": "t1", "item": "a",
         "before": 10, "after": 20},
        {"kind": "begin", "transaction": "t2"},
        {"kind": "update", "transaction": "t2", "item": "b",
         "before": 5, "after": 7},
        {"kind": "commit", "transaction": "t1"},
    ]


def recover(log):
    """Bestimmt, welche Transaktionen zurückgesetzt und welche wiederholt werden.

    Der Wiederanlauf liest das Protokoll einmal vorwärts, um die
    beendeten Transaktionen zu sammeln, und entscheidet danach für jede
    Transaktion mit Änderungen.

    Returns:
        Abbildung mit den Listen ``redone`` und ``undone``.
    """
    committed = set()
    started = []
    for entry in log:
        if entry["kind"] == "commit":
            committed.add(entry["transaction"])
        elif entry["kind"] == "update":
            if entry["transaction"] not in started:
                started.append(entry["transaction"])
    return {"redone": [name for name in started if name in committed],
            "undone": [name for name in started if name not in committed]}


def apply_recovery(log, state):
    """Bringt einen Zustand nach dem Wiederanlauf in Ordnung.

    Args:
        log: Protokoll wie von :func:`example_log`.
        state: Abbildung von Datum auf den Wert auf der Platte.

    Returns:
        Der wiederhergestellte Zustand.
    """
    plan = recover(log)
    result = dict(state)
    for entry in log:
        if entry["kind"] != "update":
            continue
        if entry["transaction"] in plan["redone"]:
            result[entry["item"]] = entry["after"]
    for entry in reversed(log):
        if entry["kind"] != "update":
            continue
        if entry["transaction"] in plan["undone"]:
            result[entry["item"]] = entry["before"]
    return result


def wal_rule_holds(events):
    """Prüft die Regel des Vorausschreibens des Protokolls.

    Args:
        events: Folge von Tripeln (``log`` oder ``write``, Transaktion,
            Datum).

    Returns:
        Falsch, sobald eine Seite geschrieben wird, bevor ihr
        Protokolleintrag steht.
    """
    logged = set()
    for kind, transaction, item in events:
        if kind == "log":
            logged.add((transaction, item))
        elif kind == "write":
            if (transaction, item) not in logged:
                return False
        else:
            raise ValueError("unbekanntes Ereignis")
    return True


def checkpoint_effect(log_length, checkpoint_at):
    """Vergleicht die Länge des zu lesenden Protokolls mit und ohne Sicherungspunkt.

    Raises:
        ValueError: wenn der Sicherungspunkt außerhalb des Protokolls liegt.
    """
    if not 0 <= checkpoint_at <= log_length:
        raise ValueError("Sicherungspunkt liegt ausserhalb")
    return {"without": log_length,
            "with checkpoint": log_length - checkpoint_at}


def failure_kinds():
    """Nennt die drei Fehlerarten und ihre Behandlung."""
    return {"transaction failure": "undo",
            "system failure": "undo and redo from the log",
            "media failure": "restore a backup and redo"}
