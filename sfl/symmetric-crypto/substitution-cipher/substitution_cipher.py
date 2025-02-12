"""Die monoalphabetische Substitution und ihr Bruch durch Statistik."""

import math
import random
import string

ALPHABET = string.ascii_lowercase

CIPHERTEXT = (
    "hun cninxh znlnybqgnxh bw lscrbjd gnhubzd bw gbzjyshrbx djiu sd qig sxz "
    "qqg turiu nfiusxkn asxztrzhu wbc drkxsy-hb-xbrdn cshrb usd rxhnxdrwrnz "
    "hun rxhncndh rx s knxncsy hunbcv bw ibggjxrishrbx. s asdrd wbc djiu s "
    "hunbcv rd ibxhsrxnz rx hun rgqbchsxh qsqncd bw xvejrdh1 sxz uschynv2 bx "
    "hurd djapnih. rx hun qcndnxh qsqnc tn tryy nfhnxz hun hunbcv hb rxiyjzn "
    "s xjganc bw xnt wsihbcd, rx qschrijysc hun nwwnih bw xbrdn rx hun "
    "iusxxny, sxz hun dslrxkd qbddrayn zjn hb hun dhshrdhrisy dhcjihjcn bw "
    "hun bcrkrxsy gnddskn sxz zjn hb hun xshjcn bw hun wrxsy zndhrxshrbx bw "
    "hun rxwbcgshrbx. hun wjxzsgnxhsy qcbayng bw ibggjxrishrbx rd hush bw "
    "cnqcbzjirxk sh bxn qbrxh nrhunc nfsihyv bc sqqcbfrgshnyv s gnddskn "
    "dnynihnz sh sxbhunc qbrxh. wcnejnxhyv hun gnddsknd usln gnsxrxk; hush "
    "rd hunv cnwnc hb bc scn ibccnyshnz siibczrxk hb dbgn dvdhng trhu "
    "inchsrx quvdrisy bc ibxinqhjsy nxhrhrnd. hundn dngsxhri sdqnihd bw "
    "ibggjxrishrbx scn rccnynlsxh hb hun nxkrxnncrxk qcbayng. hun "
    "drkxrwrisxh sdqnih rd hush hun sihjsy gnddskn rd bxn dnynihnz wcbg s "
    "dnh bw qbddrayn gnddsknd. hun dvdhng gjdh an zndrkxnz hb bqncshn wbc "
    "nsiu qbddrayn dnynihrbx, xbh pjdh hun bxn turiu tryy sihjsyyv an "
    "iubdnx drxin hurd rd jxoxbtx sh hun hrgn bw zndrkx. rw hun xjganc bw "
    "gnddsknd rx hun dnh rd wrxrhn hunx hurd xjganc bc sxv gbxbhbxri "
    "wjxihrbx bw hurd xjganc isx an cnkscznz sd s gnsdjcn bw hun "
    "rxwbcgshrbx qcbzjinz tunx bxn gnddskn rd iubdnx wcbg hun dnh, syy "
    "iubrind anrxk nejsyyv yronyv. sd tsd qbrxhnz bjh av uschynv hun gbdh "
    "xshjcsy iubrin rd hun ybkscrhugri wjxihrbx. syhubjku hurd znwrxrhrbx "
    "gjdh an knxncsyrmnz ibxdrzncsayv tunx tn ibxdrznc hun rxwyjnxin bw "
    "hun dhshrdhrid bw hun gnddskn sxz tunx tn usln s ibxhrxjbjd csxkn bw "
    "gnddsknd, tn tryy rx syy isdnd jdn sx nddnxhrsyyv ybkscrhugri gnsdjcn.")

ENGLISH_FREQUENCY = {
    "a": 8.17, "b": 1.49, "c": 2.78, "d": 4.25, "e": 12.70, "f": 2.23,
    "g": 2.02, "h": 6.09, "i": 6.97, "j": 0.15, "k": 0.77, "l": 4.03,
    "m": 2.41, "n": 6.75, "o": 7.51, "p": 1.93, "q": 0.10, "r": 5.99,
    "s": 6.33, "t": 9.06, "u": 2.76, "v": 0.98, "w": 2.36, "x": 0.15,
    "y": 1.97, "z": 0.07,
}

