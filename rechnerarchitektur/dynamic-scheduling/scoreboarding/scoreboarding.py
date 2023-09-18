"""Scoreboarding: out-of-order execution without renaming.

The CDC 6600's answer to the same problem Tomasulo solves, ten years earlier
and one idea short. A scoreboard tracks which functional unit will write each
register and stalls whenever an instruction would violate any of the three
hazards.

Because there is no renaming, the false hazards still stall:

- **WAR** stalls the *write-back*, since an earlier instruction may not have
  read the register yet
- **WAW** stalls the *issue*, since two instructions writing the same register
  must do so in order

Comparing the two algorithms on the same program is the clearest way to see
what renaming buys, and the tests do exactly that.
"""

from __future__ import annotations


def run(program, latencies, units=None):
    """Simulate the four scoreboard stages, returning the cycle of each.

    Issue, read operands, execute, write back. Issue stalls on a structural
    hazard or a WAW; read operands stalls on a RAW; write-back stalls on a WAR.
    Those three rules are the whole algorithm.

    A read waits only for a producer **earlier in program order**. A later
    instruction that will overwrite the same register is a WAR hazard, and the
    scoreboard handles it by delaying that instruction's write-back, not by
    delaying the earlier read: the reader is entitled to the old value. Getting
    this backwards deadlocks the simulation, because each instruction then
    waits for the other.

    The simulation reads the state at the start of a cycle and applies every
    change at the end of it, the way synchronous hardware works. Updating in
    place instead makes the result depend on the order the instructions happen
    to sit in the list: a dependent instruction would read a value in the same
    cycle the producer wrote it, which is one cycle too early and hides the
    difference this module exists to show.
    """
    units = units or {}
    result_of = {}
    issue = {}
    read = {}
    write = {}
    cycle = 0
    pending = list(range(len(program)))
    active = []

    while (pending or active) and cycle < 10000:
        cycle += 1
        to_read = []
        to_write = []
        to_issue = None

        for index in active:
            instruction = program[index]

            if index not in read:
                waiting = [source for source in instruction.sources
                           if result_of.get(source) is not None
                           and result_of[source] < index]
                if not waiting:
                    to_read.append(index)
                continue

            if cycle >= read[index] + latencies.get(instruction.operation, 1):
                blocked = any(
                    other < index and other not in read
                    and instruction.destination in program[other].sources
                    for other in active)
                if not blocked:
                    to_write.append(index)

        if pending:
            index = pending[0]
            instruction = program[index]
            operation = instruction.operation
            in_flight = sum(1 for other in active
                            if program[other].operation == operation)
            limit = units.get(operation)

            if not (limit is not None and in_flight >= limit) \
                    and result_of.get(instruction.destination) is None:
                to_issue = index

        for index in to_read:
            read[index] = cycle
        for index in to_write:
            write[index] = cycle
            if result_of.get(program[index].destination) == index:
                result_of[program[index].destination] = None
            active.remove(index)


        if to_issue is not None:
            pending.pop(0)
            issue[to_issue] = cycle
            active.append(to_issue)
            result_of[program[to_issue].destination] = to_issue

    return {"issue": issue, "read": read, "write": write,
            "cycles": max(write.values()) if write else 0,
            "completion": write}


def false_hazard_cost(program, latencies, units=None):
    """How much later each instruction writes on a scoreboard than on Tomasulo.

    Reported per instruction rather than as a total, because the total often
    hides it. On the classic example, `div f0` then `add f10, f0, f8` then
    `sub f8, f8, f14`, both machines finish in 25 cycles, since the division is
    the critical path either way. The `sub` writes in cycle **6** under
    Tomasulo and cycle **24** under the scoreboard, an 18-cycle WAR stall,
    because the scoreboard must wait for `add` to read the old `f8`.

    A total-cycle comparison would call that zero, which is exactly the mistake
    the per-instruction view avoids.
    """
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", "tomasulo"))
    import tomasulo as tm

    board = run(program, latencies, units)
    renamed = tm.run(program, latencies)

    return {index: board["write"].get(index, 0) - renamed["write"].get(index, 0)
            for index in range(len(program))}
