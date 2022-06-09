"""LOOP, WHILE and GOTO programs: computation without a tape.

Three tiny imperative languages over natural-number registers. They are in the
course because they make the Church-Turing thesis concrete: a model that looks
nothing like a Turing machine turns out to compute exactly the same functions.

    LOOP    assignment, sequence, and a loop that runs a fixed number of times
    WHILE   the same, plus a loop that runs while a register is non-zero
    GOTO    labelled statements with conditional and unconditional jumps

**LOOP is strictly weaker.** Every LOOP program halts, because the repetition
count is fixed when the loop starts, so the class it computes is exactly the
primitive recursive functions, and the Ackermann function is the standard
witness that this is a real restriction.

**WHILE and GOTO are equivalent**, and both are equivalent to Turing machines.
The conversions are short and are here.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class Statement:
    """Base class of program statements."""


@dataclass
class Assign(Statement):
    """``x := y + c`` or ``x := y - c``, with truncated subtraction."""

    target: str
    source: str
    offset: int = 0
    subtract: bool = False

    def __str__(self):
        """The assignment in the notation the lecture uses."""
        operator = "-" if self.subtract else "+"
        return f"{self.target} := {self.source} {operator} {self.offset}"


@dataclass
class Sequence(Statement):
    """A list of statements run in order."""

    parts: tuple

    def __str__(self):
        """The parts, separated by semicolons."""
        return "; ".join(str(part) for part in self.parts)


@dataclass
class Loop(Statement):
    """``LOOP x DO body END``: repeat exactly as often as x says.

    The count is read **once**, when the loop starts. Changing x inside the
    body does not change how often it runs, and that single rule is what makes
    every LOOP program terminate.
    """

    register: str
    body: Statement

    def __str__(self):
        """The bounded loop in the lecture's notation."""
        return f"LOOP {self.register} DO {self.body} END"


@dataclass
class While(Statement):
    """``WHILE x != 0 DO body END``: repeat while x is non-zero.

    The test is re-read every round, which is exactly what LOOP forbids, and
    exactly what makes non-termination possible.
    """

    register: str
    body: Statement

    def __str__(self):
        """The unbounded loop in the lecture's notation."""
        return f"WHILE {self.register} != 0 DO {self.body} END"


def run(program, registers, limit=100000):
    """Run a LOOP or WHILE program on a register state.

    Returns the final registers. Raises when the step limit is reached, which
    can only happen for a WHILE program: a LOOP program always halts.
    """
    state = dict(registers)
    steps = [0]

    def execute(statement):
        """Runs one statement, counting the step against the limit."""
        steps[0] += 1
        if steps[0] > limit:
            raise RuntimeError("the program did not halt within the step limit")

        if isinstance(statement, Assign):
            value = state.get(statement.source, 0)
            result = value - statement.offset if statement.subtract else value + statement.offset
            state[statement.target] = max(0, result)

        elif isinstance(statement, Sequence):
            for part in statement.parts:
                execute(part)

        elif isinstance(statement, Loop):
            for _ in range(state.get(statement.register, 0)):
                execute(statement.body)

        elif isinstance(statement, While):
            while state.get(statement.register, 0) != 0:
                execute(statement.body)

        else:
            raise TypeError(f"not a statement: {statement!r}")

    execute(program)
    return state


def uses_while(program):
    """Whether the program contains a WHILE, which decides if it can loop for ever."""
    if isinstance(program, While):
        return True
    if isinstance(program, Sequence):
        return any(uses_while(part) for part in program.parts)
    if isinstance(program, Loop):
        return uses_while(program.body)
    return False


def loop_to_while(program, counter="_c"):
    """Rewrite a LOOP as a WHILE, which is the easy direction.

    A fresh counter is copied from the register **before** the loop and counted
    down inside it. Copying first is the whole point: it preserves the LOOP
    semantics that the body cannot change how often it runs.
    """
    if isinstance(program, Loop):
        body = loop_to_while(program.body)
        fresh = f"{counter}{id(program) % 1000}"
        return Sequence((
            Assign(fresh, program.register, 0),
            While(fresh, Sequence((body, Assign(fresh, fresh, 1, subtract=True)))),
        ))

    if isinstance(program, Sequence):
        return Sequence(tuple(loop_to_while(part, counter) for part in program.parts))

    if isinstance(program, While):
        return While(program.register, loop_to_while(program.body, counter))

    return program


