"""Digitale Signaturen mit RSA und warum vorher gehesht wird."""

import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "rsa"))

import rsa


def sign(message, d, n):
    """Signiert eine Zahl mit dem geheimen Schlüssel.

    Signieren ist dieselbe Rechnung wie Entschlüsseln, nur mit vertauschten
    Rollen der Schlüssel.

    Raises:
        ValueError: wenn die Nachricht nicht kleiner als der Modul ist.
    """
    if not 0 <= message < n:
        raise ValueError("die Nachricht passt nicht in den Modul")
    return pow(message, d, n)


def verify(message, signature, e, n):
    """Prüft eine Signatur mit dem öffentlichen Schlüssel."""
    return pow(signature, e, n) == message % n


def hash_to_int(data, n):
    """Bildet beliebige Daten auf eine Zahl unter dem Modul ab."""
    digest = hashlib.sha256(data).digest()
    return int.from_bytes(digest, "big") % n


def sign_with_hash(data, d, n):
    """Signiert beliebige Daten, indem zuerst gehesht wird."""
    return sign(hash_to_int(data, n), d, n)


def verify_with_hash(data, signature, e, n):
    """Prüft eine Signatur über beliebigen Daten."""
    return verify(hash_to_int(data, n), signature, e, n)


def which_key():
    """Hält fest, welcher Schlüssel wofür benutzt wird.

    Verschlüsselt wird mit dem öffentlichen und entschlüsselt mit dem
    geheimen Schlüssel; signiert wird mit dem geheimen und geprüft mit dem
    öffentlichen. Die Rechnung ist dieselbe, der Zweck der umgekehrte.
    """
    return {"sign with": "private", "verify with": "public",
            "encrypt with": "public", "decrypt with": "private",
            "same operation": True}


def why_hash_first():
    """Nennt die Gründe, vor dem Signieren zu heshen.

    Eine Nachricht kann länger sein als der Modul und liesse sich sonst
    gar nicht signieren. Der Streuwert hat feste Länge, also bleibt die
    Signatur ein Block, gleich wie lang die Nachricht ist. Ausserdem
    nimmt das Heshen der Signatur die Rechenstruktur, an der die
    Formbarkeit hängt.

    Returns:
        Abbildung mit den drei Gründen.
    """
    return {"message longer than the modulus": True,
            "signature stays one block": True,
            "removes the multiplicative structure": True,
            "cost": "one pass over the message instead of one modular "
                    "exponentiation per block"}


def malleability():
    """Zeigt, dass rohe RSA-Signaturen formbar sind.

    Aus den Signaturen zweier Nachrichten lässt sich die Signatur ihres
    Produkts bilden, ohne den geheimen Schlüssel zu kennen: die Rechnung
    ist multiplikativ. Wird stattdessen der Streuwert signiert, so
    entspricht dem Produkt der Signaturen kein Streuwert einer Nachricht.

    Returns:
        Abbildung mit dem Befund für beide Fälle.
    """
    key = rsa.build_key(61, 53, 17)
    first, second = 5, 7
    signature_first = sign(first, key["d"], key["n"])
    signature_second = sign(second, key["d"], key["n"])
    forged = (signature_first * signature_second) % key["n"]
    product = (first * second) % key["n"]
    raw_works = verify(product, forged, key["e"], key["n"])
    hashed_first = sign_with_hash(b"five", key["d"], key["n"])
    hashed_second = sign_with_hash(b"seven", key["d"], key["n"])
    hashed_forged = (hashed_first * hashed_second) % key["n"]
    hashed_works = verify_with_hash(b"fiveseven", hashed_forged, key["e"],
                                    key["n"])
    return {"forged a signature without the key": raw_works,
            "same trick with a hash": hashed_works,
            "forged signature": forged, "product": product}


def properties():
    """Nennt, was eine Signatur leistet und was nicht.

    Sie sagt, wer die Nachricht ausgestellt hat und dass sie unverändert
    ist, und der Aussteller kann es später nicht bestreiten. Sie verbirgt
    nichts: die Nachricht steht im Klartext daneben.
    """
    return {"authenticity": True, "integrity": True,
            "non repudiation": True, "confidentiality": False,
            "for confidentiality": "encrypt as well, and do it in the right "
                                   "order"}


def against_a_message_code():
    """Stellt Signatur und Nachrichtenauthentisierungskode gegenüber.

    Ein Kode braucht einen gemeinsamen Schlüssel; beide Seiten können ihn
    erzeugen, weshalb keine der anderen etwas beweisen kann. Eine Signatur
    braucht kein gemeinsames Geheimnis und ist gegenüber Dritten
    nachweisbar.
    """
    return {"mac": {"key": "shared", "third party can verify": False,
                    "non repudiation": False, "speed": "fast"},
            "signature": {"key": "a pair", "third party can verify": True,
                          "non repudiation": True, "speed": "slow"}}
