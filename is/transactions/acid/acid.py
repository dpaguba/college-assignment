"""ACID-Eigenschaften und die Isolationsstufen von SQL."""

ANOMALIES = ["dirty read", "non repeatable read", "phantom"]

LEVELS = {
    "read uncommitted": ["dirty read", "non repeatable read", "phantom"],
    "read committed": ["non repeatable read", "phantom"],
    "repeatable read": ["phantom"],
    "serializable": [],
}


def properties():
    """Nennt die vier Eigenschaften einer Transaktion."""
    return ["atomicity", "consistency", "isolation", "durability"]


def transfer(balance, amount, fail_midway):
    """Führt eine Überweisung aus und macht sie bei einem Fehler rückgängig.

    Args:
        balance: Anfangsbestand des Quellkontos.
        amount: zu überweisender Betrag.
        fail_midway: wenn wahr, bricht die Transaktion nach der Abbuchung
            ab.

    Returns:
        Abbildung mit den Beständen beider Konten nach dem Ende der
        Transaktion.

    Raises:
        ValueError: wenn der Betrag negativ ist.
    """
    if amount < 0:
        raise ValueError("Betrag ist negativ")
    before = {"from": balance, "to": 0}
    working = dict(before)
    working["from"] -= amount
    if fail_midway:
        return before
    working["to"] += amount
    return working


def allows(level, anomaly):
    """Sagt, ob eine Isolationsstufe eine Anomalie zulässt.

    Raises:
        ValueError: bei unbekannter Stufe oder Anomalie.
    """
    if level not in LEVELS:
        raise ValueError("unbekannte Isolationsstufe")
    if anomaly not in ANOMALIES:
        raise ValueError("unbekannte Anomalie")
    return anomaly in LEVELS[level]


def anomalies(level):
    """Nennt die Anomalien, die eine Stufe zulässt."""
    if level not in LEVELS:
        raise ValueError("unbekannte Isolationsstufe")
    return list(LEVELS[level])


def durability_needs_the_log():
    """Beschreibt, worauf die Dauerhaftigkeit beruht."""
    return {"written before commit": "log", "may lag": "data pages"}