@dataclass
class Goto:
    """A GOTO program: a list of labelled instructions.

    Each instruction is one of

    - ``("assign", target, source, offset, subtract)``
    - ``("if", register, value, label)`` for a conditional jump
    - ``("goto", label)``
    - ``("halt",)``
    """

    instructions: list
    name: str = "P"

    def run(self, registers, limit=100000):
        """Run the program, returning the final registers."""
        state = dict(registers)
        counter = 0
        steps = 0

        while 0 <= counter < len(self.instructions):
            steps += 1
            if steps > limit:
                raise RuntimeError("the program did not halt within the step limit")

            instruction = self.instructions[counter]
            kind = instruction[0]

            if kind == "halt":
                break

            if kind == "assign":
                _, target, source, offset, subtract = instruction
                value = state.get(source, 0)
                state[target] = max(0, value - offset if subtract else value + offset)
                counter += 1

            elif kind == "goto":
                counter = instruction[1]

            elif kind == "if":
                _, register, value, label = instruction
                counter = label if state.get(register, 0) == value else counter + 1

            else:
                raise TypeError(f"unknown instruction {instruction!r}")

        return state

    def __str__(self):
        """The instructions, numbered, as a jump target refers to them."""
        rows = [f"{self.name}:"]
        for index, instruction in enumerate(self.instructions):
            rows.append(f"  {index}: {instruction}")
        return "\n".join(rows)


def while_to_goto(program, name="goto"):
    """Compile a WHILE program into jumps.

    A while loop becomes a test that jumps past the body when the register is
    zero, and an unconditional jump back at the end. That is all a compiler
    does with a loop, and seeing it in ten lines is the point of the exercise.
    """
    instructions = []

    def emit(statement):
        """Appends the instructions a statement translates into."""
        if isinstance(statement, Assign):
            instructions.append(("assign", statement.target, statement.source,
                                 statement.offset, statement.subtract))

        elif isinstance(statement, Sequence):
            for part in statement.parts:
                emit(part)

        elif isinstance(statement, While):
            test = len(instructions)
            instructions.append(None)
            emit(statement.body)
            instructions.append(("goto", test))
            instructions[test] = ("if", statement.register, 0, len(instructions))

        elif isinstance(statement, Loop):
            emit(loop_to_while(statement))

        else:
            raise TypeError(f"not a statement: {statement!r}")

    emit(program)
    instructions.append(("halt",))
    return Goto(instructions, name)


def goto_to_while(program, counter="_pc", name=None):
    """Simulate a GOTO program with a single WHILE loop.

    A program counter register holds which instruction is next, and the loop
    body is a chain of tests, one per instruction. The direction that looks
    harder is the one that shows why the two languages are equally strong: a
    single unbounded loop can carry arbitrary control flow.

    Returned as a runnable closure rather than a WHILE syntax tree, because the
    chain of tests needs equality on the counter and the tiny WHILE language
    here has no conditional. The construction is the same either way, and this
    keeps the language small.
    """
    def execute(registers, limit=100000):
        """Runs the goto program with the program counter held in a register."""
        state = dict(registers)
        state[counter] = 0
        steps = 0

        while state[counter] < len(program.instructions):
            steps += 1
            if steps > limit:
                raise RuntimeError("the program did not halt within the step limit")

            instruction = program.instructions[state[counter]]
            kind = instruction[0]

            if kind == "halt":
                break
            if kind == "assign":
                _, target, source, offset, subtract = instruction
                value = state.get(source, 0)
                state[target] = max(0, value - offset if subtract else value + offset)
                state[counter] += 1
            elif kind == "goto":
                state[counter] = instruction[1]
            else:
                _, register, value, label = instruction
                state[counter] = label if state.get(register, 0) == value else state[counter] + 1

        del state[counter]
        return state

    execute.name = name or f"while({program.name})"
    return execute


def addition(left="x", right="y", target="z"):
    """``z := x + y``, in LOOP: add one to a copy of x as often as y says."""
    return Sequence((
        Assign(target, left, 0),
        Loop(right, Assign(target, target, 1)),
    ))


def multiplication(left="x", right="y", target="z", helper="_t"):
    """``z := x * y``, in LOOP: add x as often as y says."""
    return Sequence((
        Assign(target, target, 0, subtract=True),
        Assign(target, "_zero", 0),
        Loop(right, Sequence((
            Assign(helper, left, 0),
            Loop(helper, Assign(target, target, 1)),
        ))),
    ))


def ackermann_while():
    """The Ackermann function, which no LOOP program computes.

    Implemented with an explicit stack in a WHILE loop, since the language has
    no recursion. It grows faster than any primitive recursive function, which
    is exactly the theorem that separates LOOP from WHILE, and the reason the
    separation is not a matter of convenience.
    """
    def compute(first, second, limit=200000):
        """Evaluates the function with an explicit stack instead of recursion."""
        stack = [first]
        value = second
        steps = 0

        while stack:
            steps += 1
            if steps > limit:
                raise RuntimeError("the computation exceeded the step limit")

            level = stack.pop()
            if level == 0:
                value += 1
            elif value == 0:
                stack.append(level - 1)
                value = 1
            else:
                stack.append(level - 1)
                stack.append(level)
                value -= 1

        return value

    return compute
