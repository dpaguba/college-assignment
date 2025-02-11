"""Stromchiffren: ein Schlüsselstrom, der auf den Klartext gelegt wird."""

import hashlib
import hmac


def keystream(seed, length, modulus=256, multiplier=37, increment=17):
    """Erzeugt einen Schlüsselstrom mit einem linearen Generator.

    Der Generator ist absichtlich einfach: er zeigt, was eine Stromchiffre
    tut, und zugleich, warum ein linearer Generator dafür untauglich ist.

    Args:
        seed: Startwert.
        length: Zahl der erzeugten Werte.
        modulus, multiplier, increment: Parameter des Generators.

    Returns:
        Liste der Werte.

    Raises:
        ValueError: bei einer negativen Länge.
    """
    if length < 0:
        raise ValueError("negative Laenge")
    values = []
    state = seed % modulus
    for _ in range(length):
        state = (multiplier * state + increment) % modulus
        values.append(state)
    return values


def apply(data, stream):
    """Verknüpft Daten und Schlüsselstrom bitweise.

    Wie beim Einmalblatt sind Verschlüsseln und Entschlüsseln dieselbe
    Operation.

    Raises:
        ValueError: wenn der Strom kürzer ist als die Daten.
    """
    if len(stream) < len(data):
        raise ValueError("der Strom ist kuerzer als die Daten")
    return [value ^ stream[index] for index, value in enumerate(data)]


def period(modulus, multiplier, increment, seed):
    """Bestimmt die Periode eines linearen Generators.

    Die Periode begrenzt, wie viel unter einem Schlüssel verschlüsselt
    werden darf: danach wiederholt sich der Strom, und ein wiederholter
    Strom ist ein wiederholtes Einmalblatt.

    Raises:
        ValueError: bei einem nicht positiven Modul.
    """
    if modulus < 1:
        raise ValueError("Modul muss positiv sein")
    state = seed % modulus
    seen = {}
    steps = 0
    while state not in seen:
        seen[state] = steps
        state = (multiplier * state + increment) % modulus
        steps += 1
    return steps - seen[state]


def recover_parameters(observed, modulus):
    """Sucht die Parameter eines linearen Generators aus seiner Ausgabe.

    Gesucht werden alle Paare aus Faktor und Summand, die die beobachtete
    Folge erzeugen. Für einen kleinen Modul genügt das vollständige
    Durchprobieren; bleibt mehr als ein Paar übrig, so reichen die
    beobachteten Werte noch nicht aus, um den Generator festzulegen.

    Args:
        observed: mindestens drei aufeinanderfolgende Werte.
        modulus: der bekannte Modul.

    Returns:
        Liste der passenden Paare als Abbildungen.

    Raises:
        ValueError: bei weniger als drei Werten.
    """
    if len(observed) < 3:
        raise ValueError("mindestens drei Werte noetig")
    found = []
    for multiplier in range(modulus):
        for increment in range(modulus):
            state = observed[0]
            fits = True
            for expected in observed[1:]:
                state = (multiplier * state + increment) % modulus
                if state != expected:
                    fits = False
                    break
            if fits:
                found.append({"multiplier": multiplier,
                              "increment": increment})
    return found


def _continue_from(state, parameters, count, modulus):
    """Setzt die Folge mit den gefundenen Parametern fort."""
    values = []
    for _ in range(count):
        state = (parameters["multiplier"] * state
                 + parameters["increment"]) % modulus
        values.append(state)
    return values


def linear_generator_is_broken(modulus=256, multiplier=37, increment=17,
                               seed=5, known=8, total=24):
    """Zeigt, dass wenige bekannte Werte den ganzen Strom preisgeben.

    Ein linearer Generator ist durch wenige aufeinanderfolgende Werte
    festgelegt. Wer ein Stück Klartext kennt, rechnet daraus den Strom an
    dieser Stelle aus, bestimmt die Parameter und erzeugt den Rest selbst.
    Genau das macht ihn für eine Stromchiffre untauglich: die Chiffre ist
    gebrochen, sobald ein einziges Stück Klartext bekannt ist.

    Returns:
        Abbildung mit dem Befund, den gefundenen Parametern und der Zahl
        der Paare, die zu den beobachteten Werten passen.
    """
    stream = keystream(seed, total, modulus, multiplier, increment)
    candidates = recover_parameters(stream[:known], modulus)
    rest = stream[known:]
    for parameters in candidates:
        predicted = _continue_from(stream[known - 1], parameters, len(rest),
                                   modulus)
        if predicted == rest:
            return {"predicted the rest": True, "parameters": parameters,
                    "candidates": len(candidates), "values needed": known,
                    "values predicted": len(rest)}
    return {"predicted the rest": False, "parameters": None,
            "candidates": len(candidates), "values needed": known,
            "values predicted": len(rest)}


def bit_flipping(authenticated=False):
    """Zeigt, dass eine Stromchiffre keine Unversehrtheit verspricht.

    Der Geheimtext ist der Klartext mit dem Strom verknüpft. Wer ein Bit
    des Geheimtexts umdreht, dreht dasselbe Bit des Klartexts um, ohne den
    Schlüssel zu kennen. Kennt der Angreifer den Aufbau der Nachricht, so
    ändert er sie gezielt.

    Args:
        authenticated: ob ein Nachrichtenauthentisierungskode angehängt ist.

    Returns:
        Abbildung mit dem Befund.
    """
    plaintext = list(b"transfer 10 euro")
    stream = keystream(9, len(plaintext))
    cipher = apply(plaintext, stream)
    secret = b"mac key"
    tag = hmac.new(secret, bytes(cipher), hashlib.sha256).digest() \
        if authenticated else None
    position = plaintext.index(ord("1"))
    tampered = list(cipher)
    tampered[position] ^= ord("1") ^ ord("9")
    received = apply(tampered, stream)
    changed = bytes(received)
    detected = False
    if authenticated:
        expected = hmac.new(secret, bytes(tampered), hashlib.sha256).digest()
        detected = not hmac.compare_digest(expected, tag)
    return {"original": bytes(plaintext).decode(),
            "received": changed.decode(errors="replace"),
            "flip succeeded": changed != bytes(plaintext),
            "detected": detected,
            "key needed for the flip": False}


def against_block_ciphers():
    """Stellt Strom- und Blockchiffren gegenüber."""
    return {"stream": "one symbol at a time, no padding, an error stays "
                      "local, the keystream must never repeat",
            "block": "a fixed group at a time, needs padding unless a "
                     "stream mode is used",
            "in practice": "a block cipher in counter mode is a stream "
                           "cipher"}


def rules():
    """Nennt die Regeln, ohne die eine Stromchiffre nichts wert ist."""
    return ["never use the same keystream twice",
            "use a generator that cannot be predicted from its output",
            "add an authentication tag, the cipher gives no integrity",
            "make the nonce part of the state, not only the key"]
