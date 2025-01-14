"""RSA: Schlüsselbildung, Rechnung und die Fallen ohne Auffüllung."""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..",
                                "modular-arithmetic"))

import modular_arithmetic


def build_key(p, q, e):
    """Bildet ein Schlüsselpaar aus zwei Primzahlen und dem Exponenten.

    Args:
        p, q: zwei verschiedene Primzahlen.
        e: der öffentliche Exponent.

    Returns:
        Abbildung mit ``n``, ``phi``, ``e`` und ``d``.

    Raises:
        ValueError: wenn die Primzahlen gleich sind oder der Exponent
            nicht teilerfremd zu φ(n) ist.
    """
    if p == q:
        raise ValueError("die Primzahlen muessen verschieden sein")
    modulus = p * q
    phi = (p - 1) * (q - 1)
    if math.gcd(e, phi) != 1:
        raise ValueError("e ist nicht teilerfremd zu phi(n)")
    return {"p": p, "q": q, "n": modulus, "phi": phi, "e": e,
            "d": modular_arithmetic.inverse(e, phi)}


def exercise_key():
    """Löst Aufgabe 6.2a mit p = 7, q = 11 und e = 13.

    Es ist n = 77 und φ(n) = 60. Gesucht ist ein d unter 60 mit
    13·d ≡ 1 (mod 60); das ist d = 37, denn 13·37 = 481 = 8·60 + 1.

    Returns:
        Das Schlüsselpaar samt der Kontrollrechnung.
    """
    key = build_key(7, 11, 13)
    key["check"] = (key["e"] * key["d"]) % key["phi"]
    return key


def encrypt(message, e, n):
    """Verschlüsselt eine Zahl mit dem öffentlichen Schlüssel.

    Raises:
        ValueError: wenn die Nachricht nicht kleiner als der Modul ist.
    """
    if not 0 <= message < n:
        raise ValueError("die Nachricht passt nicht in den Modul")
    return pow(message, e, n)


def decrypt(ciphertext, d, n):
    """Entschlüsselt mit dem geheimen Schlüssel."""
    return pow(ciphertext, d, n)


def roundtrip_holds(key):
    """Prüft, dass jede Zahl unter dem Modul zurückkommt.

    Für ein quadratfreies n gilt m^(ed) ≡ m für alle m, auch für die, die
    nicht teilerfremd zu n sind; das folgt aus dem chinesischen Restsatz.
    """
    for message in range(key["n"]):
        if decrypt(encrypt(message, key["e"], key["n"]), key["d"],
                   key["n"]) != message:
            return False
    return True


def factor_from_phi(n, phi):
    """Bestimmt p und q, wenn n und φ(n) bekannt sind.

    Aus φ(n) = (p − 1)(q − 1) = n − p − q + 1 folgt p + q = n + 1 − φ(n).
    Mit Summe und Produkt sind p und q die Wurzeln einer quadratischen
    Gleichung. Das ist die Antwort auf Aufgabe 6.2b: wer φ(n) kennt, kennt
    die Faktoren, und φ(n) ist damit ebenso geheim zu halten wie d.

    Returns:
        Abbildung mit den Faktoren und der Kontrollrechnung.

    Raises:
        ValueError: wenn die Werte zu keiner ganzzahligen Lösung führen.
    """
    total = n + 1 - phi
    discriminant = total * total - 4 * n
    if discriminant < 0:
        raise ValueError("keine reelle Loesung")
    root = math.isqrt(discriminant)
    if root * root != discriminant:
        raise ValueError("keine ganzzahlige Loesung")
    if (total + root) % 2 or (total - root) % 2:
        raise ValueError("keine ganzzahlige Loesung")
    first = (total + root) // 2
    second = (total - root) // 2
    if first * second != n:
        raise ValueError("die Faktoren passen nicht zu n")
    return {"factors": [first, second], "sum": total,
            "product": first * second, "checks out": True}


def pad(message, randomness, n, block=1000):
    """Legt einen zufälligen Anteil vor die Nachricht.

    Die Auffüllung nach PKCS ist aufwendiger; entscheidend ist hier nur,
    dass derselbe Klartext bei jedem Aufruf zu einer anderen Zahl wird.

    Raises:
        ValueError: wenn das Ergebnis nicht mehr in den Modul passt.
    """
    padded = message + randomness * block
    if padded >= n:
        raise ValueError("die aufgefuellte Nachricht passt nicht in n")
    return padded


def unpad(value, block=1000):
    """Nimmt die Auffüllung wieder weg."""
    return value % block


def deterministic_without_padding(padded=False):
    """Zeigt, warum die Auffüllung nach PKCS nötig ist.

    Ein Angreifer, der weiss, an wen eine Nachricht ging, und der ahnt,
    was darin steht, verschlüsselt seine Vermutung mit dem öffentlichen
    Schlüssel und vergleicht. Ohne Auffüllung stimmt der Geheimtext
    überein und die Vermutung ist bestätigt; das ist ein gewählter
    Klartext, für den der Angreifer nichts weiter braucht als den
    öffentlichen Schlüssel.

    Args:
        padded: ob vor dem Verschlüsseln aufgefüllt wird.

    Returns:
        Abbildung mit beiden Geheimtexten und dem Befund.
    """
    key = build_key(61, 53, 17)
    message = 42
    if padded:
        first = encrypt(pad(message, 1, key["n"]), key["e"], key["n"])
        second = encrypt(pad(message, 2, key["n"]), key["e"], key["n"])
    else:
        first = encrypt(message, key["e"], key["n"])
        second = encrypt(message, key["e"], key["n"])
    return {"first": first, "second": second, "padded": padded,
            "attacker can confirm a guess": first == second}


def small_exponent(message=5):
    """Zeigt, was ein kleiner Exponent ohne Auffüllung anrichtet.

    Mit p = 11, q = 17 ist n = 187 und der Exponent 3 zulässig. Für eine
    kleine Nachricht bleibt m³ unter dem Modul, es wird also gar nicht
    reduziert, und die dritte Wurzel über den ganzen Zahlen gibt die
    Nachricht zurück. Der geheime Schlüssel spielt dabei keine Rolle.

    Returns:
        Abbildung mit dem Befund.
    """
    key = build_key(11, 17, 3)
    raw = message ** key["e"]
    ciphertext = encrypt(message, key["e"], key["n"])
    recovered = round(ciphertext ** (1.0 / key["e"]))
    return {"no reduction happened": raw < key["n"],
            "ciphertext equals the plain power": ciphertext == raw,
            "recoverable by taking a root": recovered == message,
            "message": message, "exponent": key["e"], "modulus": key["n"],
            "fix": "random padding, so the value is never small"}


def key_sizes():
    """Nennt, welche Modulgrössen als brauchbar gelten."""
    return {"512 bit": "factored in public, worthless",
            "1024 bit": "no longer recommended",
            "2048 bit": "the current minimum",
            "3072 bit": "roughly the strength of a 128 bit symmetric key",
            "note": "an elliptic curve reaches the same strength with far "
                    "shorter keys"}
