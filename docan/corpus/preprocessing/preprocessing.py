"""Vorverarbeitung: Stopwords entfernen und Stemming."""

VOWELS = frozenset("aeiou")

STOPWORDS = frozenset("""
a about above after again against all am an and any are as at be because
been before being below between both but by cannot could did do does doing
down during each few for from further had has have having he her here hers
herself him himself his how i if in into is it its itself me more most my
myself no nor not of off on once only or other ought our ours ourselves out
over own same she should so some such than that the their theirs them
themselves then there these they this those through to too under until up
very was we were what when where which while who whom why with would you
your yours yourself yourselves
""".split())

_STEP2 = (("ational", "ate"), ("tional", "tion"), ("enci", "ence"),
          ("anci", "ance"), ("izer", "ize"), ("abli", "able"),
          ("alli", "al"), ("entli", "ent"), ("eli", "e"),
          ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"),
          ("ator", "ate"), ("alism", "al"), ("iveness", "ive"),
          ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"),
          ("iviti", "ive"), ("biliti", "ble"))

_STEP3 = (("icate", "ic"), ("ative", ""), ("alize", "al"),
          ("iciti", "ic"), ("ical", "ic"), ("ful", ""), ("ness", ""))

_STEP4 = ("al", "ance", "ence", "er", "ic", "able", "ible", "ant",
          "ement", "ment", "ent", "ion", "ou", "ism", "ate", "iti",
          "ous", "ive", "ize")


def remove_stopwords(words, stopwords=None):
    """Entfernt die Wörter ohne semantischen Gehalt.

    Args:
        words: die Wortliste.
        stopwords: die Liste der zu entfernenden Wörter.

    Returns:
        Die Liste ohne Stopwords.
    """
    stopwords = STOPWORDS if stopwords is None else stopwords
    return [word for word in words if word.lower() not in stopwords]


def _is_consonant(word, index):
    """Sagt, ob der Buchstabe an dieser Stelle ein Konsonant ist.

    Ein y ist ein Konsonant, wenn davor ein Vokal steht oder wenn es das
    erste Zeichen ist, und sonst ein Vokal. Deshalb lässt sich die Frage
    nicht am einzelnen Buchstaben entscheiden.
    """
    letter = word[index]
    if letter in VOWELS:
        return False
    if letter != "y":
        return True
    return index == 0 or not _is_consonant(word, index - 1)


def _pattern(word):
    """Übersetzt ein Wort in seine Folge aus c und v."""
    return "".join("c" if _is_consonant(word, index) else "v"
                   for index in range(len(word)))


def measure(stem):
    """Zählt die Silbenmasse m eines Stamms.

    Jedes Wort hat die Form [C](VC)^m[V]; m ist die Anzahl der
    VC-Gruppen. Die Bedingungen der späteren Schritte hängen daran: ein
    kurzes Wort verliert keine Endung, ein langes schon.

    Returns:
        Die Zahl m.
    """
    pattern = _pattern(stem)
    trimmed = pattern.lstrip("c")
    return trimmed.count("vc")


def _has_vowel(stem):
    """Sagt, ob der Stamm einen Vokal enthält."""
    return "v" in _pattern(stem)


def _ends_double_consonant(stem):
    """Sagt, ob der Stamm auf einen doppelten Konsonanten endet."""
    if len(stem) < 2 or stem[-1] != stem[-2]:
        return False
    return _is_consonant(stem, len(stem) - 1)


def _ends_cvc(stem):
    """Sagt, ob der Stamm auf Konsonant, Vokal, Konsonant endet.

    Der letzte Konsonant darf kein w, x oder y sein. Das ist die
    Bedingung, an der sich entscheidet, ob ein e wieder angehängt wird:
    aus fil wird file, aus fail nicht faile.
    """
    if len(stem) < 3:
        return False
    if not (_is_consonant(stem, len(stem) - 3)
            and not _is_consonant(stem, len(stem) - 2)
            and _is_consonant(stem, len(stem) - 1)):
        return False
    return stem[-1] not in "wxy"


def _step1a(word):
    """Behandelt die Pluralendungen."""
    if word.endswith("sses"):
        return word[:-2]
    if word.endswith("ies"):
        return word[:-2]
    if word.endswith("ss"):
        return word
    if word.endswith("s"):
        return word[:-1]
    return word


def _step1b2(stem):
    """Repariert den Stamm nach dem Entfernen von ed oder ing."""
    for suffix in ("at", "bl", "iz"):
        if stem.endswith(suffix):
            return stem + "e"
    if _ends_double_consonant(stem) and stem[-1] not in "lsz":
        return stem[:-1]
    if measure(stem) == 1 and _ends_cvc(stem):
        return stem + "e"
    return stem


