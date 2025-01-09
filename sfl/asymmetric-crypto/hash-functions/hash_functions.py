"""Geshfunktionen: die drei Kriterien und drei Kandidaten aus der Übung."""

import hashlib

CRITERIA = ("compression", "preimage resistance",
            "second preimage resistance", "collision resistance")


def criteria():
    """Nennt die Kriterien, an denen eine Geshfunktion gemessen wird."""
    return list(CRITERIA)


def last_block(blocks):
    """Erste Kandidatin aus Aufgabe 6.3: der letzte Block.

    Raises:
        ValueError: bei einer leeren Nachricht.
    """
    if not blocks:
        raise ValueError("leere Nachricht")
    return blocks[-1]


def block_sum(blocks, modulus=1 << 32):
    """Zweite Kandidatin: die Summe aller Blöcke.

    Raises:
        ValueError: bei einer leeren Nachricht.
    """
    if not blocks:
        raise ValueError("leere Nachricht")
    return sum(blocks) % modulus


def double(blocks, inner=None):
    """Dritte Kandidatin: eine gute Funktion, zweimal angewandt.

    Args:
        blocks: die Nachricht.
        inner: die innere Funktion; ohne Angabe wird SHA-256 benutzt.
    """
    if inner is None:
        def inner(values):
            """Bildet eine Blockfolge auf einen Streuwert ab.

            Die Blöcke werden auf zweiunddreissig Byte gebracht, damit die
            Funktion ihre eigene Ausgabe wieder als Eingabe annimmt; ohne
            das liesse sie sich nicht zweimal anwenden.
            """
            data = b"".join((int(value) % (1 << 256)).to_bytes(32, "big")
                            for value in values)
            return int.from_bytes(hashlib.sha256(data).digest(), "big")
    first = inner(blocks)
    return inner([first])


def preimage_of_last_block(target):
    """Baut zu einem Streuwert eine Nachricht, die ihn liefert.

    Für die erste Kandidatin ist das kein Suchen: jede Nachricht, die auf
    den gewünschten Block endet, hat ihn als Streuwert. Damit fällt die
    Urbildfestigkeit sofort.
    """
    return [0, target]


def second_preimage_of_last_block(blocks):
    """Baut zu einer Nachricht eine zweite mit demselben Streuwert."""
    return [12345] + list(blocks)


def collision_for_sum():
    """Baut zwei verschiedene Nachrichten mit derselben Blocksumme.

    Die Addition ist kommutativ, also genügt es, zwei Blöcke zu tauschen;
    ausserdem lässt sich ein Block um einen Betrag erhöhen und ein anderer
    um denselben senken.

    Returns:
        Zwei verschiedene Blockfolgen.
    """
    return [1, 2, 3], [3, 2, 1]


def rate(name):
    """Bewertet eine der drei Kandidatinnen nach den Kriterien.

    Die erste erfüllt nur die Verdichtung: ein Urbild ist hingeschrieben,
    ein zweites ebenso, und damit fallen auch die Kollisionen. Die zweite
    verdichtet ebenfalls, ist aber gegen Umordnung blind. Die dritte erbt
    alle Eigenschaften der inneren Funktion, weil jede Kollision der
    zusammengesetzten Funktion eine Kollision der inneren enthält.

    Args:
        name: ``last block``, ``sum`` oder ``double``.

    Returns:
        Abbildung von den Kriterien auf die Bewertung samt Begründung.

    Raises:
        ValueError: bei einer unbekannten Kandidatin.
    """
    if name == "last block":
        return {"compression": True, "preimage resistance": False,
                "second preimage resistance": False,
                "collision resistance": False,
                "why": "any message ending in the wanted block works, and "
                       "prefixing anything keeps the hash"}
    if name == "sum":
        return {"compression": True, "preimage resistance": False,
                "second preimage resistance": False,
                "collision resistance": False,
                "why": "addition is commutative, so any reordering "
                       "collides, and a single block reaches any value"}
    if name == "double":
        return {"compression": True, "preimage resistance": True,
                "second preimage resistance": True,
                "collision resistance": True,
                "why": "a collision of the composition contains a collision "
                       "of the inner function",
                "condition": "the inner function must accept its own output"}
    raise ValueError("unbekannte Kandidatin")


