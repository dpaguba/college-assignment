"""A five-stage pipeline, simulated cycle by cycle.

Fetch, decode, execute, memory, write back. One instruction still takes five
cycles; what changes is that five of them are in flight at once, so the
throughput approaches one instruction per cycle while the latency stays the
same.

The simulation exists so that the CPI comes out of a mechanism rather than a
formula. Every claim about stalls in the neighbouring modules is checked
against what the pipeline actually does.
"""

from __future__ import annotations

STAGES = ["IF", "ID", "EX", "MEM", "WB"]
"""The classic five stages, in order."""


class Instruction:
    """One instruction: an operation, a destination and its source registers."""

    def __init__(self, operation, destination, sources, is_load=False,
                 is_branch=False):
        """Record the operation and the registers it reads and writes."""
        self.operation = operation
        self.destination = destination
        self.sources = list(sources)
        self.is_load = is_load
        self.is_branch = is_branch

    def __repr__(self):
        """The instruction in assembler-like form."""
        return f"{self.operation} {self.destination}, {', '.join(self.sources)}"


def simulate(program, forwarding=True):
    """Run the program through the pipeline, counting cycles and stalls.

    An instruction issues when its operands are ready. Without forwarding an
    operand is ready only after the producer's write-back; with forwarding it
    is ready after the producer's execute, except for a load, whose value
    arrives one stage later and cannot be forwarded to the next instruction.

    That single exception is the load-use hazard, and it is why compilers
    schedule an unrelated instruction after every load.
    """
    ready = {}
    finish = {}
    occupancy = {}
    stalls = 0
    cycle = 1

    for index, instruction in enumerate(program):
        earliest = cycle

        for source in instruction.sources:
            if source in ready:
                earliest = max(earliest, ready[source])

        stalls += earliest - cycle
        cycle = earliest

        for offset, stage in enumerate(STAGES):
            occupancy.setdefault(cycle + offset, []).append(stage)

        if instruction.destination:
            ready[instruction.destination] = cycle + _delay(instruction, forwarding)

        finish[index] = cycle + len(STAGES) - 1
        cycle += 1

    total = max(finish.values()) if finish else 0
    return {"cycles": total, "stalls": stalls,
            "cpi": total / len(program) if program else 0.0,
            "finish": finish, "occupancy": occupancy}


def _delay(instruction, forwarding):
    """How many cycles later a consumer may issue without stalling.

    Counted in issue cycles rather than in stages, which is what makes the
    three cases comparable. A producer issued in cycle `p` computes in `p+2`
    and reaches memory in `p+3`.

    | case | consumer may issue at |
    |---|---|
    | forwarding, arithmetic | `p+1`, so back to back is free |
    | forwarding, load | `p+2`, one instruction of distance |
    | no forwarding | `p+3`, the value comes from the register file |
    """
    if not forwarding:
        return 3
    return 2 if instruction.is_load else 1


def steady_state_cpi(result, program):
    """CPI with the pipeline fill removed.

    The fill costs `depth - 1` cycles once, so the measured CPI of a short
    program is dominated by it: 60 instructions in a five-stage pipeline carry
    4 extra cycles, which is 0.067 of CPI and nothing to do with stalls.
    Comparing a stall formula against a measurement means comparing this.
    """
    return (result["cycles"] - (len(STAGES) - 1)) / len(program)


def ideal_cycles(count):
    """Cycles for a perfect pipeline: fill it once, then one per instruction."""
    return len(STAGES) + count - 1


def speedup_over_sequential(count):
    """Pipelined against unpipelined, for a perfect pipeline.

    Approaches the number of stages and never reaches it, because the pipeline
    has to fill and drain. At 100 instructions a five-stage pipeline is 4.8
    times faster, not 5, and the gap is the fill cost divided by the work.
    """
    return (len(STAGES) * count) / ideal_cycles(count)


def utilisation(result):
    """Fraction of stage slots actually occupied.

    Stalls show up here as empty slots, which is the same information as the
    CPI seen from the hardware's side rather than the program's.
    """
    slots = sum(len(stages) for stages in result["occupancy"].values())
    return slots / (result["cycles"] * len(STAGES))
