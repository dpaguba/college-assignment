"""Zweiphasen-Sperrprotokoll und die Verträglichkeit von Sperren."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "serialisability"))

import serialisability

COMPATIBILITY = {
    ("shared", "shared"): True,
    ("shared", "exclusive"): False,
    ("exclusive", "shared"): False,
    ("exclusive", "exclusive"): False,
}


def is_two_phase(operations):
    """Prüft, ob jede Transaktion eine Wachstums- und eine Schrumpfphase hat.

    Args:
        operations: Folge von Tripeln (Transaktion, ``lock`` oder
            ``unlock``, Datum).

    Returns:
        Falsch, sobald eine Transaktion nach einer Freigabe erneut sperrt.
    """
    shrinking = set()
    for transaction, action, _ in operations:
        if action == "unlock":
            shrinking.add(transaction)
        elif action == "lock":
            if transaction in shrinking:
                return False
        else:
            raise ValueError("unbekannte Sperroperation")
    return True


def compatible(held, requested):
    """Sagt, ob eine angeforderte Sperre neben einer gehaltenen bestehen kann.

    Raises:
        ValueError: bei einer unbekannten Sperrart.
    """
    key = (held, requested)
    if key not in COMPATIBILITY:
        raise ValueError("unbekannte Sperrart")
    return COMPATIBILITY[key]


def schedules_under_locking(transactions):
    """Zählt alle Schedules auf, die ein Sperrverwalter erzeugen kann.

    Simuliert wird strenges Zweiphasen-Sperren: vor jeder Operation
    verlangt die Transaktion die passende Sperre und gibt alle Sperren
    erst nach ihrer letzten Operation frei. Eine Operation kommt nur
    dran, wenn keine unverträgliche Sperre einer anderen laufenden
    Transaktion auf dem Datum liegt.

    Args:
        transactions: Abbildung von Transaktionsnamen auf ihre Folge von
            Operationen als Paare (``r`` oder ``w``, Datum).

    Returns:
        Liste der möglichen Schedules, jeder als Liste von Tripeln
        (Transaktion, Operation, Datum).
    """
    names = list(transactions)
    found = []

    def search(position, locks, prefix):
        """Setzt den Schedule fort, solange eine Operation eine Sperre bekommt."""
        if all(position[name] == len(transactions[name]) for name in names):
            found.append(list(prefix))
            return
        for name in names:
            index = position[name]
            if index == len(transactions[name]):
                continue
            operation, item = transactions[name][index]
            wanted = "shared" if operation == "r" else "exclusive"
            blocked = any(holder != name and not compatible(kind, wanted)
                          for holder, kind in locks.get(item, []))
            if blocked:
                continue
            held = list(locks.get(item, []))
            if (name, wanted) not in held:
                held.append((name, wanted))
            following = dict(locks)
            following[item] = held
            moved = dict(position)
            moved[name] = index + 1
            if moved[name] == len(transactions[name]):
                following = {key: [entry for entry in value
                                   if entry[0] != name]
                             for key, value in following.items()}
            prefix.append((name, operation, item))
            search(moved, following, prefix)
            prefix.pop()

    search({name: 0 for name in names}, {}, [])
    return found


def guarantees_serialisability():
    """Prüft die Garantie des Protokolls an allen erzeugbaren Schedules.

    Zwei Transaktionen greifen über Kreuz auf zwei Daten zu, was ohne
    Sperren zu einem Zyklus im Konfliktgraphen führen kann. Geprüft wird,
    dass kein Schedule des Sperrverwalters diesen Zyklus enthält.
    """
    transactions = {"t1": [("r", "a"), ("w", "b")],
                    "t2": [("r", "b"), ("w", "a")]}
    schedules = schedules_under_locking(transactions)
    if not schedules:
        return False
    return all(serialisability.is_conflict_serialisable(schedule)
               for schedule in schedules)


def interleaving_is_possible():
    """Zeigt, dass das Protokoll nicht jede Verschränkung verbietet.

    Arbeiten zwei Transaktionen auf verschiedenen Daten, sperren sie
    einander nicht; der Sperrverwalter lässt dann auch Schedules zu, die
    keine serielle Reihenfolge sind.

    Returns:
        Abbildung mit der Zahl aller Schedules und der Zahl der nicht
        seriellen darunter.
    """
    transactions = {"t1": [("r", "a"), ("w", "a")],
                    "t2": [("r", "b"), ("w", "b")]}
    schedules = schedules_under_locking(transactions)
    interleaved = [schedule for schedule in schedules
                   if not _is_serial(schedule)]
    return {"schedules": len(schedules), "interleaved": len(interleaved)}


def _is_serial(schedule):
    """Sagt, ob ein Schedule die Transaktionen nacheinander ausführt."""
    order = []
    for transaction, _, _ in schedule:
        if not order or order[-1] != transaction:
            order.append(transaction)
    return len(order) == len(set(order))


def prevents_cascade(variant):
    """Sagt, ob eine Protokollvariante kaskadierende Abbrüche verhindert.

    Raises:
        ValueError: bei einer unbekannten Variante.
    """
    if variant not in ("basic", "strict", "rigorous"):
        raise ValueError("unbekannte Variante")
    return variant in ("strict", "rigorous")


def lock_granularity():
    """Nennt die Sperrgranulate von grob nach fein."""
    return ["database", "table", "page", "row"]
