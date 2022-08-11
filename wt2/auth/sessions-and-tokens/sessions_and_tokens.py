"""Sitzungen auf dem Server gegen Wertmarken beim Aufrufer."""

import hashlib
import hmac
import os


class SessionServer:
    """Ein Server, der zu jeder Anmeldung einen Eintrag behält."""

    def __init__(self):
        """Legt einen Server ohne Sitzungen an."""
        self.sessions = {}

    def log_in(self, user):
        """Meldet einen Benutzer an und gibt die Sitzungskennung zurück."""
        identifier = os.urandom(16).hex()
        self.sessions[identifier] = user
        return identifier

    def user_of(self, identifier):
        """Nennt den Benutzer einer Sitzung, oder None."""
        return self.sessions.get(identifier)

    def log_out(self, identifier):
        """Beendet eine Sitzung; die Kennung ist sofort wertlos."""
        self.sessions.pop(identifier, None)


def issue_token(user, secret, expires_at=None):
    """Stellt eine selbsttragende Wertmarke aus.

    Die Marke enthält die Angaben und eine Signatur; der Server braucht
    nichts zu speichern, um sie später zu prüfen.
    """
    payload = "%s|%s" % (user, "" if expires_at is None else expires_at)
    signature = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"),
                         hashlib.sha256).hexdigest()
    return payload + "|" + signature


def read_token(token, secret, now=None):
    """Prüft eine Wertmarke und gibt ihre Angaben zurück.

    Raises:
        ValueError: bei falscher Signatur oder abgelaufener Marke.
    """
    parts = token.split("|")
    if len(parts) != 3:
        raise ValueError("unbrauchbare Wertmarke")
    user, expires, signature = parts
    payload = "%s|%s" % (user, expires)
    expected = hmac.new(secret.encode("utf-8"), payload.encode("utf-8"),
                        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise ValueError("Signatur stimmt nicht")
    if expires and now is not None and int(expires) <= now:
        raise ValueError("Wertmarke ist abgelaufen")
    return {"user": user,
            "expires at": int(expires) if expires else None}


def revocation_report():
    """Vergleicht, wie schnell sich beides zurücknehmen lässt.

    Eine Sitzung wird durch Löschen des Eintrags sofort ungültig. Eine
    Wertmarke gilt bis zu ihrem Ablauf, weil der Server nichts hat, was er
    löschen könnte.

    Returns:
        Abbildung mit beiden Antworten.
    """
    server = SessionServer()
    session = server.log_in("ada")
    server.log_out(session)
    session_dead = server.user_of(session) is None
    token = issue_token("ada", secret="s", expires_at=1000)
    still_valid = True
    try:
        read_token(token, secret="s", now=10)
    except ValueError:
        still_valid = False
    return {"session revoked at once": session_dead,
            "token revoked at once": not still_valid,
            "token valid until": 1000}


def storage_report(users, bytes_per_session=64):
    """Vergleicht, was der Server je Benutzer aufbewahren muss.

    Returns:
        Abbildung mit beiden Werten in Byte.
    """
    if users < 0:
        raise ValueError("negative Benutzerzahl")
    return {"session bytes": users * bytes_per_session, "token bytes": 0,
            "users": users}


def deny_list_report():
    """Zeigt, was eine Sperrliste für Wertmarken kostet.

    Damit sich eine Marke doch zurücknehmen lässt, muss der Server sie
    vermerken. Die Zustandslosigkeit, das eigentliche Argument für die
    Marke, ist damit dahin.

    Returns:
        Abbildung mit dem Erfolg der Rücknahme und der Zahl der Einträge.
    """
    denied = set()
    token = issue_token("ada", secret="s")
    denied.add(token)
    return {"revoked": token in denied, "entries kept": len(denied),
            "stateless": False}


def comparison():
    """Stellt beide Wege gegenüber."""
    return {"session": {"state": "on the server", "revocation": "immediate",
                        "scaling": "needs a shared store"},
            "token": {"state": "with the caller", "revocation": "at expiry",
                      "scaling": "nothing to share"}}
