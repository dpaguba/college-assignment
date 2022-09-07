"""Statuscodes: Klassen, Schuldfrage und die üblichen Verwechslungen."""

FAMILIES = {1: "informational", 2: "success", 3: "redirection",
            4: "client error", 5: "server error"}


def family(code):
    """Nennt die Klasse eines Statuscodes.

    Raises:
        ValueError: bei einem Code ausserhalb von 100 bis 599.
    """
    if not 100 <= code <= 599:
        raise ValueError("kein gueltiger Statuscode")
    return FAMILIES[code // 100]


def blame(code):
    """Sagt, wer den Fehler zu verantworten hat.

    Returns:
        ``client``, ``server`` oder ``nobody``.
    """
    group = family(code)
    if group == "client error":
        return "client"
    if group == "server error":
        return "server"
    return "nobody"


def for_creation(location):
    """Antwort auf eine erfolgreiche Neuanlage.

    Die Antwort nennt den Ort der neuen Ressource, damit der Aufrufer sie
    nicht suchen muss.
    """
    return {"status": 201, "headers": {"Location": location}}


def for_auth(authenticated, permitted=True):
    """Wählt zwischen fehlender Anmeldung und fehlendem Recht.

    401 heisst: es ist nicht bekannt, wer da fragt, eine Anmeldung würde
    helfen. 403 heisst: es ist bekannt, und es hilft nicht.
    """
    if not authenticated:
        return 401
    return 200 if permitted else 403


def for_stale_write():
    """Der Code für einen Schreibkonflikt.

    409 sagt, dass die Anfrage in Ordnung war und am Zustand scheitert;
    400 würde behaupten, sie sei falsch formuliert gewesen.
    """
    return 409


def common_confusions():
    """Nennt die Paare, die häufig verwechselt werden."""
    return {"401 vs 403": "unknown caller against known but not allowed",
            "400 vs 409": "malformed request against conflicting state",
            "404 vs 403": "hiding existence against admitting it",
            "500 vs 503": "broken against temporarily unavailable",
            "200 vs 204": "a body against nothing to return"}