REFERENCE = (
    "the recent development of various methods of modulation such as pcm and "
    "ppm which exchange bandwidth for signal to noise ratio has intensified "
    "the interest in a general theory of communication a basis for such a "
    "theory is contained in the important papers of nyquist and hartley on "
    "this subject in the present paper we will extend the theory to include "
    "a number of new factors in particular the effect of noise in the "
    "channel and the savings possible due to the statistical structure of "
    "the original message and due to the nature of the final destination of "
    "the information the fundamental problem of communication is that of "
    "reproducing at one point either exactly or approximately a message "
    "selected at another point frequently the messages have meaning that is "
    "they refer to or are correlated according to some system with certain "
    "physical or conceptual entities these semantic aspects of communication "
    "are irrelevant to the engineering problem the significant aspect is "
    "that the actual message is one selected from a set of possible messages "
    "the system must be designed to operate for each possible selection not "
    "just the one which will actually be chosen since this is unknown at the "
    "time of design if the number of messages in the set is finite then this "
    "number or any monotonic function of this number can be regarded as a "
    "measure of the information produced when one message is chosen from the "
    "set all choices being equally likely as was pointed out by hartley the "
    "most natural choice is the logarithmic function")

CORPUS = (
    "the weather turned cold in the middle of the week and the children who "
    "had been playing in the garden every afternoon came inside to sit by "
    "the fire and read their books until it was time for supper the older "
    "boy asked his mother whether they could go to the market in the morning "
    "because he wanted to buy a present for his sister whose birthday would "
    "be on the following sunday she said that they would see how the roads "
    "looked after the rain had stopped and that if the bus was running they "
    "would take the early one and be back before the middle of the day the "
    "next morning the sky was clear and the air was still and they walked "
    "down the hill to the corner where the bus stopped and waited with the "
    "other people who were going into town when the bus came it was already "
    "half full and they had to stand for the first part of the journey but "
    "after a while two seats became free near the front and they sat there "
    "and watched the fields go past the market was busier than they had "
    "expected and it took some time to find the stall that sold the small "
    "wooden animals that his sister liked so much he chose a horse with a "
    "long tail and the woman behind the table wrapped it in brown paper and "
    "tied it with a piece of string while his mother bought bread and cheese "
    "and a bag of apples for the week on the way home they talked about what "
    "they would do during the holidays and whether there would be enough "
    "money to visit their grandmother who lived on the coast and whom they "
    "had not seen since the summer before last when the train had broken "
    "down and they had spent most of a day waiting at a small station with "
    "nothing to do but count the birds on the wires above the platform his "
    "mother said that she would write a letter that evening and ask whether "
    "it would be convenient for them to come and stay for a week or two and "
    "that they should not expect an answer before the end of the month "
    "because letters took a long time to reach that part of the country and "
    "his grandmother was not in the habit of writing quickly when they got "
    "home the fire had gone out and the house was cold so the boy went to "
    "fetch more wood from the shed behind the kitchen while his sister laid "
    "the table and their mother put the kettle on and for a long while "
    "nobody said anything at all which was the way most of their evenings "
    "began and ended in that house by the hill")

COMMON_WORDS = (
    "the", "of", "and", "to", "in", "is", "that", "it", "for", "as", "with",
    "was", "on", "be", "by", "this", "are", "from", "or", "an", "but", "not",
    "they", "which", "one", "you", "all", "were", "when", "we", "there",
    "can", "has", "more", "if", "no", "out", "up", "into", "than", "them",
    "only", "other", "new", "some", "could", "time", "these", "two", "may",
    "then", "do", "first", "any", "would", "each", "make", "like", "him",
    "over", "such", "most", "even", "also", "after", "many", "must",
    "through", "back", "where", "much", "before", "same", "right", "those",
    "both", "under", "while", "should", "being", "between", "number",
    "have", "will", "their", "what", "about", "its", "our", "so", "at",
    "one", "point", "used", "way", "case", "form", "given", "set")

