"""Angriffe auf die verschlüsselte Verbindung."""

import hashlib
import zlib

VERSIONS = ("ssl3.0", "tls1.0", "tls1.1", "tls1.2", "tls1.3")
BLOCK = 8


def downgrade_possible(offered, minimum):
    """Sagt, ob ein Angreifer auf eine schwächere Fassung drücken kann.

    Wer die Verbindung beherrscht, streicht aus der Liste der angebotenen
    Fassungen die starken heraus; beide Seiten einigen sich dann auf die
    schwächste, die beide noch annehmen. Eine untere Schranke auf der
    Serverseite schliesst das aus.

    Args:
        offered: die angebotenen Fassungen.
        minimum: die niedrigste, die noch angenommen wird.

    Raises:
        ValueError: bei einer unbekannten Fassung.
    """
    for name in list(offered) + [minimum]:
        if name not in VERSIONS:
            raise ValueError("unbekannte Fassung: %s" % name)
    lowest = min(offered, key=VERSIONS.index)
    return VERSIONS.index(lowest) >= VERSIONS.index(minimum)


def stripping():
    """Beschreibt das Abstreifen der Verschlüsselung.

    Der erste Aufruf einer Adresse geht meist unverschlüsselt hinaus und
    wird erst umgeleitet. Wer dazwischen sitzt, beantwortet ihn selbst,
    spricht mit dem Server verschlüsselt und mit dem Benutzer nicht. Die
    Ansage, dass diese Adresse nur verschlüsselt zu erreichen ist, nimmt
    dem Angriff die Gelegenheit, sobald sie einmal angekommen ist.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"first visit vulnerable": True,
            "with strict transport security": False,
            "remaining gap": "the very first visit, before the header was "
                             "ever seen",
            "closed by": "a preload list shipped with the browser"}


def _model_compressed_size(text):
    """Modelliert die Grösse nach einer Kompression mit Rückwärtsverweisen.

    Gezählt wird die Länge abzüglich der längsten Zeichenkette, die ein
    zweites Mal vorkommt. Das ist der Kern dessen, was eine Kompression
    mit Wörterbuch tut, und genügt, um den Angriff zu zeigen.
    """
    longest = 0
    length = len(text)
    for start in range(length):
        for end in range(start + longest + 1, length + 1):
            piece = text[start:end]
            if text.count(piece) > 1:
                longest = max(longest, end - start)
            else:
                break
    return length - longest


def compression_leak(secret="token=7Q4"):
    """Zeigt, wie die Grösse eines komprimierten Pakets ein Geheimnis verrät.

    Der Angreifer bringt eigenen Text in dieselbe Nachricht, in der das
    Geheimnis steht, und beobachtet die Grösse. Trifft sein Text den
    Anfang des Geheimnisses, so findet die Kompression eine längere
    Wiederholung und das Paket wird kürzer. Zeichen für Zeichen liest er
    das Geheimnis so aus, ohne die Verschlüsselung anzurühren.

    Returns:
        Abbildung mit dem geratenen Geheimnis und dem Befund.
    """
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ=aeiokntr"
    known = secret[:6]
    queries = 0
    while len(known) < len(secret):
        best = None
        for candidate in alphabet:
            attempt = known + candidate
            queries += 1
            size = _model_compressed_size(attempt + secret)
            if best is None or size < best[0]:
                best = (size, candidate)
        known += best[1]
    with_zlib = len(zlib.compress((known + secret).encode("utf-8"), 9))
    return {"guessed the secret": known == secret, "guess": known,
            "secret": secret, "queries": queries,
            "zlib size of the final guess": with_zlib,
            "fix": "do not compress a message that mixes attacker input "
                   "with a secret"}


def _keystream(key, length):
    """Erzeugt einen Strom fester Länge aus einem Schlüssel."""
    output = b""
    counter = 0
    while len(output) < length:
        output += hashlib.sha256(key + str(counter).encode()).digest()
        counter += 1
    return output[:length]


def _decrypt_block(key, block):
    """Kehrt die Blockabbildung um.

    Die Abbildung ist ein Platzhalter für eine echte Blockchiffre; für den
    Ablauf des Angriffs kommt es nur darauf an, dass sie umkehrbar ist und
    der Angreifer sie nicht kennt.
    """
    stream = _keystream(key, BLOCK)
    return bytes(a ^ b for a, b in zip(block, stream))


def _valid_padding(data):
    """Prüft eine Auffüllung nach PKCS."""
    if not data:
        return False
    value = data[-1]
    if not 1 <= value <= BLOCK or value > len(data):
        return False
    return all(byte == value for byte in data[-value:])


def padding_oracle():
    """Führt den Angriff über die Auffüllung durch.

    Der Server verrät durch seine Antwort, ob die Auffüllung stimmte. Der
    Angreifer verändert den vorangehenden Block und liest daraus Byte für
    Byte den Zwischenwert der Entschlüsselung ab; mit dem echten
    vorangehenden Block ergibt sich der Klartext. Der Schlüssel wird dabei
    nie gebraucht.

    Returns:
        Abbildung mit dem gefundenen Klartext, der Zahl der Fragen und der
        Länge.
    """
    key = b"a key"
    plaintext = b"secret!" + bytes([1])
    initial = bytes(range(BLOCK))
    stream = _keystream(key, BLOCK)
    ciphertext = bytes(a ^ b for a, b in
                       zip(bytes(x ^ y for x, y in zip(plaintext, initial)),
                           stream))
    queries = 0

    def oracle(forged_iv):
        """Sagt, ob die Auffüllung nach der Entschlüsselung stimmt."""
        nonlocal queries
        queries += 1
        middle = _decrypt_block(key, ciphertext)
        return _valid_padding(bytes(a ^ b for a, b in zip(middle,
                                                          forged_iv)))

    intermediate = [0] * BLOCK
    for position in range(BLOCK - 1, -1, -1):
        wanted = BLOCK - position
        found = None
        for guess in range(256):
            forged = bytearray(BLOCK)
            for index in range(position + 1, BLOCK):
                forged[index] = intermediate[index] ^ wanted
            forged[position] = guess
            if not oracle(bytes(forged)):
                continue
            if position == BLOCK - 1:
                forged[position - 1] ^= 0xFF
                if not oracle(bytes(forged)):
                    continue
            found = guess
            break
        if found is None:
            break
        intermediate[position] = found ^ wanted
    recovered = bytes(intermediate[index] ^ initial[index]
                      for index in range(BLOCK))
    return {"recovered the plaintext": recovered == plaintext,
            "plaintext": plaintext, "recovered": recovered,
            "queries": queries, "bytes": BLOCK,
            "key needed": False,
            "fix": "authenticate the ciphertext, and answer the same way "
                   "whether the padding or the tag was wrong"}


def lessons():
    """Fasst zusammen, was die drei Angriffe gemeinsam haben.

    Alle drei brechen die Chiffre nicht: sie lesen aus etwas anderem ab,
    aus der ausgehandelten Fassung, aus der Grösse, aus der Antwortzeit
    oder der Fehlermeldung. Die Antwort ist jedes Mal, den Geheimtext
    mitzuauthentisieren und keine Unterschiede nach aussen dringen zu
    lassen.

    Returns:
        Abbildung mit den Angriffen und den Gegenmitteln.
    """
    return {"attacks": ["downgrade", "stripping", "compression side "
                        "channel", "padding oracle"],
            "none of them breaks the cipher": True,
            "fixes": ["authenticated encryption",
                      "a minimum version, negotiated under a signature",
                      "strict transport security with preloading",
                      "no compression over mixed content",
                      "identical answers for every kind of failure"]}
