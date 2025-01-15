"""Mehrere Faktoren und was sie tatsächlich abdecken."""

import hashlib
import hmac
import struct

KIND_OF = {
    "password": "knowledge", "pin": "knowledge", "answer": "knowledge",
    "token": "possession", "phone": "possession", "smart card": "possession",
    "security key": "possession", "one time code": "possession",
    "fingerprint": "inherence", "face": "inherence", "iris": "inherence",
}

PHISHING_RESISTANT = {"security key", "smart card"}


def factors():
    """Nennt die drei Arten von Faktoren mit Beispielen."""
    return {"knowledge": "something you know, such as a password",
            "possession": "something you have, such as a key or a phone",
            "inherence": "something you are, such as a fingerprint"}


def kind_of(name):
    """Ordnet einen Faktor seiner Art zu.

    Raises:
        ValueError: bei einem unbekannten Faktor.
    """
    if name not in KIND_OF:
        raise ValueError("unbekannter Faktor")
    return KIND_OF[name]


def is_multi_factor(names):
    """Sagt, ob eine Auswahl wirklich mehrere Faktoren benutzt.

    Zwei Dinge, die man weiss, sind ein Faktor, zweimal abgefragt. Erst
    Faktoren verschiedener Art decken verschiedene Angriffe ab: was ein
    Ableser des Passworts erfährt, hilft ihm gegen den Schlüssel nicht.

    Raises:
        ValueError: bei einem unbekannten Faktor oder leerer Auswahl.
    """
    if not names:
        raise ValueError("keine Faktoren genannt")
    return len({kind_of(name) for name in names}) > 1


def time_code(secret, moment, digits=6, window=30):
    """Berechnet einen zeitabhängigen Einmalkode.

    Gerechnet wird über der Zeitscheibe, nicht über der Sekunde, damit
    beide Seiten trotz kleiner Abweichung denselben Wert erhalten. Das
    Verfahren ist das von RFC 6238.

    Args:
        secret: das gemeinsame Geheimnis.
        moment: die Zeit in Sekunden.
        digits: Länge des Kodes.
        window: Länge einer Zeitscheibe in Sekunden.

    Returns:
        Der Kode als Zeichenkette mit führenden Nullen.

    Raises:
        ValueError: bei nicht positiver Stellenzahl oder Fensterlänge.
    """
    if digits < 1 or window < 1:
        raise ValueError("Stellenzahl und Fenster muessen positiv sein")
    counter = int(moment) // window
    digest = hmac.new(secret, struct.pack(">Q", counter),
                      hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    value = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return str(value % (10 ** digits)).zfill(digits)


def guessing(digits, attempts):
    """Schätzt, wie wahrscheinlich ein Angreifer einen Kode errät.

    Ohne Begrenzung der Versuche ist ein sechsstelliger Kode kein Hindernis:
    hunderttausend Versuche treffen mit rund einem Zehntel Wahrscheinlichkeit.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if digits < 1 or attempts < 1:
        raise ValueError("Werte muessen positiv sein")
    space = 10 ** digits
    probability = 1.0 - (1.0 - 1.0 / space) ** attempts
    return {"space": space, "attempts": attempts,
            "success probability": probability,
            "defence": "count the attempts and lock out"}


def stops_phishing(name):
    """Sagt, ob ein Faktor gegen eine weitergeleitete Anmeldung hilft.

    Ein Einmalkode wird abgetippt und lässt sich von einer falschen Seite
    entgegennehmen und sofort weiterreichen. Ein Sicherheitsschlüssel
    unterschreibt die Herkunft mit; auf der falschen Seite passt die
    Unterschrift nicht.

    Raises:
        ValueError: bei einem unbekannten Faktor.
    """
    if name not in KIND_OF:
        raise ValueError("unbekannter Faktor")
    return name in PHISHING_RESISTANT


def recovery_is_the_weak_point():
    """Nennt die Stelle, an der die Kette meist reisst.

    Ein zweiter Faktor nützt wenig, wenn der Weg um ihn herum offen ist:
    der Ersatzkode per Post, die Sicherheitsfrage, der Anruf beim
    Kundendienst. Der Angreifer nimmt den billigsten Weg, und das ist
    selten der beabsichtigte.
    """
    return {"backup codes": "a second password, often written down",
            "security questions": "answers that are public knowledge",
            "support desk": "a person who can be talked to",
            "sim swap": "the phone number moves to the attacker",
            "rule": "the recovery path needs the same strength as the "
                    "main one"}


def what_each_factor_costs():
    """Stellt Aufwand und Wirkung der Faktoren gegenüber."""
    return {"password": {"cost": "none", "phishable": True},
            "one time code": {"cost": "an app or a device",
                              "phishable": True},
            "push confirmation": {"cost": "an app",
                                  "phishable": True,
                                  "note": "fatigue attacks work"},
            "security key": {"cost": "hardware", "phishable": False},
            "fingerprint": {"cost": "a sensor", "phishable": False,
                            "note": "cannot be changed once copied"}}