_KNOWN_WORDS = frozenset(COMMON_WORDS)


def random_key(seed=0):
    """Erzeugt eine zufällige Zuordnung der Buchstaben."""
    letters = list(ALPHABET)
    random.Random(seed).shuffle(letters)
    return dict(zip(ALPHABET, letters))


def encrypt(text, key):
    """Wendet die Zuordnung an; alles ausser Buchstaben bleibt stehen."""
    return "".join(key.get(character, character) for character in text)


def decrypt(text, key):
    """Kehrt die Zuordnung um."""
    inverse = {value: name for name, value in key.items()}
    return "".join(inverse.get(character, character) for character in text)


def key_space():
    """Zahl der möglichen Zuordnungen: sechsundzwanzig Fakultät."""
    return math.factorial(26)


def frequencies(text):
    """Zählt die Buchstaben eines Textes in Prozent.

    Raises:
        ValueError: wenn der Text keine Buchstaben enthält.
    """
    letters = [character for character in text.lower()
               if character in ALPHABET]
    if not letters:
        raise ValueError("keine Buchstaben im Text")
    counts = {letter: 0 for letter in ALPHABET}
    for letter in letters:
        counts[letter] += 1
    return {letter: 100.0 * count / len(letters)
            for letter, count in counts.items()}


def frequencies_are_preserved():
    """Prüft, dass die Verschlüsselung die Häufigkeiten nur umbenennt.

    Die Zuordnung ist eine Umbenennung der Buchstaben; die Liste der
    Häufigkeiten bleibt daher dieselbe, nur die Beschriftung ändert sich.
    Daran hängt der ganze Angriff.

    Returns:
        Abbildung mit dem Befund.
    """
    text = "the quick brown fox jumps over the lazy dog " * 20
    key = random_key(seed=3)
    before = sorted(round(value, 6) for value in frequencies(text).values())
    after = sorted(round(value, 6)
                   for value in frequencies(encrypt(text, key)).values())
    return {"same multiset": before == after, "letters renamed": True}


def _clean(text):
    """Behält nur die Buchstaben eines Textes."""
    return "".join(character for character in text.lower()
                   if character in ALPHABET)


def _build_table(sample, order, smoothing=0.01):
    """Baut eine Häufigkeitstabelle der Buchstabengruppen einer Länge.

    Der Wert einer Gruppe ist der Logarithmus ihrer geglätteten
    Häufigkeit. Die Glättung sorgt dafür, dass eine im Beispieltext nicht
    vorkommende Gruppe einen festen, aber nicht beliebig schlechten Wert
    bekommt; ohne sie stünde neben jedem beobachteten Wert eine Klippe.

    Args:
        sample: der Beispieltext.
        order: Länge der Gruppen.
        smoothing: der Zähler einer ungesehenen Gruppe.

    Returns:
        Abbildung mit ``values`` und dem ``floor`` für Ungesehenes.

    Raises:
        ValueError: bei einer Länge unter zwei.
    """
    if order < 2:
        raise ValueError("die Gruppenlaenge muss mindestens zwei sein")
    letters = _clean(sample)
    counts = {}
    for index in range(len(letters) - order + 1):
        group = letters[index:index + order]
        counts[group] = counts.get(group, 0) + 1
    total = sum(counts.values()) + smoothing * (26 ** order)
    values = {group: math.log10((count + smoothing) / total)
              for group, count in counts.items()}
    return {"values": values, "floor": math.log10(smoothing / total),
            "order": order}


def _model(sample=None):
    """Baut das Bewertungsmodell aus Paaren und Tripeln.

    Die Paare geben ein glattes Gefälle, an dem sich das Bergsteigen
    entlanghangeln kann; die Tripel trennen die guten Zuordnungen von den
    fast guten. Der Beispieltext ist gewöhnliche englische Prosa und hat
    mit dem gesuchten Klartext nichts zu tun.
    """
    text = CORPUS if sample is None else sample
    return [_build_table(text, 2), _build_table(text, 3)]


