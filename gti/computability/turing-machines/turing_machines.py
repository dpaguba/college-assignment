"""Turing machines: the model everything else is measured against.

A finite control, an infinite tape, and a head that reads, writes and moves one
cell. The Church-Turing thesis says this is all computation is, and the
evidence is that every other model anyone proposed turned out to accept exactly
the same languages.

A transition maps ``(state, symbol)`` to ``(state, symbol to write, direction)``
with direction L, R or N. Missing entries mean the machine halts, which is why
a rejecting state is optional: halting without accepting is rejection.
"""

from __future__ import annotations

from dataclasses import dataclass, field

BLANK = "_"
LEFT, RIGHT, STAY = "L", "R", "N"


@dataclass
class Tape:
    """An unbounded tape, stored as the cells that have been touched."""

    cells: dict = field(default_factory=dict)
    position: int = 0

    @classmethod
    def of(cls, word, blank=BLANK):
        """A tape holding a word, head on the first symbol."""
        return cls({index: symbol for index, symbol in enumerate(word)}, 0)

    def read(self, blank=BLANK):
        """The symbol under the head."""
        return self.cells.get(self.position, blank)

    def write(self, symbol):
        """Overwrite the cell under the head."""
        self.cells[self.position] = symbol

    def move(self, direction):
        """Move the head one cell, or stay."""
        if direction == LEFT:
            self.position -= 1
        elif direction == RIGHT:
            self.position += 1

    def contents(self, blank=BLANK):
        """The written part of the tape as a string, blanks trimmed."""
        if not self.cells:
            return ""
        low, high = min(self.cells), max(self.cells)
        text = "".join(self.cells.get(index, blank) for index in range(low, high + 1))
        return text.strip(blank)

    def snapshot(self, blank=BLANK, width=3):
        """The tape around the head, with the head position marked."""
        low = min(list(self.cells) + [self.position]) - width
        high = max(list(self.cells) + [self.position]) + width
        parts = []
        for index in range(low, high + 1):
            symbol = self.cells.get(index, blank)
            parts.append(f"[{symbol}]" if index == self.position else symbol)
        return "".join(parts)

    def copy(self):
        """An independent copy, so a run cannot disturb the caller's tape."""
        return Tape(dict(self.cells), self.position)


@dataclass
class TuringMachine:
    """A deterministic Turing machine."""

    states: set
    input_alphabet: tuple
    tape_alphabet: tuple
    transitions: dict
    start: str
    accept: str
    reject: str = None
    blank: str = BLANK
    name: str = "M"

    def step(self, state, tape):
        """One transition, or None when the machine halts."""
        symbol = tape.read(self.blank)
        move = self.transitions.get((state, symbol))
        if move is None:
            return None

        target, written, direction = move
        tape.write(written)
        tape.move(direction)
        return target

    def run(self, word, limit=10000, trace=False):
        """Run on an input and report how it ended.

        Returns the outcome, the tape and the number of steps. The outcome is
        ``accept``, ``reject`` or ``limit``, and the third one is the accurate
        answer for a machine that has not halted yet: nothing here can tell a
        slow computation from a non-terminating one, which is the halting
        problem in one sentence.
        """
        tape = Tape.of(word, self.blank)
        state = self.start
        history = [(state, tape.snapshot(self.blank))] if trace else None

        for steps in range(limit):
            if state == self.accept:
                return {"outcome": "accept", "tape": tape, "steps": steps, "trace": history}
            if self.reject is not None and state == self.reject:
                return {"outcome": "reject", "tape": tape, "steps": steps, "trace": history}

            following = self.step(state, tape)
            if following is None:
                outcome = "accept" if state == self.accept else "reject"
                return {"outcome": outcome, "tape": tape, "steps": steps, "trace": history}

            state = following
            if trace:
                history.append((state, tape.snapshot(self.blank)))

        return {"outcome": "limit", "tape": tape, "steps": limit, "trace": history}

    def accepts(self, word, limit=10000):
        """Whether the machine accepts, with the step limit as a rejection."""
        return self.run(word, limit)["outcome"] == "accept"

    def compute(self, word, limit=10000):
        """The tape contents after halting, which is the output of a computation."""
        result = self.run(word, limit)
        return result["tape"].contents(self.blank) if result["outcome"] != "limit" else None

    def language(self, max_length, limit=2000):
        """Every accepted word up to a length, over the input alphabet."""
        found = []
        queue = [""]

        while queue:
            word = queue.pop(0)
            if self.accepts(word, limit):
                found.append(word)
            if len(word) < max_length:
                queue.extend(word + symbol for symbol in self.input_alphabet)

        return found

    def __str__(self):
        """The transition table, one row per rule."""
        rows = [f"{self.name}: start {self.start}, accept {self.accept}"
                + (f", reject {self.reject}" if self.reject else "")]
        for (state, symbol), (target, written, direction) in sorted(
                self.transitions.items(), key=lambda item: str(item[0])):
            rows.append(f"  ({state}, {symbol}) -> ({target}, {written}, {direction})")
        return "\n".join(rows)


