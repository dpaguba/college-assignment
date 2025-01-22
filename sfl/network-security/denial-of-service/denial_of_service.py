"""Überlastungsangriffe und was gegen sie hilft."""


def flood(capacity, incoming):
    """Rechnet aus, wie viele Anfragen bei Überlast bedient werden.

    Die Kapazität ist die Schranke: alles darüber wird abgewiesen, und
    darunter leiden die Anfragen, die berechtigt sind, ebenso wie die
    anderen. Genau darin besteht der Schaden.

    Raises:
        ValueError: bei negativen Werten.
    """
    if capacity < 0 or incoming < 0:
        raise ValueError("negative Werte")
    served = min(capacity, incoming)
    return {"capacity": capacity, "incoming": incoming, "served": served,
            "rejected": incoming - served,
            "share served": served / incoming if incoming else 1.0}


def amplification(request, response):
    """Berechnet den Verstärkungsfaktor eines Dienstes.

    Der Angreifer schickt eine kleine Anfrage mit gefälschter
    Absenderadresse; die grosse Antwort geht an das Opfer. Sein eigener
    Aufwand ist die Anfrage, der Schaden die Antwort.

    Raises:
        ValueError: bei nicht positiven Werten.
    """
    if request < 1 or response < 1:
        raise ValueError("Werte muessen positiv sein")
    return {"request bytes": request, "response bytes": response,
            "factor": response / request,
            "needs": "a protocol over udp and a forged source address",
            "examples": {"dns": 50, "ntp monlist": 550, "memcached": 10000}}


def syn_flood(connections=10000, cookies=False):
    """Vergleicht den Aufwand beider Seiten bei halboffenen Verbindungen.

    Der Angreifer schickt Verbindungswünsche und antwortet nie. Der Server
    merkt sich jeden und wartet; der Angreifer merkt sich nichts. Werden
    die Angaben stattdessen in die eigene Antwort hineingerechnet und
    beim Rückläufer wieder herausgelesen, so muss der Server nichts
    aufbewahren.

    Args:
        connections: Zahl der Wünsche.
        cookies: ob der Server sich nichts merkt.

    Returns:
        Abbildung mit dem Zustand beider Seiten.

    Raises:
        ValueError: bei einer negativen Zahl von Wünschen.
    """
    if connections < 0:
        raise ValueError("negative Anzahl")
    return {"half open connections": connections,
            "server state": 0 if cookies else connections,
            "attacker state": 0,
            "asymmetry": "none" if cookies else "the server pays, the "
                                                "attacker does not",
            "cost of cookies": "some options of the connection cannot be "
                               "carried"}


def distributed(sources):
    """Beschreibt, warum ein verteilter Angriff schwerer abzuwehren ist.

    Bei einer einzigen Quelle genügt eine Sperre. Bei zehntausend sieht
    jede einzelne wie ein gewöhnlicher Besucher aus, und eine Sperre nach
    Adresse trifft entweder zu wenig oder auch die Berechtigten.

    Raises:
        ValueError: bei einer nicht positiven Zahl.
    """
    if sources < 1:
        raise ValueError("die Zahl muss positiv sein")
    return {"sources": sources,
            "blocking one address helps": sources == 1,
            "requests per source": "few enough to look ordinary",
            "the real problem": "telling the two apart at all",
            "where it has to be stopped": "upstream, before the link is "
                                          "full"}


def countermeasures():
    """Nennt die Massnahmen und was jede leistet."""
    return {"rate limiting": "caps what one source may do",
            "syn cookies": "removes the state the attacker was filling",
            "filtering upstream": "the only answer once the link itself is "
                                  "saturated",
            "anycast": "spreads the traffic over many locations",
            "source address validation": "would remove amplification, and "
                                         "needs every network to take part",
            "capacity": "expensive, and the attacker can add more sources"}


def why_it_cannot_be_solved():
    """Erklärt, warum es keine vollständige Abwehr gibt.

    Ein Dienst, der erreichbar sein soll, muss Anfragen entgegennehmen und
    bearbeiten. Solange eine Anfrage den Server mehr kostet als den
    Absender, lässt sich das ausnutzen; die Abwehr besteht darin, dieses
    Verhältnis umzudrehen oder den Angriff weit genug vom Ziel aufzuhalten.
    """
    return {"root cause": "serving a request costs more than sending one",
            "goal of the defence": "make the attacker pay first, or stop "
                                   "the traffic before it arrives",
            "never fully solved": True}
