"""Die Zertifikatsinfrastruktur und wo ihr Vertrauen herkommt."""


def certificate(subject, issuer, valid_from, valid_to, key="a key"):
    """Baut ein Zertifikat als Abbildung."""
    return {"subject": subject, "issuer": issuer, "from": valid_from,
            "to": valid_to, "key": key}


def example_chain():
    """Liefert die Kette aus Aufgabe 7.2b: Blatt, Zwischenstelle, Wurzel."""
    return [certificate("github.com", "intermediate", 0, 100),
            certificate("intermediate", "root", 0, 200),
            certificate("root", "root", 0, 300)]


def name_matches(pattern, hostname):
    """Prüft, ob ein Zertifikatsname zum Rechnernamen passt.

    Ein Stern deckt genau eine Ebene ab.
    """
    if pattern == hostname:
        return True
    if not pattern.startswith("*."):
        return False
    rest = pattern[2:]
    if not hostname.endswith("." + rest):
        return False
    label = hostname[:-(len(rest) + 1)]
    return bool(label) and "." not in label


def validate(chain, trusted, hostname, now, revoked=()):
    """Prüft eine Zertifikatskette.

    Geprüft werden der Name, die Sperrliste, die Gültigkeitszeiträume, die
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
        if entry["subject"] in revoked:
            return {"valid": False, "reason": "revoked"}
    for entry in chain:
        if not entry["from"] <= now <= entry["to"]:
            return {"valid": False, "reason": "expired"}
    for lower, upper in zip(chain, chain[1:]):
        if lower["issuer"] != upper["subject"]:
            return {"valid": False, "reason": "broken chain"}
    if chain[-1]["subject"] not in trusted:
        return {"valid": False, "reason": "no trusted root"}
    return {"valid": True, "reason": None, "length": len(chain)}


def weakest_link(authorities):
    """Rechnet aus, wie viele Stellen ein Angreifer brechen muss.

    Der Browser vertraut jeder Wurzel gleichermassen; jede von ihnen darf
    für jeden Namen ausstellen. Es genügt also, eine einzige zu
    übernehmen oder zu täuschen, gleich wie sorgfältig die übrigen
    arbeiten.

    Raises:
        ValueError: bei einer nicht positiven Zahl.
    """
    if authorities < 1:
        raise ValueError("die Zahl muss positiv sein")
    return {"trusted": authorities, "needed to break the system": 1,
            "each may issue for": "every name",
            "historical cases": ["DigiNotar 2011", "Comodo 2011",
                                 "TrustWave 2012"]}


def revocation_problem():
    """Nennt, warum die Sperrung in der Praxis wenig hilft.

    Die Sperrliste muss abgerufen werden, und wenn der Abruf scheitert,
    lassen die Browser die Verbindung zu, statt sie abzubrechen. Ein
    Angreifer, der die Verbindung beherrscht, unterbindet den Abruf und
    hat damit die Sperrung ausgeschaltet.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"soft fail is the default": True,
            "reason": "hard fail would break browsing whenever the "
                      "responder is unreachable",
            "attacker on the path can block the check": True,
            "answers": ["short lived certificates", "stapling",
                        "pushed lists of the important revocations"]}


def pinned_ok(hostname, expected_key, presented_key):
    """Prüft ein festgelegtes Schlüsselpaar statt der ganzen Kette.

    Die Festlegung engt das Vertrauen auf einen bekannten Schlüssel ein;
    ein gültiges Zertifikat einer anderen Stelle hilft dem Angreifer dann
    nicht mehr. Der Preis ist, dass ein Wechsel des Schlüssels den Dienst
    unerreichbar macht, wenn er nicht vorbereitet wurde.
    """
    return expected_key == presented_key


def transparency():
    """Beschreibt, was die öffentlichen Protokolle leisten.

    Jedes ausgestellte Zertifikat wird in ein öffentliches, nur
    anhängbares Protokoll eingetragen. Eine falsch ausgestellte Bescheinigung
    lässt sich damit nicht verhindern, aber sie ist danach für jeden
    sichtbar, und der Betroffene kann sie finden.

    Returns:
        Abbildung mit dem Befund.
    """
    return {"logged": True, "prevents issuance": False,
            "detectable after the fact": True,
            "who checks": "the domain owner, by monitoring the logs",
            "enforced by": "browsers requiring a proof of inclusion"}


def what_a_certificate_says():
    """Hält fest, was in einem Zertifikat steht und was nicht.

    Es sagt, dass ein bestimmter Schlüssel zu einem bestimmten Namen
    gehört, und dass eine Stelle das geprüft hat. Es sagt nichts darüber,
    wer den Dienst betreibt oder ob er vertrauenswürdig ist.
    """
    return {"binds": "a name to a key",
            "asserted by": "the issuing authority",
            "does not say": ["who runs the service",
                             "whether the operator can be trusted",
                             "whether the software behind it is sound"]}
