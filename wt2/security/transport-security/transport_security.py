"""Verschlüsselte Übertragung: Zertifikate, Kette und Schlüsseleinigung."""


def certificate(subject, issuer, valid_from, valid_to):
    """Baut ein Zertifikat als Abbildung."""
    return {"subject": subject, "issuer": issuer, "from": valid_from,
            "to": valid_to}


def example_chain():
    """Liefert eine Kette vom Blatt bis zur Wurzel."""
    return [certificate("example.org", "intermediate", 0, 100),
            certificate("intermediate", "root", 0, 200),
            certificate("root", "root", 0, 300)]


def name_matches(pattern, hostname):
    """Prüft, ob ein Zertifikatsname zum angefragten Rechnernamen passt.

    Ein Stern deckt genau eine Ebene ab: ``*.example.org`` passt auf
    ``www.example.org``, nicht auf ``a.b.example.org``.
    """
    if pattern == hostname:
        return True
    if not pattern.startswith("*."):
        return False
    rest = pattern[2:]
    if not hostname.endswith("." + rest):
        return False
    label = hostname[:-(len(rest) + 1)]
    return "." not in label and label != ""


def validate(chain, trusted, hostname, now):
    """Prüft eine Zertifikatskette.

    Geprüft werden der Name des Blattes, die Gültigkeitszeiträume, die
    Verkettung der Aussteller und die Verankerung in einer bekannten
    Wurzel.

    Returns:
        Abbildung mit ``valid`` und im Fehlerfall ``reason``.

    Raises:
        ValueError: bei einer leeren Kette.
    """
    if not chain:
        raise ValueError("leere Kette")
    leaf = chain[0]
    if not name_matches(leaf["subject"], hostname):
        return {"valid": False, "reason": "hostname mismatch"}
    for entry in chain:
        if not entry["from"] <= now <= entry["to"]:
            return {"valid": False, "reason": "expired"}
    for lower, upper in zip(chain, chain[1:]):
        if lower["issuer"] != upper["subject"]:
            return {"valid": False, "reason": "broken chain"}
    root = chain[-1]
    if root["subject"] not in trusted:
        return {"valid": False, "reason": "no trusted root"}
    if root["issuer"] != root["subject"] and len(chain) > 1:
        return {"valid": False, "reason": "root is not self signed"}
    return {"valid": True, "reason": None, "length": len(chain)}


def handshake(prime=23, generator=5, client_secret=6, server_secret=15):
    """Rechnet eine Schlüsseleinigung nach Diffie und Hellman nach.

    Beide Seiten schicken ihren öffentlichen Wert über die Leitung und
    kommen unabhängig auf denselben gemeinsamen Schlüssel; dieser Wert
    wird nie übertragen.

    Returns:
        Abbildung mit beiden Schlüsseln und dem, was auf der Leitung war.
    """
    client_public = pow(generator, client_secret, prime)
    server_public = pow(generator, server_secret, prime)
    client_key = pow(server_public, client_secret, prime)
    server_key = pow(client_public, server_secret, prime)
    return {"client key": client_key, "server key": server_key,
            "on the wire": [prime, generator, client_public, server_public]}


def what_it_protects():
    """Nennt, was die verschlüsselte Übertragung leistet und was nicht."""
    return {"confidentiality": "nobody in between reads it",
            "integrity": "nobody in between changes it unnoticed",
            "authentication of the server": "the certificate says who it is",
            "not covered": ["what the server does with the data",
                            "who the caller is, unless a client certificate "
                            "is used",
                            "that the site is trustworthy"]}