def _score(letters, model, limit=None):
    """Bewertet einen bereits gesäuberten Text über die Tabellen."""
    if limit is not None:
        letters = letters[:limit]
    total = 0.0
    for table in model:
        order = table["order"]
        values = table["values"]
        floor = table["floor"]
        for index in range(len(letters) - order + 1):
            total += values.get(letters[index:index + order], floor)
    return total


def word_share(text):
    """Anteil der Buchstaben, die in bekannten englischen Wörtern stehen.

    Das Mass dient der Kontrolle am Ende: eine richtige Zuordnung lässt
    viele gewöhnliche Wörter entstehen, eine fast richtige kaum welche.
    """
    letters = 0
    matched = 0
    for word in text.lower().replace(",", " ").replace(".", " ").split():
        cleaned = _clean(word)
        if not cleaned:
            continue
        letters += len(cleaned)
        if cleaned in COMMON_WORDS:
            matched += len(cleaned)
    return matched / letters if letters else 0.0


def _apply(text, mapping):
    """Wendet eine Zuordnung von Geheim- auf Klarbuchstaben an.

    Übersetzt wird mit ``str.translate``, weil die Bewertung die Zuordnung
    hunderttausendfach anwendet und eine Schleife in Python dafür zu
    langsam wäre.
    """
    return text.lower().translate(str.maketrans(mapping))


def _pieces(text):
    """Zerlegt einen Text in die Wörter, die die Wortprüfung ansieht."""
    return [word for word in (_clean(part) for part in text.lower().split())
            if word]


def _word_hits(pieces, table):
    """Zählt die Buchstaben, die nach der Übersetzung in einem Wort stehen.

    Die Liste der Wörter ist eine gewöhnliche Liste englischer
    Funktionswörter und hängt nicht am gesuchten Text.
    """
    return sum(len(word) for word in (piece.translate(table)
                                      for piece in pieces)
               if word in _KNOWN_WORDS)


def break_text(ciphertext, seed=0, restarts=3, window=None, passes=30,
               weight=5.0):
    """Bricht eine Substitution durch Bergsteigen auf Buchstabengruppen.

    Der Start kommt aus dem Häufigkeitsvergleich: der häufigste
    Geheimbuchstabe wird auf den häufigsten englischen abgebildet und so
    fort. Danach wird in jedem Durchgang jedes der 325 Buchstabenpaare
    einmal vertauscht und die Vertauschung behalten, wenn der Text besser
    bewertet wird; es folgen weitere Durchgänge, bis keiner mehr etwas
    verbessert. Mehrere Neustarts mit leicht gestörtem Anfang helfen über
    lokale Maxima hinweg.

    Die Bewertung setzt sich aus den Buchstabengruppen und den erkannten
    Wörtern zusammen. Ohne den Wortanteil bleibt das Bergsteigen bei den
    seltenen Buchstaben in einem lokalen Maximum stehen: die Gruppen
    unterscheiden ``development`` und ``dekelobment`` kaum, die Wörter
    ``of`` und ``om`` dagegen sofort.

    Args:
        ciphertext: der verschlüsselte Text.
        seed: Startwert des Zufallsgenerators.
        restarts: Zahl der Neustarts.
        window: wie viel vom Text in die Bewertung eingeht; ohne Angabe
            der ganze Text.
        passes: obere Schranke der Durchgänge je Neustart.
        weight: Gewicht eines Buchstabens in einem erkannten Wort.

    Returns:
        Abbildung mit ``plaintext``, ``key``, ``score`` und ``word share``.
    """
    model = _model()
    sample = ciphertext if window is None else ciphertext[:window]
    letters = _clean(sample)
    pieces = _pieces(sample)
    observed = frequencies(ciphertext)
    by_frequency = sorted(ALPHABET, key=lambda letter: -observed[letter])
    english_order = sorted(ALPHABET,
                           key=lambda letter: -ENGLISH_FREQUENCY[letter])
    start = dict(zip(by_frequency, english_order))
    generator = random.Random(seed)
    pairs = [(first, second)
             for index, first in enumerate(ALPHABET)
             for second in ALPHABET[index + 1:]]

    def value_of(mapping):
        """Bewertet eine Zuordnung über Gruppen und erkannte Wörter."""
        table = str.maketrans(mapping)
        return (_score(letters.translate(table), model)
                + weight * _word_hits(pieces, table))

    best = None
    for restart in range(restarts):
        current = dict(start)
        if restart:
            for _ in range(restart):
                first, second = generator.sample(list(ALPHABET), 2)
                current[first], current[second] = (current[second],
                                                   current[first])
        value = value_of(current)
        for _ in range(passes):
            improved = False
            generator.shuffle(pairs)
            for first, second in pairs:
                candidate = dict(current)
                candidate[first], candidate[second] = (candidate[second],
                                                       candidate[first])
                new_value = value_of(candidate)
                if new_value > value:
                    current, value = candidate, new_value
                    improved = True
            if not improved:
                break
        if best is None or value > best[0]:
            best = (value, current)
    plaintext = _apply(ciphertext, best[1])
    return {"score": best[0], "key": best[1], "plaintext": plaintext,
            "word share": word_share(plaintext)}