def equal_counts():
    """Accepts ``a^n b^n``: cross off one a and one b at a time.

    The classic first Turing machine, and worth comparing with the pushdown
    automaton for the same language: the stack version pushes and pops, this
    one walks back and forth over the tape. Same language, and the tape can do
    much more.
    """
    transitions = {
        ("scan", "a"): ("right", "X", RIGHT),
        ("scan", "Y"): ("verify", "Y", RIGHT),
        ("scan", BLANK): ("accept", BLANK, STAY),

        ("right", "a"): ("right", "a", RIGHT),
        ("right", "Y"): ("right", "Y", RIGHT),
        ("right", "b"): ("back", "Y", LEFT),

        ("back", "a"): ("back", "a", LEFT),
        ("back", "Y"): ("back", "Y", LEFT),
        ("back", "X"): ("scan", "X", RIGHT),

        ("verify", "Y"): ("verify", "Y", RIGHT),
        ("verify", BLANK): ("accept", BLANK, STAY),
    }
    return TuringMachine({"scan", "right", "back", "verify", "accept"}, ("a", "b"),
                         ("a", "b", "X", "Y", BLANK), transitions,
                         "scan", "accept", None, BLANK, "a^n b^n")


def three_equal_blocks():
    """Accepts ``a^n b^n c^n``, which no pushdown automaton can.

    The language the [CFL pumping lemma](../../context-free/cfl-pumping-lemma/)
    rules out one level down. A Turing machine does it by crossing off one of
    each in turn, and that is the clearest single demonstration that the tape
    is strictly stronger than the stack.
    """
    transitions = {
        ("scan", "a"): ("findb", "X", RIGHT),
        ("scan", "Y"): ("checkY", "Y", RIGHT),
        ("scan", BLANK): ("accept", BLANK, STAY),

        ("findb", "a"): ("findb", "a", RIGHT),
        ("findb", "Y"): ("findb", "Y", RIGHT),
        ("findb", "b"): ("findc", "Y", RIGHT),

        ("findc", "b"): ("findc", "b", RIGHT),
        ("findc", "Z"): ("findc", "Z", RIGHT),
        ("findc", "c"): ("back", "Z", LEFT),

        ("back", "a"): ("back", "a", LEFT),
        ("back", "b"): ("back", "b", LEFT),
        ("back", "Y"): ("back", "Y", LEFT),
        ("back", "Z"): ("back", "Z", LEFT),
        ("back", "X"): ("scan", "X", RIGHT),

        ("checkY", "Y"): ("checkY", "Y", RIGHT),
        ("checkY", "Z"): ("checkZ", "Z", RIGHT),
        ("checkZ", "Z"): ("checkZ", "Z", RIGHT),
        ("checkZ", BLANK): ("accept", BLANK, STAY),
    }
    return TuringMachine({"scan", "findb", "findc", "back", "checkY", "checkZ", "accept"},
                         ("a", "b", "c"), ("a", "b", "c", "X", "Y", "Z", BLANK), transitions,
                         "scan", "accept", None, BLANK, "a^n b^n c^n")


def successor():
    """Adds one to a binary number, as an example of computing rather than deciding.

    A Turing machine is not only an acceptor. Reading the output off the tape
    after halting is what makes it a model of computation, and every later
    reduction relies on that reading.
    """
    transitions = {
        ("right", "0"): ("right", "0", RIGHT),
        ("right", "1"): ("right", "1", RIGHT),
        ("right", BLANK): ("add", BLANK, LEFT),

        ("add", "1"): ("add", "0", LEFT),
        ("add", "0"): ("done", "1", LEFT),
        ("add", BLANK): ("done", "1", LEFT),

        ("done", "0"): ("done", "0", LEFT),
        ("done", "1"): ("done", "1", LEFT),
        ("done", BLANK): ("accept", BLANK, RIGHT),
    }
    return TuringMachine({"right", "add", "done", "accept"}, ("0", "1"),
                         ("0", "1", BLANK), transitions, "right", "accept",
                         None, BLANK, "binary successor")
