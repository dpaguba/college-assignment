"""Paketfilter: Regeln, Voreinstellung und der Wert des Verbindungszustands."""

INTERNAL = "192.168.0.0/24"


def in_network(address, network):
    """Prüft, ob eine Adresse in einem Netz liegt.

    Args:
        address: die Adresse in Punktschreibweise.
        network: das Netz als Adresse mit Präfixlänge.

    Raises:
        ValueError: bei einer unlesbaren Angabe.
    """
    try:
        base, prefix = network.split("/")
        bits = int(prefix)
        parts = [int(piece) for piece in address.split(".")]
        base_parts = [int(piece) for piece in base.split(".")]
    except (ValueError, AttributeError) as error:
        raise ValueError("unlesbare Adresse oder Netz") from error
    if len(parts) != 4 or len(base_parts) != 4 or not 0 <= bits <= 32:
        raise ValueError("unlesbare Adresse oder Netz")
    value = sum(piece << (8 * (3 - index))
                for index, piece in enumerate(parts))
    base_value = sum(piece << (8 * (3 - index))
                     for index, piece in enumerate(base_parts))
    mask = (0xFFFFFFFF << (32 - bits)) & 0xFFFFFFFF if bits else 0
    return value & mask == base_value & mask


def rule(action, source=None, source_port=None, destination=None,
         destination_port=None, protocol=None, state=None):
    """Baut eine Regel; ein weggelassenes Feld passt auf alles."""
    return {"action": action, "source": source, "source port": source_port,
            "destination": destination,
            "destination port": destination_port, "protocol": protocol,
            "state": state}


def _field_matches(constraint, value, is_address):
    """Prüft ein einzelnes Feld gegen eine Bedingung."""
    if constraint is None:
        return True
    if value is None:
        return False
    if is_address:
        return in_network(value, constraint)
    if isinstance(constraint, (set, frozenset, list, tuple)):
        return value in constraint
    return value == constraint


def matches(entry, packet):
    """Prüft, ob eine Regel auf ein Paket passt."""
    checks = (("source", True), ("destination", True),
              ("source port", False), ("destination port", False),
              ("protocol", False), ("state", False))
    for field, is_address in checks:
        if not _field_matches(entry[field], packet.get(field), is_address):
            return False
    return True


def decide(rules, packet):
    """Wendet die Regeln der Reihe nach an und nimmt die erste, die passt.

    Raises:
        ValueError: wenn keine Regel passt, die Liste also keine
            Voreinstellung enthält.
    """
    for entry in rules:
        if matches(entry, packet):
            return entry["action"]
    raise ValueError("keine Regel passt und keine Voreinstellung gesetzt")


def http_only():
    """Stellt die Regeln aus Aufgabe 7.1a auf.

    Erlaubt wird den internen Rechnern der Aufbau von Verbindungen zu den
    Diensten auf den Ports 80 und 443 und die Antwort darauf; alles andere
    wird verworfen. Die letzte Regel ist die Voreinstellung, und sie muss
    verwerfen: eine Liste ohne sie erlaubt am Ende alles, was niemand
    bedacht hat.
    """
    return [
        rule("allow", source=INTERNAL, destination_port=80, protocol="tcp",
             state="new"),
        rule("allow", source=INTERNAL, destination_port=443, protocol="tcp",
             state="new"),
        rule("allow", source_port={80, 443}, destination=INTERNAL,
             protocol="tcp", state="established"),
        rule("drop"),
    ]


def block_two_servers():
    """Stellt die Regeln aus Aufgabe 7.1b auf.

    Ausgehende Verbindungen und ihre Antworten sind erlaubt, der Verkehr
    zu und von zwei genannten Servern nicht. Die Sperren stehen vorn: eine
    Regel, die nach der Erlaubnis kommt, wird nie erreicht.
    """
    return [
        rule("drop", destination="6.6.6.6/32"),
        rule("drop", destination="66.66.66.66/32"),
        rule("drop", source="6.6.6.6/32"),
        rule("drop", source="66.66.66.66/32"),
        rule("allow", source=INTERNAL, state="new"),
        rule("allow", destination=INTERNAL, state="established"),
        rule("drop"),
    ]


def stateless_problem():
    """Erklärt, was ein Filter ohne Verbindungszustand nicht ausdrücken kann.

    Er sieht jedes Paket für sich und weiss nicht, ob es die Antwort auf
    eine erlaubte Anfrage ist. Um Antworten hereinzulassen, muss er alle
    Pakete mit einem Quellport von 80 oder 443 an die hohen Zielports
    erlauben, und die kann ein Angreifer ebenso setzen.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"must open the high ports": True,
            "range": "1024 to 65535",
            "attacker can set the source port": True,
            "with state": "the filter remembers the outgoing connection and "
                          "lets only its answer back"}


def order_matters():
    """Zeigt, dass die Reihenfolge der Regeln das Ergebnis bestimmt.

    Returns:
        Abbildung mit dem Ergebnis für beide Reihenfolgen desselben Paars.
    """
    packet = {"source": "192.168.0.5", "destination": "6.6.6.6",
              "destination port": 443, "protocol": "tcp", "state": "new"}
    deny_first = [rule("drop", destination="6.6.6.6/32"),
                  rule("allow", source=INTERNAL, state="new"),
                  rule("drop")]
    allow_first = [rule("allow", source=INTERNAL, state="new"),
                   rule("drop", destination="6.6.6.6/32"),
                   rule("drop")]
    return {"deny first": decide(deny_first, packet),
            "allow first": decide(allow_first, packet),
            "lesson": "a rule after a matching one is never reached"}


def kinds():
    """Nennt die Bauarten von Filtern."""
    return {"packet filter": "one packet at a time, addresses and ports",
            "stateful filter": "remembers connections",
            "application gateway": "understands the protocol and can look "
                                   "into the payload",
            "note": "each step up costs performance and adds a component "
                    "that can itself be attacked"}
