"""Betriebsarten einer Blockchiffre und was jede von ihnen verrät."""

MASK = 0xFFFFFFFF
MULTIPLIER = 0x2545F491
INVERSE = pow(MULTIPLIER, -1, 1 << 32)

MODES = ("ecb", "cbc", "ctr")


def modes():
    """Nennt die hier umgesetzten Betriebsarten."""
    return list(MODES)


def encrypt_block(key, value):
    """Verschlüsselt einen einzelnen Block.

    Die Abbildung ist eine Spielzeugchiffre: der Block wird mit dem
    Schlüssel verknüpft und mit einer ungeraden Zahl multipliziert, was
    modulo zwei hoch zweiunddreissig umkehrbar ist. Sie taugt nicht zum
    Schützen von Daten und genügt, um die Betriebsarten zu zeigen.
    """
    return ((value ^ key) * MULTIPLIER) & MASK


def decrypt_block(key, value):
    """Kehrt :func:`encrypt_block` um."""
    return (((value * INVERSE) & MASK) ^ key) & MASK


def encrypt(blocks, key, mode, nonce=0):
    """Verschlüsselt eine Folge von Blöcken in der genannten Betriebsart.

    Args:
        blocks: die Klartextblöcke als ganze Zahlen.
        key: der Schlüssel.
        mode: ``ecb``, ``cbc`` oder ``ctr``.
        nonce: Startwert; bei ``cbc`` der Initialisierungsvektor, bei
            ``ctr`` der Zählerbeginn.

    Returns:
        Liste der Geheimtextblöcke.

    Raises:
        ValueError: bei einer unbekannten Betriebsart.
    """
    if mode not in MODES:
        raise ValueError("unbekannte Betriebsart")
    if mode == "ecb":
        return [encrypt_block(key, block) for block in blocks]
    if mode == "cbc":
        previous = nonce
        result = []
        for block in blocks:
            previous = encrypt_block(key, block ^ previous)
            result.append(previous)
        return result
    return [block ^ encrypt_block(key, nonce + index)
            for index, block in enumerate(blocks)]


def decrypt(blocks, key, mode, nonce=0):
    """Entschlüsselt eine Folge von Blöcken.

    Raises:
        ValueError: bei einer unbekannten Betriebsart.
    """
    if mode not in MODES:
        raise ValueError("unbekannte Betriebsart")
    if mode == "ecb":
        return [decrypt_block(key, block) for block in blocks]
    if mode == "cbc":
        previous = nonce
        result = []
        for block in blocks:
            result.append(decrypt_block(key, block) ^ previous)
            previous = block
        return result
    return [block ^ encrypt_block(key, nonce + index)
            for index, block in enumerate(blocks)]


def needs_padding(mode):
    """Sagt, ob die Betriebsart volle Blöcke braucht.

    Die Zählerbetriebsart benutzt die Chiffre nur, um einen Schlüsselstrom
    zu erzeugen, und verknüpft ihn mit dem Klartext; ein angebrochener
    Block bleibt angebrochen. Die anderen beiden schicken den Klartext
    durch die Chiffre und brauchen deshalb volle Blöcke.

    Raises:
        ValueError: bei einer unbekannten Betriebsart.
    """
    if mode not in MODES:
        raise ValueError("unbekannte Betriebsart")
    return mode in ("ecb", "cbc")


def pattern_leak():
    """Misst, wie viel ein wiederholtes Muster im Geheimtext hinterlässt.

    Gleiche Klartextblöcke werden im Codebuchbetrieb zu gleichen
    Geheimtextblöcken; das Bild des Klartexts bleibt sichtbar. Die
    Verkettung mischt jeden Block mit dem vorigen und lässt keine
    Wiederholung übrig.

    Returns:
        Abbildung mit der Zahl verschiedener Blöcke in beiden Betriebsarten.
    """
    blocks = [1, 1, 1, 1, 2, 2, 2, 2, 1, 1]
    ecb = encrypt(blocks, key=7, mode="ecb")
    cbc = encrypt(blocks, key=7, mode="cbc", nonce=3)
    return {"plaintext blocks": len(blocks),
            "plaintext distinct blocks": len(set(blocks)),
            "ecb distinct blocks": len(set(ecb)),
            "cbc distinct blocks": len(set(cbc))}


def error_propagation():
    """Misst, wie weit ein einzelner Übertragungsfehler reicht.

    Ein verändertes Bit im Geheimtext verdirbt im Codebuchbetrieb genau
    seinen Block. Bei der Verkettung verdirbt es zusätzlich den folgenden,
    weil der vorige Geheimtextblock in die Entschlüsselung eingeht. Im
    Zählerbetrieb bleibt es bei einem Block.

    Returns:
        Abbildung von der Betriebsart auf die Zahl verdorbener Blöcke.
    """
    blocks = [5, 9, 13, 17, 21]
    report = {}
    for mode in MODES:
        cipher = encrypt(blocks, key=7, mode=mode, nonce=3)
        damaged = list(cipher)
        damaged[2] ^= 1
        recovered = decrypt(damaged, key=7, mode=mode, nonce=3)
        report[mode] = sum(1 for original, value in zip(blocks, recovered)
                           if original != value)
    return report


def nonce_reuse():
    """Zeigt, was zweimal derselbe Zähler bedeutet.

    Der Zählerbetrieb erzeugt aus Schlüssel und Zähler einen Strom und
    verknüpft ihn mit dem Klartext. Wird derselbe Zähler ein zweites Mal
    benutzt, so ist es derselbe Strom, und die Verknüpfung beider
    Geheimtexte lässt ihn wegfallen: derselbe Fehler wie ein zweimal
    benutztes Einmalblatt.

    Returns:
        Abbildung mit beiden Verknüpfungen, die übereinstimmen müssen.
    """
    first = [11, 22, 33, 44]
    second = [55, 66, 77, 88]
    cipher_first = encrypt(first, key=7, mode="ctr", nonce=1)
    cipher_second = encrypt(second, key=7, mode="ctr", nonce=1)
    return {"xor of the ciphertexts": [a ^ b for a, b in zip(cipher_first,
                                                             cipher_second)],
            "xor of the plaintexts": [a ^ b for a, b in zip(first, second)],
            "rule": "a counter value is used once per key"}


def parallelism():
    """Nennt, welche Betriebsart sich nebenläufig ausführen lässt."""
    return {"ecb": {"encrypt": "parallel", "decrypt": "parallel"},
            "cbc": {"encrypt": "sequential", "decrypt": "parallel"},
            "ctr": {"encrypt": "parallel", "decrypt": "parallel"},
            "note": "cbc encryption needs the previous ciphertext block"}


def none_of_them_authenticates():
    """Hält fest, was allen drei Betriebsarten fehlt.

    Keine von ihnen sagt, ob der Geheimtext unterwegs verändert wurde. Wer
    beides will, nimmt eine Betriebsart mit eingebauter Prüfung oder setzt
    einen Nachrichtenauthentisierungskode dahinter.
    """
    return {"confidentiality": True, "integrity": False,
            "answer": "authenticated encryption, for example gcm",
            "the common mistake": "encrypt then forget to authenticate"}
