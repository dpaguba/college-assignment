"""Die Caesar-Verschiebung und wie klein ihr Schlüsselraum ist."""

CIPHERTEXT = ("N pelcgbtencuvp flfgrz fubhyq or frpher rira vs rirelguvat "
              "nobhg gur flfgrz, rkprcg gur xrl, vf choyvp xabjyrqtr.")

COMMON = ("the", "and", "system", "secure", "public", "key", "should")


def shift(text, key):
    """Verschiebt jeden Buchstaben um den Schlüssel.

    Gross- und Kleinschreibung bleiben erhalten, alles andere ebenfalls.
    """
    result = []
    for character in text:
        if "a" <= character <= "z":
            result.append(chr((ord(character) - 97 + key) % 26 + 97))
        elif "A" <= character <= "Z":
            result.append(chr((ord(character) - 65 + key) % 26 + 65))
        else:
            result.append(character)
    return "".join(result)


def key_space():
    """Zahl der möglichen Schlüssel; das ist die ganze Schwäche."""
    return 26


def score(text):
    """Bewertet, wie englisch ein Text aussieht.

    Gezählt werden bekannte Wörter; das genügt, um aus 26 Kandidaten den
    richtigen zu wählen.
    """
    lowered = text.lower()
    return sum(lowered.count(word) for word in COMMON)


def break_by_search(text):
    """Probiert alle Schlüssel durch und wählt den lesbarsten.

    Returns:
        Abbildung mit dem Schlüssel, dem Klartext und der Zahl der
        geprüften Kandidaten.
    """
    best = None
    for key in range(26):
        candidate = shift(text, -key)
        value = score(candidate)
        if best is None or value > best[0]:
            best = (value, key, candidate)
    return {"key": best[1], "plaintext": best[2], "score": best[0],
            "candidates tried": 26}


def exercise():
    """Löst Aufgabe 5.1.

    Returns:
        Abbildung mit dem Schlüssel, dem Klartext und dem Prinzip, das er
        ausspricht.
    """
    report = break_by_search(CIPHERTEXT)
    report["principle"] = "Kerckhoffs"
    report["meaning"] = ("a cipher must stay secure when everything except "
                         "the key is public, because a secret design cannot "
                         "be reviewed and its flaws are found by the wrong "
                         "people")
    return report


def why_it_fails():
    """Nennt die Gründe, aus denen die Verschiebung nichts taugt."""
    return ["26 keys, which is a few seconds by hand",
            "the letter frequencies are only moved, not changed",
            "one known plaintext letter gives the whole key",
            "the same letter always becomes the same letter"]
