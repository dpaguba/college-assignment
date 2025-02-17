"""Verdeckte Kanäle: Übertragung über etwas, das nicht dafür gedacht ist."""

import math


def definition():
    """Beschreibt, was einen verdeckten Kanal ausmacht.

    Ein verdeckter Kanal überträgt Information über einen Mechanismus, der
    dafür nicht vorgesehen ist. Genau deshalb greift die Zugriffskontrolle
    nicht: sie bewacht die Wege, die zur Übertragung gedacht sind.
    """
    return {"designed to communicate": False, "carries information": True,
            "visible to access control": False,
            "bypasses": "the policy, not the mechanism"}


def kinds():
    """Nennt die beiden Arten und woran sie sich unterscheiden."""
    return {"storage": "one process writes a shared value, the other reads "
                       "it: a file name, a lock, a full disk",
            "timing": "one process changes how long something takes, the "
                      "other measures it"}


def timing_channel(message, threshold=5.0):
    """Überträgt Bits über die Laufzeit einer Operation.

    Der Sender arbeitet lange für eine Eins und kurz für eine Null; der
    Empfänger misst und vergleicht mit einer Schwelle. Geschrieben wird
    dabei nichts.

    Args:
        message: die zu übertragenden Bits.
        threshold: Schwelle, ab der eine Messung als Eins gilt.

    Returns:
        Die empfangenen Bits.
    """
    measured = [9.0 if bit else 1.0 for bit in message]
    return [1 if value > threshold else 0 for value in measured]


def capacity(error_rate):
    """Kapazität eines binären symmetrischen Kanals in Bit je Zeichen.

    Rauschen senkt die Kapazität, beseitigt den Kanal aber nicht: bei
    einer Fehlerrate unter einer Hälfte bleibt etwas übrig, und mit
    Wiederholung lässt es sich beliebig sicher machen.

    Raises:
        ValueError: bei einer Fehlerrate ausserhalb von [0, 1].
    """
    if not 0.0 <= error_rate <= 1.0:
        raise ValueError("Fehlerrate liegt ausserhalb von [0, 1]")
    if error_rate in (0.0, 1.0):
        return 1.0
    entropy = -(error_rate * math.log2(error_rate)
                + (1 - error_rate) * math.log2(1 - error_rate))
    return 1.0 - entropy


def closed_by_isolation(kind):
    """Sagt, ob die üblichen Isolationsmassnahmen den Kanal schliessen.

    Ein Speicherkanal braucht ein gemeinsam sichtbares Objekt; nimmt man
    es weg, ist der Kanal zu. Ein Zeitkanal braucht nur eine gemeinsame
    Ressource, deren Auslastung sich messen lässt, und die lässt sich
    nicht wegnehmen, solange beide auf derselben Maschine laufen.

    Raises:
        ValueError: bei einer unbekannten Art.
    """
    if kind not in kinds():
        raise ValueError("unbekannte Art")
    return kind == "storage"


def why_hard():
    """Nennt, warum verdeckte Kanäle schwerer zu bekämpfen sind."""
    return {"uses a legitimate mechanism": True,
            "no rule is broken": True,
            "closing it costs performance": True,
            "the remaining ones are found by measurement, not by rules": True}


def bandwidth_examples():
    """Nennt gemessene Grössenordnungen aus der Literatur."""
    return {"cache timing": "hundreds of kilobits per second between cores",
            "disk arm position": "a few bits per second",
            "power draw": "bits per second, and it crosses an air gap",
            "conclusion": "low bandwidth is still enough for a key"}
