"""Rechte an Dateien unter UNIX."""

import re

LEVELS = ("owner", "group", "others")
PERMISSIONS = ("read", "write", "execute")


def permissions():
    """Nennt die drei Rechte, die vergeben werden können."""
    return list(PERMISSIONS)


def levels():
    """Nennt die drei Ebenen, an die sie vergeben werden."""
    return list(LEVELS)


def parse(mode):
    """Zerlegt eine Rechtezeichenkette wie ``-rwsr-xr-x``.

    Returns:
        Abbildung mit ``kind``, den drei Ebenen als Mengen und den
        Sonderbits ``setuid``, ``setgid`` und ``sticky``.

    Raises:
        ValueError: wenn die Zeichenkette nicht zehn Zeichen hat oder
            unbekannte Zeichen enthält.
    """
    if not re.fullmatch(r"[-dlbcps][-rwxsStT]{9}", mode or ""):
        raise ValueError("keine gueltige Rechtezeichenkette")
    kinds = {"-": "file", "d": "directory", "l": "link", "b": "block device",
             "c": "character device", "p": "pipe", "s": "socket"}
    result = {"kind": kinds[mode[0]], "setuid": mode[3] in "sS",
              "setgid": mode[6] in "sS", "sticky": mode[9] in "tT"}
    for index, level in enumerate(LEVELS):
        block = mode[1 + 3 * index:4 + 3 * index]
        granted = set()
        if block[0] == "r":
            granted.add("read")
        if block[1] == "w":
            granted.add("write")
        if block[2] in "xst":
            granted.add("execute")
        result[level] = granted
    return result


def to_octal(mode):
    """Rechnet eine Rechtezeichenkette in die oktale Schreibweise um.

    Sind Sonderbits gesetzt, steht ihre Ziffer voran.
    """
    parsed = parse(mode)
    digits = ""
    for level in LEVELS:
        value = 0
        if "read" in parsed[level]:
            value += 4
        if "write" in parsed[level]:
            value += 2
        if "execute" in parsed[level]:
            value += 1
        digits += str(value)
    special = 0
    if parsed["setuid"]:
        special += 4
    if parsed["setgid"]:
        special += 2
    if parsed["sticky"]:
        special += 1
    return (str(special) if special else "") + digits


def may(mode, level, permission):
    """Sagt, ob eine Ebene ein Recht an der Datei hat.

    Raises:
        ValueError: bei unbekannter Ebene oder unbekanntem Recht.
    """
    if level not in LEVELS:
        raise ValueError("unbekannte Ebene")
    if permission not in PERMISSIONS:
        raise ValueError("unbekanntes Recht")
    return permission in parse(mode)[level]


def parliament_listing():
    """Wertet die Auflistung aus Aufgabe 1.2 aus.

    Returns:
        Abbildung von Dateinamen auf die Feststellungen, die sich aus der
        Zeile ablesen lassen.
    """
    rows = [("-rw-rw-r--", "schlz", "ampel", "coalition.pptx"),
            ("drwx------", "mrkl", "mrkl", "g8-topics"),
            ("-rw-r-----", "sphn", "ministry-health", "ffp2-invoice.pdf"),
            ("-rwsr-xr-x", "root", "root", "omicron.sh")]
    report = {}
    for mode, owner, group, name in rows:
        parsed = parse(mode)
        if "read" in parsed["others"]:
            readable = "everyone"
        elif "read" in parsed["group"]:
            readable = "the owner and the group"
        else:
            readable = "the owner only"
        entry = {"kind": parsed["kind"], "owner": owner, "group": group,
                 "readable by": readable, "octal": to_octal(mode)}
        if parsed["setuid"]:
            entry["runs as"] = owner
            entry["note"] = ("anyone may run it and it runs with the "
                             "owner's rights")
        report[name] = entry
    return report


def umask(default, mask):
    """Wendet eine Maske auf die voreingestellten Rechte an.

    Die Maske nimmt Rechte weg; sie vergibt keine.

    Raises:
        ValueError: bei Werten ausserhalb von 0 bis 0o777.
    """
    if not 0 <= default <= 0o777 or not 0 <= mask <= 0o777:
        raise ValueError("Werte liegen ausserhalb von 0 bis 0o777")
    return default & ~mask & 0o777


def why_setuid_is_dangerous():
    """Erklärt, was an einem gesetzten setuid-Bit heikel ist.

    Das Programm läuft mit den Rechten seines Besitzers, nicht denen des
    Aufrufers. Ein Fehler darin ist damit ein Fehler mit fremden Rechten,
    und bei root heisst das mit allen.
    """
    return {"runs with": "the owner's rights",
            "called by": "anyone with execute permission",
            "a bug becomes": "a privilege escalation",
            "rule": "as few setuid programs as possible, and each one small"}
