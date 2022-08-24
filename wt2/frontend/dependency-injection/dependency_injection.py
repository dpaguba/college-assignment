"""Abhängigkeitsinjektion mit einer Hierarchie von Injektoren."""


class Injector:
    """Hält Rezepte für Dienste und gibt fertige Instanzen heraus."""

    def __init__(self, parent=None):
        """Legt einen Injektor an, gegebenenfalls unter einem Elternteil."""
        self.recipes = {}
        self.instances = {}
        self.parent = parent
        self.building = set()

    def provide(self, name, factory, needs=()):
        """Hinterlegt, wie ein Dienst gebaut wird.

        Args:
            name: der Name, unter dem der Dienst angefordert wird.
            factory: die Funktion, die ihn baut.
            needs: die Namen der Dienste, die sie als Argumente bekommt.
        """
        self.recipes[name] = (factory, list(needs))
        self.instances.pop(name, None)

    def child(self):
        """Legt einen untergeordneten Injektor an.

        Er sieht alles, was der Elternteil kennt, und kann einzelne
        Dienste durch eigene ersetzen, ohne den Elternteil zu ändern.
        """
        return Injector(parent=self)

    def get(self, name):
        """Liefert die Instanz eines Dienstes.

        Innerhalb eines Injektors wird jeder Dienst genau einmal gebaut.

        Raises:
            KeyError: wenn der Dienst nirgends hinterlegt ist.
            ValueError: bei einem Kreis in den Abhängigkeiten.
        """
        if name in self.instances:
            return self.instances[name]
        if name not in self.recipes:
            if self.parent is None:
                raise KeyError("unbekannter Dienst: %s" % name)
            return self.parent.get(name)
        if name in self.building:
            raise ValueError("Kreis in den Abhaengigkeiten bei %s" % name)
        factory, needs = self.recipes[name]
        self.building.add(name)
        try:
            arguments = [self.get(dependency) for dependency in needs]
            instance = factory(*arguments)
        finally:
            self.building.discard(name)
        self.instances[name] = instance
        return instance

    def knows(self, name):
        """Sagt, ob dieser Injektor oder ein Elternteil den Dienst kennt."""
        if name in self.recipes:
            return True
        return self.parent.knows(name) if self.parent else False


def why_not_construct_directly():
    """Nennt, was die Umkehrung der Erzeugung einbringt."""
    return ["a test can hand in a substitute",
            "the caller does not need to know how the service is built",
            "one instance can be shared without a global",
            "the wiring is in one place"]


def scopes():
    """Beschreibt die Reichweiten, in denen Dienste leben."""
    return {"root": "one instance for the whole application",
            "module": "one instance per module",
            "component": "one instance per component, gone with it"}
