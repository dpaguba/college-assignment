"""Beobachtungstabelle des Lernverfahrens von Angluin."""


class Table:
    """Die Tabelle mit Präfixen, Suffixen und den Antworten des Orakels.

    Die Zeilen sind mit Wörtern beschriftet, die Spalten mit Suffixen; in
    jeder Zelle steht die Antwort auf die Frage, ob die Zusammensetzung
    zur Sprache gehört. Zwei Zeilen mit gleicher Belegung stehen für
    denselben Zustand.
    """

    def __init__(self, alphabet, membership):
        """Legt eine Tabelle mit dem leeren Wort in beiden Mengen an.

        Args:
            alphabet: die Buchstaben der Sprache.
            membership: das Orakel, das ein Wort beurteilt.

        Raises:
            ValueError: bei einem leeren Alphabet.
        """
        if not alphabet:
            raise ValueError("leeres Alphabet")
        self.alphabet = tuple(alphabet)
        self.membership = membership
        self.prefixes = [""]
        self.suffixes = [""]
        self.answers = {}
        self.queries = 0

    def ask(self, word):
        """Fragt das Orakel und merkt sich die Antwort.

        Jedes Wort wird nur einmal gefragt; die Zahl der Fragen ist das
        Mass, an dem sich das Verfahren messen lässt.
        """
        if word not in self.answers:
            self.answers[word] = bool(self.membership(word))
            self.queries += 1
        return self.answers[word]

    def row(self, prefix):
        """Liefert die Belegung einer Zeile als Tupel."""
        return tuple(self.ask(prefix + suffix) for suffix in self.suffixes)

    def extensions(self):
        """Nennt die Zeilen, die um einen Buchstaben verlängert sind."""
        found = []
        for prefix in self.prefixes:
            for letter in self.alphabet:
                word = prefix + letter
                if word not in self.prefixes:
                    found.append(word)
        return found

    def add_prefix(self, word):
        """Nimmt ein Wort in die Menge der Zeilen auf."""
        if word not in self.prefixes:
            self.prefixes.append(word)

    def add_suffix(self, word):
        """Nimmt ein Wort in die Menge der Spalten auf."""
        if word not in self.suffixes:
            self.suffixes.append(word)

    def unclosed(self):
        """Sucht eine verlängerte Zeile ohne Entsprechung unter den Zeilen.

        Die Tabelle heisst abgeschlossen, wenn jede Verlängerung wie eine
        der bestehenden Zeilen aussieht. Fehlt eine, so ist ein Zustand
        entdeckt worden, der noch keinen Namen hat.

        Returns:
            Das fehlende Wort oder None.
        """
        known = {self.row(prefix) for prefix in self.prefixes}
        for word in self.extensions():
            if self.row(word) not in known:
                return word
        return None

    def inconsistent(self):
        """Sucht zwei gleiche Zeilen, deren Verlängerungen sich unterscheiden.

        Sehen zwei Zeilen gleich aus, müssen auch ihre Verlängerungen
        gleich aussehen; sonst fehlt eine Spalte, die sie unterscheidet.

        Returns:
            Das fehlende Suffix oder None.
        """
        for first in self.prefixes:
            for second in self.prefixes:
                if first >= second:
                    continue
                if self.row(first) != self.row(second):
                    continue
                for letter in self.alphabet:
                    left = self.row(first + letter)
                    right = self.row(second + letter)
                    if left != right:
                        for index, (a, b) in enumerate(zip(left, right)):
                            if a != b:
                                return letter + self.suffixes[index]
        return None

    def make_closed_and_consistent(self):
        """Ergänzt Zeilen und Spalten, bis beide Bedingungen gelten."""
        while True:
            missing = self.unclosed()
            if missing is not None:
                self.add_prefix(missing)
                continue
            suffix = self.inconsistent()
            if suffix is not None:
                self.add_suffix(suffix)
                continue
            return

    def hypothesis(self):
        """Baut den Automaten, den die Tabelle beschreibt.

        Ein Zustand ist eine Zeilenbelegung, der Startzustand die Zeile des
        leeren Wortes, und ein Zustand ist akzeptierend, wenn die Antwort
        auf das leere Suffix wahr ist.

        Returns:
            Abbildung mit ``states``, ``start``, ``accepting``,
            ``transitions`` und ``alphabet``.

        Raises:
            ValueError: wenn die Tabelle nicht abgeschlossen ist.
        """
        if self.unclosed() is not None:
            raise ValueError("die Tabelle ist nicht abgeschlossen")
        names = {}
        representatives = {}
        for prefix in self.prefixes:
            signature = self.row(prefix)
            if signature not in names:
                names[signature] = len(names)
                representatives[signature] = prefix
        transitions = {}
        for signature, state in names.items():
            prefix = representatives[signature]
            for letter in self.alphabet:
                target = self.row(prefix + letter)
                if target not in names:
                    raise ValueError("die Tabelle ist nicht abgeschlossen")
                transitions[(state, letter)] = names[target]
        accepting = {state for signature, state in names.items()
                     if signature[0]}
        return {"states": sorted(names.values()), "start": names[self.row("")],
                "accepting": accepting, "transitions": transitions,
                "alphabet": self.alphabet}

    def as_text(self):
        """Stellt die Tabelle als Text dar, für einen Blick von aussen."""
        lines = ["".ljust(8) + " ".join(suffix or "e"
                                        for suffix in self.suffixes)]
        for prefix in self.prefixes:
            marks = " ".join("1" if value else "0"
                             for value in self.row(prefix))
            lines.append((prefix or "e").ljust(8) + marks)
        return "\n".join(lines)
