"""Schlüsselvereinbarung aus einem Passwort."""

import hashlib

PRIME = (1 << 127) - 1
COFACTOR = 2


def _generator_from(password, prime=PRIME):
    """Leitet aus dem Passwort einen Erzeuger der Gruppe ab.

    Beide Seiten kommen nur dann auf denselben Erzeuger, wenn sie dasselbe
    Passwort kennen; das Passwort selbst wird dabei nicht übertragen. Der
    Modul ist die Mersenne-Primzahl 2¹²⁷ − 1, klein genug zum Nachrechnen
    und gross genug, dass die Rechnung nicht entartet; ein Einsatz bräuchte
    eine sichere Primzahl von mindestens 2048 Bit.
    """
    digest = hashlib.sha256(password.encode("utf-8")).digest()
    value = int.from_bytes(digest, "big") % prime
    return pow(max(value, 2), COFACTOR, prime)


def exchange(first_password, second_password, first_secret=0x1234,
             second_secret=0x5678, prime=PRIME):
    """Führt die Vereinbarung zwischen zwei Seiten aus.

    Der Ablauf folgt dem Gedanken von SPEKE: der Erzeuger kommt aus dem
    Passwort, darüber läuft eine gewöhnliche Vereinbarung. Wer das
    Passwort nicht kennt, hat einen anderen Erzeuger und kommt auf einen
    anderen Schlüssel; auf der Leitung steht nichts, woran sich ein
    geratenes Passwort prüfen liesse.

    Args:
        first_password, second_password: was die beiden Seiten eingeben.
        first_secret, second_secret: die kurzlebigen Exponenten.
        prime: der Modul.

    Returns:
        Abbildung mit beiden Schlüsseln und der Frage, ob sie gleich sind.
    """
    first_generator = _generator_from(first_password, prime)
    second_generator = _generator_from(second_password, prime)
    first_public = pow(first_generator, first_secret, prime)
    second_public = pow(second_generator, second_secret, prime)
    first_key = pow(second_public, first_secret, prime)
    second_key = pow(first_public, second_secret, prime)
    return {"agreed": first_key == second_key,
            "first key": first_key, "second key": second_key,
            "on the wire": [first_public, second_public],
            "password sent": False}


def naive_scheme():
    """Bewertet den Vorschlag, einfach den Streuwert zu schicken.

    Wer den Streuwert überträgt, überträgt damit das, was der Server
    prüft: ein Mithörer kann ihn aufzeichnen und später erneut senden,
    ohne das Passwort zu kennen. Ausserdem kann er ihn gegen ein
    Wörterbuch rechnen, so oft er will, ohne dass der Server etwas merkt.

    Returns:
        Abbildung mit den beiden Schwächen.
    """
    password = "correct horse"
    sent = hashlib.sha256(password.encode("utf-8")).hexdigest()
    guesses = ["password", "correct horse", "hunter2"]
    cracked = any(hashlib.sha256(guess.encode("utf-8")).hexdigest() == sent
                  for guess in guesses)
    return {"replayable": True, "offline attack possible": cracked,
            "what the server checks": "exactly what travelled",
            "conclusion": "the hash has become the password"}


def properties():
    """Nennt, was ein ordentliches Verfahren leistet und was nicht.

    Aus dem Mitgehörten lässt sich kein Passwort prüfen, ein Angriff aus
    dem Wörterbuch muss also gegen den Server laufen. Dort kostet jeder
    Versuch eine Verbindung, und der Server kann zählen und bremsen.
    """
    return {"offline dictionary attack prevented": True,
            "one guess per attempt": True,
            "online guessing still possible": True,
            "password never sent": True,
            "mutual": "both sides learn whether the other knew it",
            "answer to online guessing": "rate limiting and lock out"}


def why_not_just_tls():
    """Erklärt, was das Verfahren zusätzlich zur verschlüsselten Leitung gibt.

    Über eine verschlüsselte Leitung geht das Passwort im Klartext an den
    Server, der es also sieht und richtig behandeln muss. Bei einer
    Vereinbarung aus dem Passwort sieht ihn niemand, auch der Server
    nicht; er hält nur einen davon abgeleiteten Wert.
    """
    return {"over tls": "the server receives the password itself",
            "with a password based exchange": "the server never sees it",
            "still needed": "the server must be the right one, which is "
                            "what the certificate is for"}


def examples():
    """Nennt die Verfahren, die in der Literatur vorkommen."""
    return {"EKE": "the first construction, by Bellovin and Merritt",
            "SPEKE": "the generator is derived from the password",
            "SRP": "widely deployed, the server stores a verifier",
            "OPAQUE": "the current recommendation, the server learns "
                      "nothing about the password"}
