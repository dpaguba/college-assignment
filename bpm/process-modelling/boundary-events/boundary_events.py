"""Angeheftete Ereignisse: die Ausnahme am Rand einer Aktivität."""


def attach(activity, event, interrupting):
    """Heftet ein Ereignis an eine Aktivität.

    Ein unterbrechendes Ereignis bricht die Aktivität ab und schickt den
    Fall auf den Ausnahmepfad. Ein nicht unterbrechendes (doppelt
    gestrichelte Umrandung) startet den Ausnahmepfad nebenher, während die
    Aktivität weiterläuft.

    Args:
        activity: die Aktivität, an deren Rand das Ereignis sitzt.
        event: das Ereignis.
        interrupting: ob es die Aktivität abbricht.

    Returns:
        Abbildung mit dem Verhalten und dem ausgehenden Pfad.

    Raises:
        ValueError: wenn Aktivität oder Ereignis fehlen.
    """
    if not activity:
        raise ValueError("ein Randereignis braucht eine Aktivität")
    if not event:
        raise ValueError("ein Randereignis braucht ein Ereignis")
    return {"activity": activity, "event": event,
            "interrupting": interrupting,
            "activity continues": not interrupting,
            "border": "solid" if interrupting else "dashed twice",
            "flow": "exception flow"}


def order_example():
    """Das Beispiel der Vorlesung: die Prüfung der Verfügbarkeit.

    An der Aktivität hängen zwei Ereignisse: neue Kundendaten (nicht
    unterbrechend, sie werden nebenher hinterlegt) und eine Stornierung
    (unterbrechend, die Bestellung wird abgebrochen).

    Returns:
        Liste der angehefteten Ereignisse.
    """
    return [attach("Verfügbarkeit von Artikel prüfen",
                   "Neue Kundendaten erhalten", interrupting=False),
            attach("Verfügbarkeit von Artikel prüfen",
                   "Stornierung erhalten", interrupting=True)]


def kinds():
    """Nennt die Ereignisarten, die am Rand vorkommen."""
    return {"message": "eine Nachricht trifft ein",
            "timer": "eine Frist läuft ab",
            "error": "die Aktivität meldet einen Fehler",
            "escalation": "der Fall wird eine Ebene höher gegeben",
            "condition": "eine Bedingung wird wahr",
            "signal": "ein Signal wird ausgesendet"}


def error_is_always_interrupting():
    """Sagt, welches Randereignis keine Wahl hat.

    Ein Fehlerereignis bricht immer ab: die Aktivität hat gemeldet, dass
    sie nicht zu Ende kommt, und kann deshalb nicht weiterlaufen.
    """
    return {"error": True, "cancel": True,
            "message": False, "timer": False, "signal": False,
            "why": "the activity has already declared that it failed"}


def without_boundary_events():
    """Zeigt, was der Ausweg ohne Randereignisse kostet.

    Ohne sie muss jede Ausnahme im Kontrollfluss stehen: nach jeder
    Aktivität ein Gateway, das fragt, ob etwas dazwischenkam. Das Modell
    verdoppelt seine Knoten und liest sich nicht mehr.
    """
    return {"alternative": "a gateway after every activity",
            "cost": "the model roughly doubles in size",
            "readability": "the normal path disappears in the exceptions"}
