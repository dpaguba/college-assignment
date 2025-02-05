"""Stapelwächter: ein Wert, dessen Veränderung den Überlauf verrät."""

import random


def layout(buffer_size, width=8):
    """Beschreibt die Lage des Wächters im Rahmen.

    Er liegt zwischen dem Puffer und den gesicherten Daten, damit jede
    zusammenhängende Kopie über das Pufferende ihn zwangsläufig trifft.

    Raises:
        ValueError: bei einer negativen Puffergrösse.
    """
    if buffer_size < 0:
        raise ValueError("negative Puffergroesse")
    return {"buffer": 0, "canary": buffer_size,
            "saved rbp": buffer_size + width,
            "return address": buffer_size + 2 * width}


def run(input_length, buffer_size, canary=True, width=8):
    """Führt eine Kopie aus und prüft danach den Wächter.

    Args:
        input_length: Länge der kopierten Daten.
        buffer_size: Grösse des Puffers.
        canary: ob ein Wächter gesetzt ist.
        width: Breite des Wächters.

    Returns:
        Abbildung mit dem Befund und dem Ausgang.

    Raises:
        ValueError: bei negativen Werten.
    """
    if input_length < 0 or buffer_size < 0:
        raise ValueError("negative Werte")
    positions = layout(buffer_size, width)
    canary_touched = input_length > positions["canary"]
    return_touched = input_length > positions["return address"]
    if not canary_touched:
        return {"detected": False, "outcome": "normal",
                "canary": canary}
    if canary:
        return {"detected": True, "outcome": "aborted", "canary": True,
                "message": "stack smashing detected"}
    return {"detected": False,
            "outcome": "control flow hijacked" if return_touched
            else "corrupted", "canary": False}


def when_checked():
    """Sagt, wann der Wächter geprüft wird und was das bedeutet.

    Geprüft wird beim Verlassen der Funktion. Bis dahin ist der Überlauf
    längst geschehen: was er auf dem Weg überschrieben hat, wirkt bereits.
    Der Wächter verhindert die Übernahme des Rücksprungs, nicht den
    Schaden davor.
    """
    return {"set at": "function entry", "checked at": "function return",
            "damage may already be done": True,
            "protects": "the return address",
            "does not protect": "other locals, or data reached before the "
                                "return"}


def leaked_canary(buffer_size=16, width=8):
    """Zeigt, was ein bekannter Wächterwert ändert.

    Wer den Wert kennt, etwa durch eine Ausgabe, die zu viel verrät,
    schreibt ihn beim Überlauf einfach wieder hin. Die Prüfung findet ihn
    unverändert vor.

    Returns:
        Abbildung mit dem Befund.
    """
    secret = random.Random(1).getrandbits(64)
    leaked = secret
    written_back = leaked
    return {"detected": written_back != secret,
            "canary known to the attacker": True,
            "how it leaks": "a format string, an uninitialised read, or an "
                            "error message that prints too much"}


def non_contiguous_write(buffer_size=16, width=8):
    """Zeigt einen Schreibzugriff, der den Wächter überspringt.

    Ein Index, der aus einer Eingabe berechnet wird, schreibt an eine
    beliebige Stelle statt fortlaufend über das Pufferende. Der Wächter
    liegt dazwischen und wird nie berührt.

    Returns:
        Abbildung mit dem Befund.
    """
    positions = layout(buffer_size, width)
    written_offset = positions["return address"]
    touched_canary = written_offset == positions["canary"]
    return {"detected": touched_canary, "written at": written_offset,
            "canary at": positions["canary"],
            "why": "the write is indexed, not sequential"}


def kinds():
    """Nennt die Bauarten des Wächters."""
    return {"terminator": "contains bytes that end a string copy, such as "
                          "the null byte",
            "random": "a value drawn at start up and kept in a register",
            "random xor": "the random value combined with the return "
                          "address, so a partial leak is not enough"}


def cost():
    """Nennt, was der Wächter kostet.

    Zwei Speicherzugriffe und ein Vergleich je Funktion mit einem Puffer,
    und ein Rahmen, der um acht Byte wächst. Übersetzer setzen ihn deshalb
    nur dort ein, wo ein Feld auf dem Stapel liegt.
    """
    return {"per protected function": "one store, one load, one compare",
            "frame grows by": "the width of the canary",
            "applied to": "functions with a local array, unless forced"}
