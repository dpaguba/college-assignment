"""Trennung von Prozessen und was sie leistet."""


class AccessViolation(Exception):
    """Wird geworfen, wenn ein Prozess fremden Speicher berührt."""


class Machine:
    """Eine Maschine, die jedem Prozess einen eigenen Adressraum gibt."""

    def __init__(self):
        """Legt eine Maschine ohne Prozesse an."""
        self.memory = {}
        self.shared = {}
        self.next_id = 1

    def spawn(self, name):
        """Startet einen Prozess mit eigenem Speicher."""
        identifier = self.next_id
        self.next_id += 1
        self.memory[identifier] = {}
        return identifier

    def write(self, process, page, value):
        """Schreibt in den eigenen Adressraum."""
        self.memory[process][page] = value
        for other, pages in self.shared.items():
            if page in pages and other != process:
                self.memory[other][page] = value

    def read(self, process, page):
        """Liest aus dem eigenen Adressraum.

        Raises:
            KeyError: wenn die Seite nicht belegt ist.
        """
        return self.memory[process][page]

    def read_foreign(self, process, other, page):
        """Versucht, den Adressraum eines anderen Prozesses zu lesen.

        Raises:
            AccessViolation: immer, solange die Seite nicht geteilt ist.
        """
        if page in self.shared.get(process, set()) \
                and page in self.shared.get(other, set()):
            return self.memory[other][page]
        raise AccessViolation("fremder Adressraum")

    def share(self, first, second, page):
        """Vereinbart eine gemeinsam sichtbare Seite.

        Gemeinsamer Speicher ist die Ausnahme, die beide Seiten
        ausdrücklich verabreden; alles andere bleibt getrennt.
        """
        self.shared.setdefault(first, set()).add(page)
        self.shared.setdefault(second, set()).add(page)
        value = self.memory[first].get(page)
        if value is not None:
            self.memory[second][page] = value


def measures():
    """Nennt die Mittel, mit denen Prozesse getrennt werden."""
    return {"virtual memory": "each process sees its own addresses",
            "privilege rings": "user code cannot execute privileged "
                               "instructions",
            "system calls": "the only door into the kernel, and it is "
                            "checked",
            "namespaces": "a process sees only part of the system",
            "sandboxing": "the set of allowed system calls is narrowed"}


def against_covert_channels():
    """Sagt, welche verdeckten Kanäle die Trennung schliesst.

    Ein Speicherkanal braucht ein gemeinsam beschreibbares Objekt und
    verschwindet mit der Trennung der Adressräume. Ein Zeitkanal braucht
    nur eine gemeinsame Ressource, deren Auslastung messbar ist, und
    Rechenzeit und Zwischenspeicher bleiben gemeinsam.
    """
    return {"storage channel closed": True, "timing channel closed": False,
            "reason": "time on a shared resource is still observable",
            "what would close it": "separate hardware, or a fixed schedule "
                                   "that hides the load"}


def principle_of_least_privilege():
    """Beschreibt das Prinzip, das hinter allen Massnahmen steht."""
    return {"rule": "every part gets exactly the rights it needs",
            "consequence": "a compromise reaches only as far as those rights",
            "measure": "how much an attacker gains from one process"}
