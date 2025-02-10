"""Das Einmalblatt: die einzige beweisbar perfekte Verschlüsselung."""

import random

EXAM_MESSAGES = {
    "001": "0010110100001000",
    "002": "01111101100001",
    "003": "00101110000001",
    "004": "0101011011001101",
    "005": "0000101110110110",
    "006": "11110110101101",
    "007": "0010110110111010",
}

OWN_EXAM = "007"


def random_key(length, seed=None):
    """Erzeugt eine Schlüsselfolge aus einzelnen Bits.

    Für ein echtes Einmalblatt muss die Folge zufällig sein; der Startwert
    dient hier nur der Wiederholbarkeit im Test und ist genau das, was ein
    Einmalblatt nicht haben darf.

    Args:
        length: Zahl der Bits.
        seed: Startwert des Generators.

    Returns:
        Liste von Bits.

    Raises:
        ValueError: bei einer negativen Länge.
    """
    if length < 0:
        raise ValueError("negative Laenge")
    generator = random.Random(seed)
    return [generator.getrandbits(1) for _ in range(length)]


def apply(bits, key):
    """Verknüpft Nachricht und Schlüssel bitweise.

    Verschlüsseln und Entschlüsseln sind dieselbe Operation, weil das
    ausschliessende Oder zu sich selbst invers ist.

    Raises:
        ValueError: wenn der Schlüssel kürzer ist als die Nachricht.
    """
    if len(key) < len(bits):
        raise ValueError("der Schluessel ist kuerzer als die Nachricht")
    return [bit ^ key[index] for index, bit in enumerate(bits)]


def perfect_secrecy(length=4):
    """Zählt, welche Klartexte zu einem Geheimtext passen können.

    Zu jedem Geheimtext gibt es für jeden denkbaren Klartext genau einen
    Schlüssel, der ihn erzeugt. Der Geheimtext schliesst daher keinen
    Klartext aus, gleich wie viel Rechenzeit ein Angreifer hat.

    Returns:
        Abbildung mit der Zahl der möglichen Klartexte und der Zahl aller
        Klartexte dieser Länge.
    """
    ciphertext = [1, 0, 1, 1][:length]
    possible = set()
    for number in range(1 << length):
        candidate = [(number >> position) & 1 for position in range(length)]
        key = [a ^ b for a, b in zip(candidate, ciphertext)]
        if apply(candidate, key) == ciphertext:
            possible.add(tuple(candidate))
    return {"possible plaintexts": len(possible),
            "all plaintexts of that length": 1 << length,
            "meaning": "the ciphertext rules nothing out"}


def key_reuse():
    """Zeigt, was zwei Nachrichten unter demselben Schlüssel verraten.

    Werden zwei Klartexte mit demselben Schlüssel verknüpft, so hebt das
    ausschliessende Oder der beiden Geheimtexte den Schlüssel auf und
    lässt genau das ausschliessende Oder der Klartexte übrig. Die
    Verschlüsselung ist damit weg, ohne dass der Schlüssel bekannt wäre.

    Returns:
        Abbildung mit beiden Verknüpfungen, die übereinstimmen müssen.
    """
    first = [1, 0, 1, 1, 0, 0, 1, 0]
    second = [0, 0, 1, 0, 1, 1, 1, 1]
    key = random_key(len(first), seed=4)
    cipher_first = apply(first, key)
    cipher_second = apply(second, key)
    return {"xor of the ciphertexts": [a ^ b for a, b in zip(cipher_first,
                                                             cipher_second)],
            "xor of the plaintexts": [a ^ b for a, b in zip(first, second)],
            "key cancelled": True}


def seeded_generator(seed_bits=256, message_bits=100000):
    """Bewertet den Vorschlag, das Blatt aus einem Startwert zu erzeugen.

    Wird der Schlüssel aus einem 256 Bit langen Startwert berechnet, so
    gibt es nur 2 hoch 256 mögliche Schlüsselfolgen, gleich wie lang die
    Nachricht ist. Die Sicherheit hängt dann am Generator und an der Länge
    des Startwerts, nicht mehr an der Länge des Schlüssels.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"is a one time pad": False,
            "real key material": seed_bits,
            "apparent key material": message_bits,
            "security rests on": "the quality of the generator",
            "what it actually is": "a stream cipher"}


def exam_results(padded=False):
    """Wertet die abgefangenen Nachrichten aus Aufgabe 5.3c aus.

    Jede Nachricht hat ihr eigenes Einmalblatt, der Inhalt ist also nicht
    zu lesen. Die Länge verrät er trotzdem: eine bestandene Prüfung ist
    16 Bit lang, eine nicht bestandene 14. Wer die eigene Kennung und das
    eigene Ergebnis kennt, ordnet damit alle übrigen zu.

    Args:
        padded: ob alle Nachrichten vorher auf gleiche Länge gebracht
            wurden.

    Returns:
        Abbildung mit den Längen und, sofern erkennbar, den beiden Listen.
    """
    if padded:
        width = max(len(text) for text in EXAM_MESSAGES.values())
        lengths = [width] * len(EXAM_MESSAGES)
        return {"lengths": lengths, "passed": None, "failed": None,
                "leak": None,
                "prevention": "pad every plaintext to the same length"}
    own_length = len(EXAM_MESSAGES[OWN_EXAM])
    passed = sorted(name for name, text in EXAM_MESSAGES.items()
                    if len(text) == own_length)
    failed = sorted(name for name, text in EXAM_MESSAGES.items()
                    if len(text) != own_length)
    return {"lengths": [len(text) for text in EXAM_MESSAGES.values()],
            "passed": passed, "failed": failed,
            "own exam": OWN_EXAM, "own length": own_length,
            "leak": "the length of the message",
            "prevention": "pad every plaintext to the same length"}


def requirements():
    """Nennt die Bedingungen, unter denen das Blatt perfekt ist."""
    return ["the key is truly random",
            "the key is at least as long as the message",
            "the key is used exactly once",
            "the key reaches the other side over a secure channel"]


def why_it_is_rarely_used():
    """Nennt den Grund, aus dem es kaum eingesetzt wird.

    Der Schlüssel ist so lang wie die Nachricht und muss vorher sicher
    übertragen werden. Wer einen Kanal hat, über den er so viel sicher
    übertragen kann, hätte darüber auch die Nachricht schicken können.
    """
    return {"problem": "key distribution",
            "circularity": "a secure channel for the key would have carried "
                           "the message",
            "where it is used": "when the key can be exchanged long in "
                                "advance, as with diplomatic traffic"}
