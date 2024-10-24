"""Digitale Geschäftsmodelle und der Netzeffekt."""

COMPONENTS = {
    "Nutzenversprechen": "was der Kunde bekommt und warum es ihm nützt",
    "Wertschöpfung": "wie die Leistung entsteht und wer daran beteiligt "
                     "ist",
    "Ertragsmodell": "womit Geld verdient wird",
    "Kundensegment": "für wen die Leistung gedacht ist",
    "Kanäle": "wie die Leistung den Kunden erreicht",
}

PATTERNS = {
    "Abonnement": "wiederkehrende Zahlung für laufenden Zugang",
    "Freemium": "eine kostenlose Grundstufe finanziert durch eine "
                "bezahlte",
    "Plattform": "zwei Seiten werden zusammengebracht, die Plattform "
                 "nimmt eine Gebühr",
    "Long Tail": "viele seltene Artikel statt weniger häufiger",
    "Pay per Use": "bezahlt wird die tatsächliche Nutzung",
    "Werbefinanzierung": "die Aufmerksamkeit der Nutzer wird verkauft",
}


def components():
    """Nennt die Bestandteile eines Geschäftsmodells."""
    return dict(COMPONENTS)


def patterns():
    """Nennt die Muster, die in der Vorlesung vorkommen."""
    return dict(PATTERNS)


def network_effect(users, providers=None):
    """Zählt die Verbindungen, die ein Netz möglich macht.

    Bei einem einseitigen Netz können alle Teilnehmer miteinander
    verbunden werden, das sind n·(n − 1)/2 Paare: der Wert wächst
    ungefähr quadratisch mit der Zahl der Teilnehmer. Bei einem
    zweiseitigen Netz zählt nur die Verbindung zwischen den Seiten, also
    das Produkt. Beides erklärt, warum eine Plattform am Anfang wenig
    wert ist und ab einer bestimmten Grösse schwer einzuholen.

    Args:
        users: die Teilnehmer der einen Seite.
        providers: die der anderen; ohne Angabe ein einseitiges Netz.

    Returns:
        Abbildung mit der Zahl der Paare und der Art des Netzes.

    Raises:
        ValueError: bei einer negativen Zahl.
    """
    if users < 0 or (providers is not None and providers < 0):
        raise ValueError("negative Teilnehmerzahl")
    if providers is None:
        return {"possible pairs": users * (users - 1) // 2,
                "sides": 1, "grows": "quadratisch",
                "users": users}
    return {"possible pairs": users * providers, "sides": 2,
            "grows": "mit dem Produkt beider Seiten",
            "users": users, "providers": providers}


def chicken_and_egg():
    """Nennt das Anlaufproblem einer zweiseitigen Plattform.

    Anbieter kommen, wenn Kunden da sind, und Kunden kommen, wenn Anbieter
    da sind. Die üblichen Auswege: eine Seite subventionieren, mit einer
    Nische beginnen, in der wenige Teilnehmer reichen, oder eine Seite
    selbst stellen, bis die andere trägt.
    """
    return {"problem": "jede Seite wartet auf die andere",
            "ways out": ["eine Seite subventionieren",
                         "in einer Nische beginnen",
                         "eine Seite zunächst selbst stellen"],
            "why it matters": "der Wert der Plattform ist am Anfang "
                              "beinahe null und wächst dann schnell"}


def what_makes_it_digital():
    """Sagt, was ein digitales von einem gewöhnlichen Modell trennt.

    Nicht die Technik, sondern die Kostenstruktur: die Grenzkosten einer
    weiteren Einheit sind nahe null, während die Fixkosten hoch sind.
    Daraus folgt fast alles andere, vom Abonnement bis zur Neigung zum
    Monopol.
    """
    return {"marginal cost": "nahe null",
            "fixed cost": "hoch",
            "follows": ["Skalierung ohne Stückkosten",
                        "Abonnement statt Einzelverkauf",
                        "Neigung zu wenigen grossen Anbietern"]}
