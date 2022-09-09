"""Cross-site request forgery und die Massnahmen dagegen."""

import hmac
import os


class Server:
    """Ein Server, der Sitzungen führt und Überweisungen entgegennimmt."""

    def __init__(self, require_token=True):
        """Legt einen Server an.

        Args:
            require_token: ob eine Anfrage eine Marke mitbringen muss.
        """
        self.sessions = {}
        self.tokens = {}
        self.balance = 1000
        self.require_token = require_token

    def log_in(self, user):
        """Meldet einen Benutzer an und legt eine Marke für ihn bereit."""
        session = os.urandom(8).hex()
        self.sessions[session] = user
        self.tokens[session] = os.urandom(16).hex()
        return session

    def token_for(self, session):
        """Gibt die Marke einer Sitzung heraus.

        Der Angreifer kann die Anfrage im Namen des Opfers stellen, weil
        der Browser die Sitzungskarte mitschickt. An diese Marke kommt er
        nicht, weil er die Antwort der fremden Herkunft nicht lesen darf.
        """
        return self.tokens.get(session)

    def transfer(self, session, amount, token=None):
        """Führt eine Überweisung aus, wenn alles stimmt.

        Returns:
            Abbildung mit dem Ergebnis und dem Grund einer Ablehnung.
        """
        if session not in self.sessions:
            return {"accepted": False, "reason": "not logged in"}
        if self.require_token:
            expected = self.tokens.get(session)
            if token is None or not hmac.compare_digest(str(expected),
                                                        str(token)):
                return {"accepted": False, "reason": "token missing or wrong"}
        self.balance -= amount
        return {"accepted": True, "balance": self.balance}


def attack_report(protected):
    """Spielt den Angriff durch: eine fremde Seite stellt die Anfrage.

    Der Browser des Opfers schickt die Sitzungskarte mit, weil sie zur
    Adresse des Servers gehört. Die Marke kennt der Angreifer nicht.

    Returns:
        Abbildung mit dem Erfolg und dem Kontostand.
    """
    server = Server(require_token=protected)
    session = server.log_in("ada")
    before = server.balance
    result = server.transfer(session, amount=500, token=None)
    return {"succeeded": result["accepted"], "before": before,
            "after": server.balance, "protected": protected}


def is_dangerous(method, changes_state):
    """Sagt, ob eine Anfrage sich besonders leicht fälschen lässt.

    Eine Anfrage, die den Zustand ändert und dabei eine sichere Methode
    benutzt, lässt sich mit einem Bild auslösen, ohne dass der Benutzer
    etwas anklickt.
    """
    from_safe = method in ("GET", "HEAD")
    return from_safe and changes_state


def same_site_blocks(setting, cross_site):
    """Sagt, ob die Sitzungskarte bei einer fremden Herkunft mitgeht.

    Raises:
        ValueError: bei einer unbekannten Einstellung.
    """
    if setting not in ("strict", "lax", "none"):
        raise ValueError("unbekannte Einstellung")
    if not cross_site:
        return False
    return setting in ("strict", "lax")


def defences():
    """Nennt die Massnahmen und was jede leistet."""
    return {"token in the form": "the attacker cannot read it",
            "same site cookie": "the browser does not send the card",
            "check the origin header": "the browser states where it came from",
            "no state change on GET": "removes the easiest way in",
            "ask again for the important step": "the last line"}


def why_the_browser_helps_the_attacker():
    """Erklärt, warum der Angriff überhaupt geht.

    Der Browser hängt die Sitzungskarte an jede Anfrage an die Adresse,
    zu der sie gehört, ohne zu fragen, wer die Anfrage ausgelöst hat. Das
    ist gewollt und der Grund, aus dem eine Anmeldung über mehrere Seiten
    hinweg funktioniert.
    """
    return {"the cookie is attached by destination, not by origin": True,
            "the attacker never sees the answer": True,
            "so the attack is blind but effective": True}
