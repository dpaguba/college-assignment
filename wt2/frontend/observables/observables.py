"""Beobachtbare Ströme: Werte, die über die Zeit eintreffen."""


class Subscription:
    """Ein laufendes Abonnement, das sich beenden lässt."""

    def __init__(self):
        """Legt ein aktives Abonnement an."""
        self.active = True

    def unsubscribe(self):
        """Beendet das Abonnement; weitere Werte kommen nicht mehr an."""
        self.active = False


class Observable:
    """Ein Strom, der erst beim Abonnieren etwas tut."""

    def __init__(self, producer):
        """Legt einen Strom über seiner Erzeugerfunktion an.

        Args:
            producer: Funktion, die einen Beobachter bekommt und ihn
                bedient.
        """
        self.producer = producer

    def subscribe(self, on_value, on_error=None, on_complete=None):
        """Abonniert den Strom und startet damit die Erzeugung.

        Returns:
            Das Abonnement.
        """
        subscription = Subscription()
        observer = {"next": on_value, "error": on_error,
                    "complete": on_complete, "subscription": subscription}
        self.producer(observer)
        return subscription

    def map(self, function):
        """Bildet jeden Wert ab."""
        def producer(observer):
            """Reicht die abgebildeten Werte weiter."""
            self.subscribe(lambda value: observer["next"](function(value)),
                           observer["error"], observer["complete"])
        return Observable(producer)

    def filter(self, predicate):
        """Lässt nur die Werte durch, die das Prädikat erfüllen."""
        def producer(observer):
            """Reicht die passenden Werte weiter."""
            def forward(value):
                """Prüft und reicht weiter."""
                if predicate(value):
                    observer["next"](value)
            self.subscribe(forward, observer["error"], observer["complete"])
        return Observable(producer)

    def take(self, count):
        """Beendet den Strom nach einer festen Zahl von Werten."""
        def producer(observer):
            """Zählt mit und bricht ab."""
            seen = [0]

            def forward(value):
                """Reicht weiter, solange noch etwas fehlt."""
                if seen[0] < count:
                    seen[0] += 1
                    observer["next"](value)
            self.subscribe(forward, observer["error"], observer["complete"])
        return Observable(producer)


def of(*values):
    """Baut einen Strom aus festen Werten."""
    def producer(observer):
        """Gibt die Werte der Reihe nach ab."""
        for value in values:
            if not observer["subscription"].active:
                return
            observer["next"](value)
        if observer["complete"]:
            observer["complete"]()
    return Observable(producer)


def lazy_until_subscribed():
    """Zeigt, dass ohne Abonnent nichts geschieht.

    Returns:
        Abbildung mit der Zahl der erzeugten Werte vor und nach dem
        Abonnieren.
    """
    produced = [0]

    def producer(observer):
        """Erzeugt drei Werte und zählt sie mit."""
        for value in range(3):
            produced[0] += 1
            observer["next"](value)

    stream = Observable(producer)
    before = produced[0]
    stream.subscribe(lambda value: None)
    return {"before": before, "after": produced[0]}


def unsubscribe_example():
    """Zeigt, dass ein beendetes Abonnement keine Werte mehr bekommt.

    Der Erzeuger prüft vor jedem Wert, ob noch jemand zuhört, und hört
    dann selbst auf: abgegeben werden weniger Werte als vorhanden sind.

    Returns:
        Abbildung mit der Zahl der vorhandenen, abgegebenen und
        empfangenen Werte.
    """
    emitted = [0]
    received = []

    def producer(observer):
        """Gibt fünf Werte ab, solange das Abonnement lebt."""
        for value in range(5):
            if not observer["subscription"].active:
                return
            emitted[0] += 1
            observer["next"](value)

    stream = Observable(producer)
    holder = {}

    def receive(value):
        """Nimmt zwei Werte und beendet dann das Abonnement."""
        received.append(value)
        if len(received) == 2:
            holder["subscription"].active = False

    subscription = Subscription()
    holder["subscription"] = subscription
    stream.producer({"next": receive, "error": None, "complete": None,
                     "subscription": subscription})
    return {"available": 5, "emitted": emitted[0],
            "received": len(received)}


def error_example():
    """Zeigt, dass ein Fehler den Strom beendet.

    Returns:
        Abbildung mit der Zahl der Werte vor dem Fehler und dem Vermerk,
        dass der Strom nicht ordentlich endet.
    """
    seen = []
    state = {"completed": False, "failed": False}

    def producer(observer):
        """Gibt zwei Werte ab und scheitert dann."""
        observer["next"](1)
        observer["next"](2)
        if observer["error"]:
            observer["error"](ValueError("kaputt"))
            return
        if observer["complete"]:
            observer["complete"]()

    Observable(producer).subscribe(
        seen.append,
        on_error=lambda error: state.update(failed=True),
        on_complete=lambda: state.update(completed=True))
    return {"values before error": len(seen), "completed": state["completed"],
            "failed": state["failed"]}


def promise_versus_stream():
    """Vergleicht ein Versprechen mit einem Strom.

    Ein Versprechen liefert genau einen Wert und ist danach fertig; ein
    Strom kann beliebig viele liefern und beginnt erst beim Abonnieren.

    Returns:
        Abbildung mit der Zahl der gelieferten Werte.
    """
    promise = [42]
    stream = []
    of(1, 2, 3).subscribe(stream.append)
    return {"promise": len(promise), "stream": len(stream),
            "promise starts": "immediately", "stream starts": "on subscribe"}