def accuracy_against(plaintext, expected):
    """Misst, wie viele Buchstaben mit einem erwarteten Text übereinstimmen.

    Raises:
        ValueError: wenn der Vergleichstext keine Buchstaben enthält.
    """
    produced = _clean(plaintext)
    wanted = _clean(expected)
    if not wanted:
        raise ValueError("kein Vergleichstext")
    matched = sum(1 for a, b in zip(wanted, produced) if a == b)
    return matched / len(wanted)


_EXERCISE_RESULT = {}


def break_exercise():
    """Bricht den Text aus Aufgabe 5.2.

    Das Ergebnis wird gemerkt, weil der Bruch einige Sekunden dauert und
    mehrfach abgefragt wird.

    Returns:
        Abbildung mit dem Klartext, der Trefferquote gegen den bekannten
        Anfang und dem Verfasser.
    """
    if not _EXERCISE_RESULT:
        result = break_text(CIPHERTEXT, seed=7)
        _EXERCISE_RESULT.update({
            "plaintext": result["plaintext"], "key": result["key"],
            "word share": result["word share"],
            "accuracy": accuracy_against(result["plaintext"], REFERENCE),
            "author": "C. E. Shannon",
            "work": "A Mathematical Theory of Communication, 1948"})
    return dict(_EXERCISE_RESULT)


def length_matters():
    """Misst, wie die Textlänge den Bruch beeinflusst.

    Ein kurzer Text liefert zu wenige Buchstabengruppen, als dass die
    Statistik entscheiden könnte; ein langer entscheidet sie eindeutig.

    Returns:
        Abbildung mit der Trefferquote für einen kurzen und einen langen
        Ausschnitt.
    """
    key = random_key(seed=11)
    scores = {}
    for name, text in (("short", REFERENCE[:50]), ("long", REFERENCE)):
        recovered = break_text(encrypt(text, key), seed=3,
                               restarts=3)["plaintext"]
        scores[name] = accuracy_against(recovered, text)
    scores["short letters"] = len(_clean(REFERENCE[:50]))
    scores["long letters"] = len(_clean(REFERENCE))
    return scores


def why_it_breaks():
    """Nennt, was die Substitution verrät."""
    return ["the letter frequencies are renamed, not changed",
            "so are the frequencies of pairs and of quadruples",
            "word lengths and repeated patterns survive",
            "a single guessed word fixes several letters at once",
            "the key space is huge and irrelevant: 26 factorial keys do not "
            "help when the statistics point at one of them"]
