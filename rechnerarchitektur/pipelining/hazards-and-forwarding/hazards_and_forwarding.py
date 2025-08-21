"""Hazard classification, forwarding, and the cost of each kind.

Three data hazards, and only one of them is a real dependence:

| name | pattern | real |
|---|---|---|
| RAW | read after write | **yes** |
| WAR | write after read | no |
| WAW | write after write | no |

RAW is a dependence of the computation: the second instruction needs a value
the first produces. WAR and WAW are dependences of the **naming**: they exist
only because two instructions happen to use the same register, and renaming
removes them, which is what Tomasulo's algorithm does.
"""

from __future__ import annotations


def classify(first, second):
    """The hazard between two instructions, or `None`."""
    if first.destination and first.destination in second.sources:
        return "RAW"
    if first.destination and second.destination == first.destination:
        return "WAW"
    if second.destination and second.destination in first.sources:
        return "WAR"
    return None


def is_true_dependence(hazard):
    """Whether a hazard reflects the computation rather than the register names."""
    return hazard == "RAW"


def forwarding_saves(first, second):
    """Whether forwarding removes the stall between two instructions.

    It removes the stall for an arithmetic producer and only shortens it for a
    load: the loaded value is not available until the memory stage, one cycle
    after the consumer would need it.
    """
    if classify(first, second) != "RAW":
        return False
    return not first.is_load


def branch_penalty(resolved_in, fetch_stage=1):
    """Cycles lost when a branch is taken, given where it is resolved.

    Every stage between fetch and resolution holds an instruction fetched on
    the assumption that the branch fell through, and each must be discarded.
    Moving the resolution earlier is the cheapest branch optimisation there is,
    and it is why the classic MIPS pipeline computes the target in decode.
    """
    return max(0, resolved_in - fetch_stage)


def cpi_with_stalls(base_cpi, stalls_per_instruction):
    """The CPI a stall rate produces."""
    return base_cpi + stalls_per_instruction


def cpi_with_branches(base_cpi, branch_fraction, taken_fraction, penalty):
    """CPI including the branch penalty.

    Only taken branches cost, so the penalty is weighted twice: by how many
    instructions are branches and by how many of those are taken. A predictor
    reduces the second factor without touching the first, which is why
    prediction accuracy matters more than branch frequency.
    """
    return base_cpi + branch_fraction * taken_fraction * penalty


def cpi_with_memory(base_cpi, miss_rate, miss_penalty, accesses_per_instruction=1.0):
    """CPI including memory stalls, the other half of the CPI equation."""
    return base_cpi + accesses_per_instruction * miss_rate * miss_penalty


def dependences(program):
    """Every hazard between every pair of instructions in order."""
    found = []
    for index, first in enumerate(program):
        for offset, second in enumerate(program[index + 1:], index + 1):
            hazard = classify(first, second)
            if hazard:
                found.append((index, offset, hazard))
    return found


def critical_path(program):
    """The longest chain of true dependences, which bounds any schedule.

    No reordering can make a program shorter than its critical path, so the
    difference between the path and the actual schedule is what scheduling and
    renaming can still win. Counting only RAW edges is the point: the other two
    kinds are removable and do not belong in the bound.
    """
    longest = {}

    for index, instruction in enumerate(program):
        best = 1
        for earlier in range(index):
            if classify(program[earlier], instruction) == "RAW":
                best = max(best, longest[earlier] + 1)
        longest[index] = best

    return max(longest.values()) if longest else 0
