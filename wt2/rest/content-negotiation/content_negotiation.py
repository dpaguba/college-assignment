"""Aushandlung des Formats über den Accept-Kopf."""


def parse_accept(header):
    """Zerlegt einen Accept-Kopf in Medientypen mit ihrer Güte.

    Fehlt die Güte, gilt eins. Die Reihenfolge im Kopf bleibt erhalten,
    damit sie bei gleicher Güte entscheiden kann.

    Returns:
        Liste von Tripeln (Medientyp, Güte, Position).

    Raises:
        ValueError: bei einem leeren Kopf.
    """
    if not header or not header.strip():
        raise ValueError("leerer Accept-Kopf")
    entries = []
    for position, piece in enumerate(header.split(",")):
        parts = [part.strip() for part in piece.split(";")]
        media = parts[0]
        quality = 1.0
        for part in parts[1:]:
            if part.startswith("q="):
                quality = float(part[2:])
        entries.append((media, quality, position))
    return entries


def _specificity(media):
    """Bewertet, wie genau ein Muster ist; genauer schlägt allgemeiner."""
    if media == "*/*":
        return 0
    if media.endswith("/*"):
        return 1
    return 2


def _matches(pattern, offered):
    """Sagt, ob ein angebotener Typ auf ein Muster passt."""
    if pattern == "*/*":
        return True
    if pattern.endswith("/*"):
        return offered.split("/", 1)[0] == pattern.split("/", 1)[0]
    return pattern == offered


def choose(header, offered):
    """Wählt das Format, das beide Seiten am besten bedient.

    Entschieden wird zuerst nach der Güte, dann nach der Genauigkeit des
    Musters, dann nach der Reihenfolge im Kopf.

    Args:
        header: der Accept-Kopf des Aufrufers.
        offered: die Formate, die der Dienst liefern kann.

    Returns:
        Der gewählte Medientyp oder None, wenn nichts passt.
    """
    best = None
    for media, quality, position in parse_accept(header):
        if quality <= 0:
            continue
        for candidate in offered:
            if not _matches(media, candidate):
                continue
            key = (quality, _specificity(media), -position)
            if best is None or key > best[0]:
                best = (key, candidate)
    return best[1] if best else None


def status_for_no_match():
    """Der Statuscode, wenn kein angebotenes Format passt."""
    return 406


def dimensions():
    """Nennt, worüber sich Aufrufer und Dienst einigen können."""
    return {"Accept": "media type",
            "Accept-Language": "language",
            "Accept-Encoding": "compression",
            "Accept-Charset": "character set"}


def vary_header():
    """Erklärt, warum die Antwort sagen muss, wonach sie sich richtet.

    Ein Zwischenspeicher, der die Antwort ohne diesen Hinweis aufbewahrt,
    liefert sie später an einen Aufrufer aus, der ein anderes Format
    verlangt hat.
    """
    return {"header": "Vary", "value": "Accept",
            "without it": "a cache may serve the wrong representation"}
