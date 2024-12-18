"""Kontrollfluss: Aufruf, Rücksprung und die bedingten Sprünge."""

CONDITIONS = {
    "je": lambda flags: flags.get("ZF", 0) == 1,
    "jz": lambda flags: flags.get("ZF", 0) == 1,
    "jne": lambda flags: flags.get("ZF", 0) == 0,
    "jnz": lambda flags: flags.get("ZF", 0) == 0,
    "jb": lambda flags: flags.get("CF", 0) == 1,
    "jnae": lambda flags: flags.get("CF", 0) == 1,
    "jae": lambda flags: flags.get("CF", 0) == 0,
    "jnb": lambda flags: flags.get("CF", 0) == 0,
    "jl": lambda flags: flags.get("SF", 0) != flags.get("OF", 0),
    "jnge": lambda flags: flags.get("SF", 0) != flags.get("OF", 0),
    "jge": lambda flags: flags.get("SF", 0) == flags.get("OF", 0),
    "js": lambda flags: flags.get("SF", 0) == 1,
    "jns": lambda flags: flags.get("SF", 0) == 0,
    "jo": lambda flags: flags.get("OF", 0) == 1,
}


def taken(jump, flags):
    """Sagt, ob ein bedingter Sprung genommen wird.

    Raises:
        ValueError: bei einem unbekannten Sprungbefehl.
    """
    if jump not in CONDITIONS:
        raise ValueError("unbekannter Sprungbefehl")
    return CONDITIONS[jump](flags)


def equivalent(first, second):
    """Prüft, ob zwei Sprungbefehle dieselbe Bedingung prüfen.

    Verglichen wird über alle Flagbelegungen; zwei Namen sind gleich,
    wenn sie sich nirgends unterscheiden.
    """
    for zero in (0, 1):
        for carry in (0, 1):
            for sign in (0, 1):
                for overflow in (0, 1):
                    flags = {"ZF": zero, "CF": carry, "SF": sign,
                             "OF": overflow}
                    if taken(first, flags) != taken(second, flags):
                        return False
    return True


class Machine:
    """Ein Modell, das den Befehlszeiger einer Folge nachvollzieht.

    Die Zeilennummern gelten als Adressen, wie es die Übung vereinfacht.
    """

    def __init__(self, lines):
        """Legt die Maschine über einer Befehlsfolge an."""
        self.lines = list(lines)
        self.labels = {}
        for index, line in enumerate(self.lines, start=1):
            text = line.strip()
            if text.endswith(":"):
                self.labels[text[:-1].strip()] = index + 1
        self.stack = []

    def address_of(self, instruction):
        """Nennt die Adresse eines Befehls.

        Raises:
            ValueError: wenn der Befehl nicht vorkommt.
        """
        for index, line in enumerate(self.lines, start=1):
            if line.strip() == instruction.strip():
                return index
        raise ValueError("Befehl kommt nicht vor: %s" % instruction)

    def rip_after(self, instruction):
        """Bestimmt den Befehlszeiger nach der Ausführung eines Befehls.

        Ein gewöhnlicher Befehl geht zur nächsten Adresse. Ein Aufruf legt
        die Rückkehradresse ab und springt zum Ziel. Ein Rücksprung holt
        sie zurück. Ein unbedingter Sprung geht zu seinem Ziel.
        """
        address = self.address_of(instruction)
        text = instruction.strip()
        if text.startswith("call "):
            target = text.split(None, 1)[1].strip()
            self.stack.append(address + 1)
            return self.labels.get(target, int(target)
                                   if target.isdigit() else address + 1)
        if text.startswith("jmp "):
            target = text.split(None, 1)[1].strip()
            return self.labels.get(target, int(target)
                                   if target.isdigit() else address + 1)
        if text == "ret":
            if not self.stack:
                raise IndexError("nichts zum Zurueckspringen")
            return self.stack.pop()
        return address + 1


def compare_versus_subtract():
    """Stellt cmp und sub gegenüber.

    Beide rechnen dasselbe und setzen dieselben Flags; sub schreibt das
    Ergebnis in das Zielregister, cmp verwirft es.
    """
    return {"flags": "the same", "destination after cmp": "unchanged",
            "destination after sub": "the difference"}


def why_conditions_come_in_pairs():
    """Erklärt, warum ein Vergleich zwei Sätze von Sprüngen braucht.

    Dasselbe Bitmuster bedeutet vorzeichenlos etwas anderes als
    vorzeichenbehaftet. Deshalb gibt es jb und jl nebeneinander: der eine
    liest das Übertragsflag, der andere den Vergleich von Vorzeichen- und
    Überlaufflag. Wer den falschen wählt, bekommt bei negativen Zahlen
    oder bei sehr grossen vorzeichenlosen Werten die falsche Antwort.
    """
    return {"unsigned": ["jb", "jae", "ja", "jbe"],
            "signed": ["jl", "jge", "jg", "jle"],
            "the mistake": "using the unsigned form on signed data"}
