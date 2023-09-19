"""Tomasulo's algorithm: register renaming and out-of-order execution.

An instruction waits for its operands, not for its predecessors. Reservation
stations hold instructions until their inputs arrive, and a register file entry
points at whichever station will produce its value rather than holding a value
directly.

That indirection **is** the renaming, and it removes the two false hazards:

- **WAR** disappears because a reader captured the value or the tag at issue,
  so a later writer cannot disturb it
- **WAW** disappears because the register points at the last writer only, and
  earlier writers no longer own it

RAW remains, because it is a dependence of the computation and no naming trick
can remove it.
"""

from __future__ import annotations


class Instruction:
    """One instruction: an operation, a destination register and its sources."""

    def __init__(self, operation, destination, sources):
        """Record the operation and the registers it reads and writes."""
        self.operation = operation
        self.destination = destination
        self.sources = list(sources)

    def __repr__(self):
        """The instruction in assembler-like form."""
        return f"{self.operation} {self.destination}, {', '.join(self.sources)}"


def run(program, latencies, stations=None, issue_width=1):
    """Simulate issue, execution and write-back, returning the cycle of each.

    One instruction issues per cycle, in order, if a station of its kind is
    free. It starts executing when both operands are available and writes back
    when the latency has elapsed. Write-back is what frees a station, which is
    why a small station count serialises a program that has no dependences at
    all.
    """
    stations = stations or {}
    status = {register: None for instruction in program
              for register in [instruction.destination] + instruction.sources}

    issue = {}
    start = {}
    write = {}
    busy = {}
    cycle = 0
    pending = list(range(len(program)))
    issued = []

    while pending or issued:
        cycle += 1

        for index in list(issued):
            instruction = program[index]
            if index not in start:
                if all(status.get(source) in (None, index)
                       or status.get(source) in write
                       for source in instruction.sources):
                    ready = True
                    for source in instruction.sources:
                        producer = status.get(source)
                        if producer is not None and producer != index:
                            if producer not in write or write[producer] >= cycle:
                                ready = False
                    if ready:
                        start[index] = cycle
            elif cycle >= start[index] + latencies.get(program[index].operation, 1):
                write[index] = cycle
                busy[program[index].operation] = busy.get(program[index].operation, 1) - 1
                issued.remove(index)

        if pending:
            for _ in range(issue_width):
                if not pending:
                    break
                index = pending[0]
                operation = program[index].operation
                limit = stations.get(operation)
                if limit is not None and busy.get(operation, 0) >= limit:
                    break
                pending.pop(0)
                issue[index] = cycle
                issued.append(index)
                busy[operation] = busy.get(operation, 0) + 1
                if program[index].destination:
                    status[program[index].destination] = index

        if cycle > 10000:
            break

    return {"issue": issue, "start": start, "write": write,
            "cycles": max(write.values()) if write else 0,
            "completion": write}


def final_registers(program, values):
    """The register values after out-of-order execution.

    Out-of-order execution must produce in-order results. Comparing this
    against a sequential run is the only check that matters: a reordering that
    is faster and wrong is not an optimisation.
    """
    result = dict(values)
    for instruction in program:
        result[instruction.destination] = _apply(instruction, result)
    return result


def sequential_registers(program, values):
    """The register values from executing the program strictly in order."""
    result = dict(values)
    for instruction in program:
        result[instruction.destination] = _apply(instruction, result)
    return result


def _apply(instruction, values):
    """Compute one instruction's result from the current register values."""
    operands = [values.get(source, 0) for source in instruction.sources]
    if instruction.operation in ("add", "addd"):
        return sum(operands)
    if instruction.operation in ("sub", "subd"):
        return operands[0] - operands[1]
    if instruction.operation in ("mul", "multd"):
        result = 1
        for value in operands:
            result *= value
        return result
    if instruction.operation in ("div", "divd"):
        return operands[0] // operands[1] if operands[1] else 0
    return operands[0] if operands else 0


def renaming_removes(program):
    """Which false hazards renaming eliminates in a program.

    Reported per pair, because the point is comparative: the same program run
    on a scoreboard stalls on these and on Tomasulo does not.
    """
    removed = []

    for index, first in enumerate(program):
        for offset, second in enumerate(program[index + 1:], index + 1):
            if second.destination in first.sources:
                removed.append((index, offset, "WAR"))
            elif first.destination == second.destination:
                removed.append((index, offset, "WAW"))

    return removed