def _step1b(word):
    """Behandelt die Endungen eed, ed und ing.

    Es greift genau eine Regel, nämlich die mit der längsten passenden
    Endung. Trifft deren Bedingung nicht zu, bleibt das Wort in diesem
    Schritt unverändert; es wird keine kürzere Endung nachgeschoben.
    Daraus folgt feed zu feed und agreed zu agree.
    """
    if word.endswith("eed"):
        return word[:-1] if measure(word[:-3]) > 0 else word
    for suffix in ("ed", "ing"):
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            return _step1b2(stem) if _has_vowel(stem) else word
    return word


def _step1c(word):
    """Ersetzt ein abschliessendes y durch i."""
    if word.endswith("y") and _has_vowel(word[:-1]):
        return word[:-1] + "i"
    return word


def _replace_longest(word, rules, condition):
    """Wendet die Regel mit der längsten passenden Endung an."""
    best = None
    for suffix, replacement in rules:
        if word.endswith(suffix) and (best is None
                                      or len(suffix) > len(best[0])):
            best = (suffix, replacement)
    if best is None:
        return word
    suffix, replacement = best
    stem = word[:-len(suffix)]
    return stem + replacement if condition(stem, suffix) else word


def _step4(word):
    """Entfernt die Endungen langer Stämme."""
    best = max((suffix for suffix in _STEP4 if word.endswith(suffix)),
               key=len, default=None)
    if best is None:
        return word
    stem = word[:-len(best)]
    if best == "ion" and not (stem.endswith("s") or stem.endswith("t")):
        return word
    return stem if measure(stem) > 1 else word


def _step5(word):
    """Entfernt ein überflüssiges e und einen doppelten Konsonanten."""
    if word.endswith("e"):
        stem = word[:-1]
        if measure(stem) > 1 or (measure(stem) == 1
                                 and not _ends_cvc(stem)):
            word = stem
    if (measure(word) > 1 and _ends_double_consonant(word)
            and word.endswith("l")):
        word = word[:-1]
    return word


def stem(word):
    """Führt ein Wort auf seinen Stamm zurück.

    Der Algorithmus streicht Endungen in fünf Schritten und prüft vor
    jedem Streichen, ob der Rest lang genug ist. Er kennt keine
    Wortliste und liefert deshalb Stämme, die keine Wörter sind: aus
    ponies wird poni und aus sensibiliti wird sensibl. Für die
    Suche genügt das, weil nur zählt, dass verwandte Wörter denselben
    Stamm bekommen.

    Args:
        word: das Wort in Kleinbuchstaben.

    Returns:
        Der Stamm.

    Raises:
        ValueError: bei einem leeren Wort.
    """
    if not word:
        raise ValueError("leeres Wort")
    word = word.lower()
    if len(word) <= 2:
        return word
    word = _step1c(_step1b(_step1a(word)))
    word = _replace_longest(word, _STEP2,
                            lambda stem, _: measure(stem) > 0)
    word = _replace_longest(word, _STEP3,
                            lambda stem, _: measure(stem) > 0)
    return _step5(_step4(word))


def preprocess(words, stopwords=None):
    """Entfernt die Stopwords und führt den Rest auf Stämme zurück.

    Die Reihenfolge ist nicht beliebig: erst die Stopwords, dann das
    Stemming. Umgekehrt würde aus einem Stopword ein Stamm, der in der
    Liste nicht mehr steht, und das Wort bliebe stehen.
    """
    return [stem(word) for word in remove_stopwords(words, stopwords)]


def what_it_gets_wrong():
    """Nennt beide Fehlerarten des Verfahrens an eigenen Beispielen.

    Zu viel gestemmt heisst, dass zwei Wörter verschiedener Bedeutung
    denselben Stamm bekommen; zu wenig gestemmt heisst, dass zwei Formen
    desselben Worts verschiedene Stämme behalten. Beides folgt daraus,
    dass der Algorithmus nur Endungen sieht und keine Bedeutung.

    Der zweite Fall trifft auch Formen, die der Algorithmus eigentlich
    zusammenführen sollte: relative wird zu rel und relate zu relat, weil
    die eine Endung in Schritt vier fällt und die andere schon in
    Schritt zwei ersetzt wurde.

    Returns:
        Abbildung mit Paaren zu beiden Fehlerarten.
    """
    return {"over": [("general", "generous"), ("news", "new"),
                     ("experiment", "experience")],
            "under": [("relative", "relate"), ("mouse", "mice"),
                      ("run", "ran")],
            "why": "der Algorithmus sieht Endungen und keine Bedeutung",
            "when it is enough": "wenn nur zählt, dass verwandte Formen "
                                 "denselben Stamm bekommen"}
