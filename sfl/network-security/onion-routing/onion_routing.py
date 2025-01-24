"""Zwiebelrouting: Anonymität durch geschichtete Verschlüsselung."""

import hashlib

POSITIONS = ("entry", "middle", "exit")


def build_circuit(names):
    """Legt einen Pfad mit einem Schlüssel je Station an.

    Der Absender vereinbart mit jeder Station einen eigenen Schlüssel; die
    Stationen kennen einander nicht und teilen nichts miteinander.

    Raises:
        ValueError: wenn die Zahl der Stationen nicht drei ist.
    """
    if len(names) != 3:
        raise ValueError("ein Pfad hat drei Stationen")
    return [{"name": name, "position": POSITIONS[index],
             "key": int.from_bytes(
                 hashlib.sha256(name.encode("utf-8")).digest()[:4], "big")}
            for index, name in enumerate(names)]


def _mix(data, key):
    """Verknüpft Daten mit einem Schlüssel; die Operation ist selbstinvers."""
    stream = hashlib.sha256(str(key).encode("utf-8")).digest()
    raw = data.encode("utf-8") if isinstance(data, str) else data
    return bytes(byte ^ stream[index % len(stream)]
                 for index, byte in enumerate(raw))


def wrap(payload, circuit):
    """Legt für jede Station eine Schicht um die Nachricht.

    Gewickelt wird von innen nach aussen: die innerste Schicht gehört der
    letzten Station, die äusserste der ersten. Jede Station kann genau
    ihre eigene Schicht öffnen.

    Returns:
        Abbildung mit den Daten und der Zahl der Schichten.
    """
    data = payload
    for station in reversed(circuit):
        data = _mix(data, station["key"])
    return {"data": data, "layers": len(circuit), "peeled": 0}


def peel(packet, circuit):
    """Nimmt die äusserste Schicht ab.

    Returns:
        Das Paket mit einer Schicht weniger; nach der letzten steht die
        Nachricht unter ``payload``.

    Raises:
        ValueError: wenn schon alle Schichten entfernt sind.
    """
    if packet["peeled"] >= packet["layers"]:
        raise ValueError("es ist keine Schicht mehr da")
    station = circuit[packet["peeled"]]
    data = _mix(packet["data"], station["key"])
    peeled = packet["peeled"] + 1
    result = {"data": data, "layers": packet["layers"], "peeled": peeled,
              "opened by": station["name"]}
    if peeled == packet["layers"]:
        result["payload"] = data.decode("utf-8")
    return result


def knowledge():
    """Sagt, was jede Station sieht.

    Die erste kennt den Absender, weil er ihr die Pakete schickt, aber
    nicht das Ziel, das unter zwei weiteren Schichten liegt. Die letzte
    kennt das Ziel, weil sie dorthin ausliefert, aber nicht den Absender.
    Die mittlere kennt keines von beiden, nur ihre beiden Nachbarn.

    Returns:
        Abbildung von der Stelle im Pfad auf das, was sie weiss.
    """
    return {"entry": {"knows the sender": True,
                      "knows the destination": False,
                      "sees": "the sender and the middle node"},
            "middle": {"knows the sender": False,
                       "knows the destination": False,
                       "sees": "its two neighbours"},
            "exit": {"knows the sender": False,
                     "knows the destination": True,
                     "sees": "the middle node and the destination"}}


def controlled_nodes(count, positions=()):
    """Beurteilt, was ein Angreifer mit einer Zahl von Stationen erreicht.

    Eine einzelne Station sieht immer nur eine Seite. Erst wer die erste
    und die letzte zugleich betreibt, hat beide Enden und kann sie über
    die Zeitpunkte und Grössen der Pakete einander zuordnen.

    Args:
        count: Zahl der beherrschten Stationen.
        positions: welche Stellen des Pfades darunter sind; die genannten
            Stellen sind eine Teilmenge der beherrschten Stationen.

    Returns:
        Abbildung mit dem Befund.

    Raises:
        ValueError: bei einer negativen Zahl oder wenn mehr Stellen
            genannt sind, als Stationen beherrscht werden.
    """
    if count < 0:
        raise ValueError("negative Anzahl")
    if len(set(positions)) > count:
        raise ValueError("mehr Stellen als beherrschte Stationen")
    holds_both_ends = "entry" in positions and "exit" in positions
    return {"nodes": count, "positions": list(positions),
            "can link sender and destination": holds_both_ends,
            "can read the traffic": "exit" in positions,
            "can drop or delay": count > 0,
            "probability with a share p of the network": "p squared for the "
                                                         "two ends"}


def exit_node_risk():
    """Nennt, was die letzte Station sieht.

    Sie stellt die Verbindung zum Ziel her und sieht daher genau das, was
    ein Netzbetreiber ohne Zwiebelrouting sähe. Ist die Verbindung zum
    Ziel nicht verschlüsselt, liest sie mit; das Zwiebelrouting verbirgt,
    wer spricht, nicht was gesagt wird.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"sees the plaintext unless the site uses tls": True,
            "knows the destination": True,
            "does not know the sender": True,
            "consequence": "anonymity is not confidentiality"}


def traffic_analysis():
    """Beschreibt den Angriff, der ohne eine einzige Station auskommt.

    Wer den Verkehr an beiden Enden beobachten kann, braucht die
    Verschlüsselung nicht zu brechen: die Zeitpunkte und die Grössen der
    Pakete auf beiden Seiten passen zueinander. Gegen einen Beobachter,
    der weite Teile des Netzes sieht, hilft das Verfahren nicht.

    Returns:
        Abbildung mit dem Befund und den Gegenmitteln.
    """
    return {"timing correlation works": True,
            "needs no node": True,
            "assumption broken": "the attacker sees only part of the "
                                 "network",
            "countermeasures": ["padding to a fixed size",
                                "cover traffic", "delays"],
            "why they are rare": "they cost bandwidth and latency, and the "
                                 "users notice"}


def what_it_provides():
    """Fasst zusammen, was das Verfahren leistet."""
    return {"hides": "who talks to whom",
            "does not hide": "what is said, unless the connection is "
                             "encrypted as well",
            "does not protect against": ["an attacker at both ends",
                                         "a browser that identifies itself",
                                         "a user who logs in"]}