def birthday_bound(bits):
    """Aufwand, mit dem eine Kollision zu erwarten ist.

    Nach dem Geburtstagsproblem genügen etwa zwei hoch der halben
    Ausgabelänge Versuche; deshalb braucht eine Funktion doppelt so viele
    Ausgabebits, wie die gewünschte Sicherheit verlangt.

    Raises:
        ValueError: bei einer nicht positiven Bitzahl.
    """
    if bits < 1:
        raise ValueError("Bitzahl muss positiv sein")
    return 1 << (bits // 2)


def invertible_but_collision_resistant(input_bits=512, output_bits=160):
    """Beantwortet Aufgabe 6.3d.

    Gegeben ist eine Funktion mit einer Umkehrung, die zu jedem Streuwert
    ein Urbild liefert. Ein Angreifer nimmt eine beliebige Nachricht,
    bildet ihren Streuwert und lässt sich dazu ein Urbild geben. Da der
    Eingaberaum viel grösser ist als der Ausgaberaum, hat fast jeder
    Streuwert sehr viele Urbilder, und das zurückgegebene ist mit
    überwältigender Wahrscheinlichkeit ein anderes als das ursprüngliche.
    Zwei Auswertungen genügen also für eine Kollision.

    Returns:
        Abbildung mit dem Befund, dem Aufwand und dem Vergleich zum
        Geburtstagsangriff.
    """
    preimages_per_hash = 1 << (input_bits - output_bits)
    chance_of_the_same = 1.0 / preimages_per_hash
    return {"collision resistance possible": False,
            "work to find a collision": 2,
            "birthday work without the inverse": birthday_bound(output_bits),
            "preimages per hash": preimages_per_hash,
            "probability the inverse returns the same message":
                chance_of_the_same,
            "why": "hash a message, ask the inverse for a preimage, and it "
                   "is almost certainly a different message with the same "
                   "hash"}


def md5_versus_sha256():
    """Vergleicht die beiden Funktionen aus Aufgabe 6.3b.

    Beide verdichten, aber für die eine sind Kollisionen seit langem
    veröffentlicht: zwei verschiedene Dateien mit demselben Streuwert
    lassen sich in Sekunden erzeugen. Damit taugt sie nicht mehr dort, wo
    es auf Unversehrtheit ankommt, wohl aber noch als Prüfsumme gegen
    zufällige Übertragungsfehler.

    Returns:
        Abbildung mit den Ausgabelängen und dem Stand der Angriffe.
    """
    return {"md5 bits": 128, "sha256 bits": 256,
            "md5 has known collisions": True,
            "sha256 has known collisions": False,
            "md5 birthday bound": birthday_bound(128),
            "sha256 birthday bound": birthday_bound(256),
            "conclusion": "a hash may still compress and be useless for "
                          "security"}


def digest_of(data, algorithm="sha256"):
    """Berechnet einen Streuwert mit der Standardbibliothek.

    Raises:
        ValueError: bei einem unbekannten Verfahren.
    """
    if algorithm not in ("md5", "sha1", "sha256", "sha512"):
        raise ValueError("unbekanntes Verfahren")
    return hashlib.new(algorithm, data).hexdigest()


def where_they_are_used():
    """Nennt die Aufgaben, für die Geshfunktionen eingesetzt werden."""
    return {"integrity": "compare a value instead of the whole file",
            "signatures": "sign the hash, not the message",
            "passwords": "store a derived value, never the password",
            "commitment": "publish the hash now, the value later",
            "deduplication": "the same hash means the same content"}
