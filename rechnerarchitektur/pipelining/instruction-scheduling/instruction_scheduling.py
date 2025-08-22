"""Instruction scheduling and loop unrolling.

A pipeline stalls when an instruction needs a value that is not ready. Moving
an unrelated instruction into the gap fills it, and that is the whole of static
scheduling: reorder without changing the meaning.

The limit is the dependence structure. A chain where each instruction needs the
previous one cannot be reordered at all, and the only way to find independent
work is to make some, which is what unrolling does.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "pipeline-simulation"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "hazards-and-forwarding"))
import hazards_and_forwarding as hf
import pipeline_simulation as ps


def schedule(program):
    """Reorder instructions to avoid stalls, keeping every dependence.

    A greedy list schedule: at each step, pick the ready instruction whose
    operands have been available longest. Ready means every instruction it
    depends on has already been placed, which covers all three hazard kinds,
    because reordering across a WAR or WAW is unsafe without renaming.
    """
    remaining = list(range(len(program)))
    placed = []
    ready_at = {}

    while remaining:
        best = None
        best_time = None

        for index in remaining:
            if not _dependences_placed(program, index, placed, remaining):
                continue
            time = _earliest(program, index, placed, ready_at)
            if best is None or time < best_time:
                best, best_time = index, time

        if best is None:
            best = remaining[0]
            best_time = _earliest(program, best, placed, ready_at)

        placed.append(best)
        remaining.remove(best)
        instruction = program[best]
        if instruction.destination:
            delay = 2 if instruction.is_load else 1
            ready_at[instruction.destination] = len(placed) + delay

    return [program[index] for index in placed]


def _dependences_placed(program, index, placed, remaining):
    """Whether every instruction this one must follow has been placed."""
    for other in remaining:
        if other >= index:
            continue
        if hf.classify(program[other], program[index]) is not None:
            return False
    return True


def _earliest(program, index, placed, ready_at):
    """The position at which an instruction could issue without stalling."""
    position = len(placed) + 1
    for source in program[index].sources:
        if source in ready_at:
            position = max(position, ready_at[source])
    return position


def respects_dependences(original, scheduled):
    """Whether a reordering preserved every hazard's direction.

    The only correctness condition a scheduler has. Checking it separately from
    the stall count matters: a scheduler that reorders freely removes every
    stall and computes the wrong answer.
    """
    positions = {id(instruction): index for index, instruction in enumerate(scheduled)}

    for index, first in enumerate(original):
        for second in original[index + 1:]:
            if hf.classify(first, second) is not None:
                if positions[id(first)] > positions[id(second)]:
                    return False

    return True


def unroll(body, times):
    """Replicate a loop body, renaming the registers of each copy.

    Unrolling by itself removes only the loop overhead. What makes it pay is
    that the copies are independent once renamed, so the scheduler has work to
    fill the stalls with. Renaming is therefore not an optimisation of
    unrolling, it is the point of it.
    """
    result = []

    for iteration in range(times):
        for instruction in body:
            destination = (f"{instruction.destination}_{iteration}"
                           if instruction.destination else None)
            sources = [f"{source}_{iteration}"
                       if any(other.destination == source for other in body)
                       else source
                       for source in instruction.sources]
            result.append(ps.Instruction(instruction.operation, destination, sources,
                                         is_load=instruction.is_load,
                                         is_branch=instruction.is_branch))

    return result


def report(program):
    """Stalls and cycles before and after scheduling, with the bound.

    The critical path is included because it says how much of the remaining
    time is irreducible: a schedule at the path length is optimal, and one
    above it is not.
    """
    before = ps.simulate(program, forwarding=True)
    scheduled = schedule(program)
    after = ps.simulate(scheduled, forwarding=True)

    return {
        "before": {"cycles": before["cycles"], "stalls": before["stalls"]},
        "after": {"cycles": after["cycles"], "stalls": after["stalls"]},
        "critical_path": hf.critical_path(program),
        "valid": respects_dependences(program, scheduled),
    }
