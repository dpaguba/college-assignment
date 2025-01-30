"""Pufferüberläufe auf dem Stapel."""


class Overflow(Exception):
    """Wird geworfen, wenn eine begrenzte Kopie zu lang wäre."""


class Memory:
    """Ein Stapelrahmen mit Puffer, Basiszeiger und Rückkehradresse."""

    def __init__(self, buffer_size, return_address="0x401136"):
        """Legt den Rahmen an.

        Args:
            buffer_size: Grösse des Puffers in Byte.
            return_address: der ursprüngliche Wert der Rückkehradresse.
        """
        self.buffer_size = buffer_size
        self.original_return = return_address
        self.cells = ["\x00"] * buffer_size + ["B"] * 8 \
            + list(return_address.ljust(8))
        self.saved_base_start = buffer_size
        self.return_start = buffer_size + 8

    def copy(self, data, bounded=False):
        """Kopiert Daten in den Puffer.

        Ohne Begrenzung schreibt die Kopie über das Ende hinaus, wie es
        ``strcpy`` tut. Mit Begrenzung wird abgebrochen, wie es ``strncpy``
        täte.

        Raises:
            Overflow: wenn begrenzt kopiert wird und die Daten zu lang sind.
        """
        if bounded and len(data) > self.buffer_size:
            raise Overflow("die Daten passen nicht in den Puffer")
        for index, character in enumerate(data):
            if index < len(self.cells):
                self.cells[index] = character
            else:
                self.cells.append(character)
        return len(data)

    def return_address(self):
        """Liest die Rückkehradresse aus dem Rahmen."""
        return "".join(self.cells[self.return_start:self.return_start + 8])

    def return_address_overwritten(self):
        """Sagt, ob die Rückkehradresse verändert wurde."""
        return self.return_address() != self.original_return.ljust(8)

    def saved_base_overwritten(self):
        """Sagt, ob der gesicherte Basiszeiger verändert wurde."""
        return "".join(self.cells[self.saved_base_start:
                                  self.saved_base_start + 8]) != "B" * 8


def pass_the_check(buffer_size=16):
    """Löst Aufgabe 3.3c: die Prüfung bestehen, ohne das Passwort zu kennen.

    Neben dem Puffer liegt eine Variable, die den Zugang steuert. Eine
    Eingabe, die über den Puffer hinausreicht, überschreibt sie, und die
    Prüfung des Passworts wird damit gegenstandslos.

    Returns:
        Abbildung mit der Eingabe, dem richtigen Passwort und dem Ergebnis.
    """
    password = "s3cr3t"
    granted_flag = [0]
    buffer_cells = ["\x00"] * buffer_size
    attacker_input = "A" * (buffer_size + 1)
    for index, character in enumerate(attacker_input):
        if index < buffer_size:
            buffer_cells[index] = character
        else:
            granted_flag[0] = ord(character)
    typed = "".join(buffer_cells)
    return {"input": attacker_input, "password": password,
            "password matched": typed == password,
            "granted": granted_flag[0] != 0,
            "why": "the flag next to the buffer was overwritten"}


def kinds():
    """Nennt die beiden Arten und woran sie sich unterscheiden."""
    return {"stack": "overwrites saved base pointer and return address, so "
                     "the function returns where the attacker wants",
            "heap": "overwrites the bookkeeping of the allocator, so a "
                    "later free or allocation writes where the attacker "
                    "wants"}


def defences():
    """Nennt die Massnahmen von der wirksamsten abwärts."""
    return ["bounded string functions",
            "a language that checks its indices",
            "stack canaries",
            "a non executable stack",
            "address space randomisation",
            "compiler warnings taken seriously"]


def why_c_makes_it_easy():
    """Erklärt, warum gerade C diese Klasse von Fehlern hat.

    Ein Feld kennt seine Länge nicht, eine Zeichenkette endet an einem
    Nullbyte statt an einer Grenze, und die Kopierfunktionen der
    Standardbibliothek prüfen nichts. Der Fehler liegt eine Stelle weiter
    als die Sprache sehen kann.
    """
    return {"arrays carry no length": True,
            "strings end at a byte, not at a bound": True,
            "the standard functions check nothing": True,
            "the check has to be written by hand every time": True}
