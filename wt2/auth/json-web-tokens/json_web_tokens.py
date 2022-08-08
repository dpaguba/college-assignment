"""JSON Web Tokens: Aufbau, Signatur und die bekannten Fallen."""

import base64
import hashlib
import hmac
import json


class InvalidToken(Exception):
    """Wird geworfen, wenn eine Marke die Prüfung nicht besteht."""


def _encode_part(data):
    """Kodiert ein Datenstück nach base64url ohne Auffüllzeichen."""
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"))
    return base64.urlsafe_b64encode(raw.encode("utf-8")).rstrip(b"=").decode()


def _decode_part(text):
    """Dekodiert ein base64url-Stück und liest das JSON darin."""
    padding = "=" * (-len(text) % 4)
    return json.loads(base64.urlsafe_b64decode(text + padding))


def _sign(message, secret):
    """Bildet die Signatur über Kopf und Nutzlast."""
    digest = hmac.new(secret.encode("utf-8"), message.encode("utf-8"),
                      hashlib.sha256).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b"=").decode()


def encode(claims, secret, expires_at=None, algorithm="HS256"):
    """Stellt eine signierte Marke aus.

    Args:
        claims: die Angaben, die die Marke trägt.
        secret: das gemeinsame Geheimnis.
        expires_at: Ablaufzeitpunkt, der als ``exp`` eingetragen wird.
        algorithm: der Name im Kopf.

    Returns:
        Die Marke als drei durch Punkte getrennte Teile.
    """
    header = {"alg": algorithm, "typ": "JWT"}
    payload = dict(claims)
    if expires_at is not None:
        payload["exp"] = expires_at
    message = _encode_part(header) + "." + _encode_part(payload)
    return message + "." + _sign(message, secret)


def peek(token):
    """Liest die Nutzlast ohne jede Prüfung.

    Die Marke ist kodiert, nicht verschlüsselt: jeder, der sie hat, kann
    ihren Inhalt lesen. Ein Geheimnis gehört deshalb nicht hinein.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidToken("die Marke hat nicht drei Teile")
    return _decode_part(parts[1])


def decode(token, secret, now=None):
    """Prüft eine Marke und gibt ihre Angaben zurück.

    Geprüft werden das Verfahren im Kopf, die Signatur über Kopf und
    Nutzlast und der Ablauf.

    Raises:
        InvalidToken: bei jedem Fehlschlag.
    """
    parts = token.split(".")
    if len(parts) != 3:
        raise InvalidToken("die Marke hat nicht drei Teile")
    header_part, payload_part, signature = parts
    try:
        header = _decode_part(header_part)
    except (ValueError, TypeError) as error:
        raise InvalidToken("der Kopf ist unlesbar") from error
    if header.get("alg") != "HS256":
        raise InvalidToken("unerwartetes Verfahren: %s" % header.get("alg"))
    expected = _sign(header_part + "." + payload_part, secret)
    if not hmac.compare_digest(expected, signature):
        raise InvalidToken("die Signatur stimmt nicht")
    payload = _decode_part(payload_part)
    if "exp" in payload and now is not None and payload["exp"] <= now:
        raise InvalidToken("die Marke ist abgelaufen")
    return payload


def tamper(token, claims):
    """Ersetzt die Nutzlast einer Marke, ohne neu zu signieren.

    Das ist der Versuch, den die Signatur abfangen soll.
    """
    parts = token.split(".")
    return parts[0] + "." + _encode_part(claims) + "." + parts[2]


def forge_with_none(claims):
    """Baut eine Marke, die als Verfahren ``none`` angibt.

    Eine Prüfung, die das Verfahren aus dem Kopf übernimmt, statt es
    vorzuschreiben, akzeptiert eine solche Marke ohne Signatur. Der Kopf
    kommt vom Angreifer; er darf nicht bestimmen, wie er geprüft wird.
    """
    header = {"alg": "none", "typ": "JWT"}
    return _encode_part(header) + "." + _encode_part(claims) + "."


def signature_covers_the_header():
    """Prüft, dass eine Änderung am Kopf die Signatur ungültig macht."""
    token = encode({"user": "ada"}, secret="s")
    header_part, payload_part, signature = token.split(".")
    changed = _encode_part({"alg": "HS512", "typ": "JWT"})
    forged = changed + "." + payload_part + "." + signature
    try:
        decode(forged, secret="s")
    except InvalidToken:
        return True
    return False


def registered_claims():
    """Nennt die Angaben, die die Spezifikation vorsieht."""
    return {"iss": "who issued it", "sub": "who it is about",
            "aud": "who it is for", "exp": "when it stops being valid",
            "nbf": "when it starts being valid", "iat": "when it was issued",
            "jti": "an identifier, useful for a deny list"}
