"""Speichern und Prüfen von Passwörtern."""

import hashlib
import hmac
import math
import os
import time

ITERATIONS = 100000

COMMON = ("123456", "password", "hunter2", "qwerty", "letmein", "dragon")


def store(password, iterations=ITERATIONS, salt=None):
    """Bildet einen Datensatz aus Salz, abgeleitetem Wert und Rundenzahl.

    Raises:
        ValueError: bei einem leeren Passwort.
    """
    if not password:
        raise ValueError("leeres Passwort")
    if salt is None:
        salt = os.urandom(16)
    return {"salt": salt, "iterations": iterations,
            "hash": hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                        salt, iterations)}


def verify(password, record):
    """Prüft ein Passwort gegen einen Datensatz.

    Der Vergleich läuft in gleichbleibender Zeit, damit er nicht über
    seine Dauer verrät, wie viele Bytes gestimmt haben.
    """
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"),
                                    record["salt"], record["iterations"])
    return hmac.compare_digest(candidate, record["hash"])


def entropy(alphabet, length):
    """Informationsgehalt eines gleichverteilt gewählten Passworts in Bit.

    Die Rechnung setzt voraus, dass wirklich gleichverteilt gewählt wurde;
    für ein von Hand ausgedachtes Passwort ist sie eine Obergrenze, die
    weit über dem liegt, was tatsächlich zu raten ist.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if alphabet < 1 or length < 1:
        raise ValueError("Alphabet und Laenge muessen positiv sein")
    return length * math.log2(alphabet)


def dictionary_attack(accounts=8, iterations=1000):
    """Führt einen Wörterbuchangriff auf einen Bestand aus.

    Ein Teil der Konten benutzt ein Passwort aus der Liste der häufigen,
    der Rest ein zufälliges. Der Angreifer probiert die Liste gegen jeden
    Datensatz; wegen des Salzes muss er das je Konto einzeln tun, und
    genau das ist der Aufwand, den das Salz erzwingt.

    Returns:
        Abbildung mit der Zahl der Konten, der geknackten und der Versuche.
    """
    passwords = []
    for index in range(accounts):
        if index % 2 == 0:
            passwords.append(COMMON[index // 2 % len(COMMON)])
        else:
            passwords.append(os.urandom(12).hex())
    records = [store(password, iterations=iterations)
               for password in passwords]
    cracked = 0
    attempts = 0
    for record in records:
        for candidate in COMMON:
            attempts += 1
            if verify(candidate, record):
                cracked += 1
                break
    return {"accounts": accounts, "cracked": cracked, "attempts": attempts,
            "attempts without salt": len(COMMON),
            "why": "the salt forces the attacker to redo the work per "
                   "account"}


def length_versus_complexity():
    """Vergleicht ein Passwort aus Wörtern mit einem aus Sonderzeichen.

    Vier zufällig gezogene Wörter aus einer Liste von 7776 tragen 51.7
    Bit. Acht gemischte Zeichen trügen 52.6 Bit, wenn sie gleichverteilt
    gewählt würden; von Hand gewählt werden sie es nicht, und die
    gemessenen Schätzungen liegen bei etwa 30 Bit. Dazu kommt, dass die
    vier Wörter zu merken sind und die acht Zeichen aufgeschrieben werden.

    Returns:
        Abbildung mit den Werten.
    """
    words = entropy(7776, 4)
    uniform_characters = entropy(95, 8)
    return {"four common words": words,
            "eight mixed characters": 30.0,
            "eight mixed characters if chosen uniformly": uniform_characters,
            "note": "the uniform figure is an upper bound nobody reaches by "
                    "hand"}


def work_factor(iterations_low=1000, iterations_high=100000):
    """Misst, wie die Rundenzahl den Aufwand eines Angriffs bestimmt.

    Returns:
        Abbildung mit der Zeit für einen Versuch in beiden Einstellungen.
    """
    salt = b"0123456789abcdef"
    start = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", b"hunter2", salt, iterations_low)
    without = time.perf_counter() - start
    start = time.perf_counter()
    hashlib.pbkdf2_hmac("sha256", b"hunter2", salt, iterations_high)
    with_stretching = time.perf_counter() - start
    return {"without": without, "with stretching": with_stretching,
            "factor": iterations_high / iterations_low,
            "for the user": "one login, unnoticeable",
            "for the attacker": "every guess, multiplied"}


def rules():
    """Nennt, was beim Speichern zu beachten ist."""
    return ["a fresh salt per record",
            "a function built to be slow: pbkdf2, scrypt, argon2",
            "a work factor raised as hardware gets faster",
            "a comparison in constant time",
            "no length limit that forces short passwords",
            "a check against lists of leaked passwords"]


def what_not_to_do():
    """Nennt die Fehler, die immer wieder gemacht werden."""
    return ["storing the password itself",
            "a single unsalted digest",
            "a fast hash such as md5 or a bare sha256",
            "a salt that is the same for everyone",
            "rules that force a pattern, so everyone appends the same digit",
            "a hint field, which is a second password in plain text"]
