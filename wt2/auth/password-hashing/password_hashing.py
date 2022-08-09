"""Speichern von Passwörtern: Salz, Streckung und zeitgleicher Vergleich."""

import hashlib
import hmac
import os
import time

ITERATIONS = 100000


def store(password, iterations=ITERATIONS, salt=None):
    """Bildet einen Datensatz für ein Passwort.

    Das Salz ist je Datensatz neu, damit zwei gleiche Passwörter
    verschiedene Werte ergeben und eine vorberechnete Tabelle nichts
    nützt. Die Zahl der Wiederholungen macht das Ausprobieren teuer.

    Args:
        password: das Klartextpasswort.
        iterations: Zahl der Wiederholungen der Ableitung.
        salt: ein festes Salz, sonst ein zufälliges.

    Returns:
        Abbildung mit ``salt``, ``hash`` und ``iterations``.

    Raises:
        ValueError: bei einem leeren Passwort.
    """
    if not password:
        raise ValueError("leeres Passwort")
    if salt is None:
        salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt,
                                 iterations)
    return {"salt": salt, "hash": digest, "iterations": iterations}


def verify(password, record):
    """Prüft ein Passwort gegen einen Datensatz.

    Der Vergleich läuft über ``hmac.compare_digest`` und braucht damit
    unabhängig von der Zahl der übereinstimmenden Bytes gleich lang.
    """
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                 record["salt"], record["iterations"])
    return hmac.compare_digest(digest, record["hash"])


def uses_constant_time_comparison():
    """Sagt, ob der Vergleich zeitunabhängig ist.

    Ein Vergleich, der beim ersten abweichenden Byte abbricht, verrät über
    seine Laufzeit, wie viele Bytes gestimmt haben; damit lässt sich der
    richtige Wert Byte für Byte erraten.
    """
    return verify.__code__.co_names.count("compare_digest") > 0


def rainbow_table_report(passwords=("hunter2", "password", "123456")):
    """Vergleicht einen ungesalzenen mit einem gesalzenen Bestand.

    Für die ungesalzene Fassung wird eine Tabelle der gängigen Passwörter
    berechnet und mit dem Bestand verglichen; für die gesalzene ist
    dieselbe Tabelle wertlos, weil jeder Datensatz ein eigenes Salz hat.

    Returns:
        Abbildung mit der Zahl der geknackten Datensätze in beiden Fällen.
    """
    common = ["hunter2", "password", "123456", "qwerty"]
    table = {hashlib.sha256(word.encode("utf-8")).digest(): word
             for word in common}
    unsalted = [hashlib.sha256(word.encode("utf-8")).digest()
                for word in passwords]
    salted = [store(word, iterations=1000) for word in passwords]
    cracked_without = sum(1 for digest in unsalted if digest in table)
    cracked_with = sum(1 for record in salted if record["hash"] in table)
    return {"cracked without salt": cracked_without,
            "cracked with salt": cracked_with,
            "records": len(passwords)}


def cost_of_iterations(few=1000, many=50000):
    """Misst, wie die Zahl der Wiederholungen die Zeit bestimmt.

    Returns:
        Abbildung mit beiden Zeiten in Sekunden.
    """
    salt = b"0123456789abcdef"
    start = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", b"hunter2", salt, few)
    quick = time.perf_counter() - start
    start = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", b"hunter2", salt, many)
    slow = time.perf_counter() - start
    return {"few": quick, "many": slow, "few iterations": few,
            "many iterations": many}


def why_not_a_plain_digest(samples=20000):
    """Misst, wie viel schneller ein blosser Streuwert ist.

    Ein Streuwert ist dafür gebaut, schnell zu sein; genau das braucht der
    Angreifer, der Milliarden Kandidaten durchprobiert. Eine Ableitung ist
    dafür gebaut, langsam zu sein.

    Returns:
        Abbildung mit beiden Geschwindigkeiten je Sekunde.
    """
    start = time.perf_counter()
    for index in range(samples):
        hashlib.sha256(str(index).encode("utf-8")).digest()
    digest_time = time.perf_counter() - start
    rounds = 50
    start = time.perf_counter()
    for index in range(rounds):
        hashlib.pbkdf2_hmac("sha256", str(index).encode("utf-8"),
                            b"salt", ITERATIONS)
    derive_time = time.perf_counter() - start
    return {"digests per second": samples / max(digest_time, 1e-9),
            "derivations per second": rounds / max(derive_time, 1e-9)}


def recommendations():
    """Nennt, worauf es beim Speichern von Passwörtern ankommt."""
    return ["a fresh salt per record",
            "a function built to be slow",
            "enough iterations that a check takes a noticeable moment",
            "a comparison that does not leak its progress",
            "never the password itself, not even in a log"]
