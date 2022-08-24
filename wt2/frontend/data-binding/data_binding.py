"""Datenbindung zwischen Modell und Ansicht."""


class Model:
    """Ein Modell, das seine Beobachter über Änderungen benachrichtigt."""

    def __init__(self, fields):
        """Legt das Modell mit seinen Feldern an."""
        self.fields = dict(fields)
        self.listeners = {}
        self.notifications = 0

    def get(self, name):
        """Liest ein Feld.

        Raises:
            KeyError: wenn das Feld fehlt.
        """
        return self.fields[name]

    def set(self, name, value):
        """Schreibt ein Feld und benachrichtigt seine Beobachter.

        Benachrichtigt werden nur die Beobachter dieses Feldes; ein
        Modell, das bei jeder Änderung alles neu zeichnen liesse, wäre
        der Grund für die meisten Leistungsprobleme einer Oberfläche.
        """
        if name not in self.fields:
            raise KeyError(name)
        self.fields[name] = value
        for listener in self.listeners.get(name, []):
            listener(value)
            self.notifications += 1

    def observe(self, name, listener):
        """Meldet einen Beobachter für ein Feld an."""
        self.listeners.setdefault(name, []).append(listener)


class View:
    """Eine Ansicht, die den Wert eines Feldes zeigt."""

    def __init__(self, model, name, direction):
        """Verbindet die Ansicht mit einem Feld des Modells."""
        self.model = model
        self.name = name
        self.direction = direction
        self.value = model.get(name)

    def edit(self, value):
        """Simuliert eine Eingabe des Benutzers.

        Bei einseitiger Bindung bleibt die Änderung in der Ansicht; nur
        die zweiseitige schreibt sie zurück ins Modell.
        """
        self.value = value
        if self.direction == "two way":
            self.model.set(self.name, value)


def bind(model, name, direction="one way"):
    """Verbindet ein Feld des Modells mit einer Ansicht.

    Args:
        model: das Modell.
        name: der Feldname.
        direction: ``one way`` oder ``two way``.

    Returns:
        Die Ansicht.

    Raises:
        ValueError: bei einer unbekannten Richtung.
    """
    if direction not in ("one way", "two way"):
        raise ValueError("unbekannte Bindungsrichtung")
    view = View(model, name, direction)

    def update(value):
        """Übernimmt eine Änderung des Modells in die Ansicht."""
        view.value = value

    model.observe(name, update)
    return view


def notification_count():
    """Misst, wie viele Beobachter eine einzelne Änderung erreicht.

    Returns:
        Abbildung mit der Zahl der Felder und der Benachrichtigungen.
    """
    model = Model({"a": 1, "b": 2, "c": 3})
    for name in ("a", "b", "c"):
        bind(model, name)
    model.set("b", 20)
    return {"fields": len(model.fields), "notified": model.notifications}


def change_detection():
    """Beschreibt die beiden Wege, eine Änderung zu bemerken."""
    return {"dirty checking": "compare the values after every event",
            "observation": "the model announces what changed",
            "cost of dirty checking": "grows with the number of bindings",
            "cost of observation": "every write goes through a setter"}


def directions():
    """Nennt die Bindungsrichtungen und wofür sie taugen."""
    return {"one way to the view": "displaying a value",
            "one way to the model": "reacting to an event",
            "two way": "a form field, where both sides change"}
