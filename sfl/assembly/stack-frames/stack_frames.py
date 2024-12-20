"""Der Stapelrahmen einer Funktion."""

ARGUMENT_REGISTERS = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")


class Stack:
    """Ein Stapel, der wie auf x86 nach unten wächst."""

    def __init__(self, top=0x1000, width=8):
        """Legt einen leeren Stapel an.

        Args:
            top: die höchste Adresse.
            width: Breite eines Eintrags in Byte.
        """
        self.top = top
        self.width = width
        self.pointer = top
        self.cells = {}

    def push(self, value):
        """Legt einen Wert ab; der Zeiger wandert nach unten."""
        self.pointer -= self.width
        self.cells[self.pointer] = value
        return self.pointer

    def pop(self):
        """Nimmt den obersten Wert.

        Raises:
            IndexError: wenn der Stapel leer ist.
        """
        if self.pointer >= self.top:
            raise IndexError("der Stapel ist leer")
        value = self.cells.pop(self.pointer)
        self.pointer += self.width
        return value

    def peek(self, offset=0):
        """Liest einen Wert relativ zum Stapelzeiger."""
        return self.cells.get(self.pointer + offset * self.width)


def build_frame(locals_size, width=8):
    """Beschreibt den Aufbau eines Rahmens.

    Von unten nach oben: die lokalen Variablen, der gesicherte
    Basiszeiger, die Rückkehradresse. Ein Überlauf einer lokalen Variablen
    schreibt daher zuerst über den Basiszeiger und dann über die
    Rückkehradresse.

    Args:
        locals_size: Grösse der lokalen Variablen in Byte.
        width: Breite eines Eintrags.

    Returns:
        Abbildung mit ``layout`` von unten nach oben und den ``offsets``.

    Raises:
        ValueError: bei negativer Grösse.
    """
    if locals_size < 0:
        raise ValueError("negative Groesse")
    return {"layout": ["locals", "saved rbp", "return address"],
            "offsets": {"locals": 0, "saved rbp": locals_size,
                        "return address": locals_size + width},
            "frame size": locals_size + 2 * width}


def calling_convention():
    """Nennt die Aufrufkonvention von System V für x86-64."""
    return {"integer arguments": list(ARGUMENT_REGISTERS),
            "further arguments": "on the stack, right to left",
            "return value": "rax",
            "callee saved": ["rbx", "rbp", "r12", "r13", "r14", "r15"],
            "caller saved": ["rax", "rcx", "rdx", "rsi", "rdi", "r8", "r9",
                             "r10", "r11"]}


def place_arguments(count):
    """Verteilt Argumente auf Register und Stapel.

    Returns:
        Liste von Abbildungen mit ``index`` und ``where``.

    Raises:
        ValueError: bei einer negativen Anzahl.
    """
    if count < 0:
        raise ValueError("negative Anzahl")
    placement = []
    for index in range(count):
        if index < len(ARGUMENT_REGISTERS):
            placement.append({"index": index, "where": "register",
                              "name": ARGUMENT_REGISTERS[index]})
        else:
            placement.append({"index": index, "where": "stack",
                              "name": "rsp+%d" % (8 * (index
                                                       - len(ARGUMENT_REGISTERS)))})
    return placement


def prologue_and_epilogue():
    """Nennt die Befehle, die einen Rahmen auf- und abbauen."""
    return {"prologue": ["push rbp", "mov rbp, rsp", "sub rsp, n"],
            "epilogue": ["mov rsp, rbp", "pop rbp", "ret"],
            "shortcut": "leave does the first two of the epilogue"}


def why_the_return_address_is_the_target():
    """Erklärt, warum ein Überlauf gerade die Rückkehradresse trifft.

    Ein Puffer liegt unter der Rückkehradresse und wird nach oben
    beschrieben. Wer über sein Ende hinausschreibt, erreicht daher zuerst
    den gesicherten Basiszeiger und dann die Adresse, zu der die Funktion
    zurückspringt: der Angreifer muss nichts suchen, die Richtung der
    Schreiboperation führt ihn hin.
    """
    return {"buffer grows": "upwards", "stack grows": "downwards",
            "consequence": "an overflow runs straight into the saved data"}
