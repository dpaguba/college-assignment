"""The datapath: what the control unit switches, and what a cycle costs.

Every instruction takes the same five steps through the same hardware: fetch,
decode and read registers, execute in the ALU, access memory, write back. What
differs is which steps do anything, and that is precisely what the control
signals say.

| instruction | reads memory | writes memory | writes a register | ALU second input |
|---|---|---|---|---|
| `add` | no | no | yes | register |
| `addi` | no | no | yes | immediate |
| `lw` | **yes** | no | yes | immediate |
| `sw` | no | **yes** | no | immediate |
| `bne` | no | no | no | register |

The table also decides the clock. A single-cycle machine must give every
instruction the whole path, so its period is the sum of all five stages, and
`add` pays for a memory access it does not make. A multicycle machine clocks
each stage separately and lets short instructions finish early.

That does **not** make it faster by itself, and the direction of the effect is
the opposite of the intuitive one. Its period is the **longest** stage, so an
unbalanced pipeline hurts it: the single-cycle machine pays for a long stage
once per instruction, and the multicycle machine pays for it in every cycle.

With a mix of 25% loads, 10% stores, 45% arithmetic and 20% branches the CPI is
4.05, and:

| stage times | single cycle | multicycle |
|---|---|---|
| 200, 100, 200, 200, 100 | 800 | 810 |
| 200 each | 1000 | **810** |
| 200, 100, 200, **800**, 100 | 1400 | 3240 |

It wins when the stages are balanced and the mix skips some of them, and its
real argument is hardware reuse: one ALU and one memory port instead of
several.
"""

from __future__ import annotations


def control(name):
    """The control signals for one instruction."""
    signals = {"mem_read": False, "mem_write": False, "register_write": False,
               "alu_source_immediate": False, "branch": False,
               "memory_to_register": False}

    if name in ("add", "sub", "and", "or"):
        signals["register_write"] = True
    elif name in ("addi", "ori", "andi"):
        signals["register_write"] = True
        signals["alu_source_immediate"] = True
    elif name == "lw":
        signals["mem_read"] = True
        signals["register_write"] = True
        signals["alu_source_immediate"] = True
        signals["memory_to_register"] = True
    elif name == "sw":
        signals["mem_write"] = True
        signals["alu_source_immediate"] = True
    elif name in ("bne", "beq"):
        signals["branch"] = True
    else:
        raise ValueError(f"no control signals for {name}")

    return signals


def alu(left, right, operation):
    """The ALU, which is the only place arithmetic happens.

    Address computation, comparison and arithmetic all go through it, which is
    why a load and an add share a datapath: `lw a3, 4(a0)` is an addition whose
    result is used as an address rather than written to a register.
    """
    if operation == "add":
        return left + right
    if operation == "sub":
        return left - right
    if operation == "and":
        return left & right
    if operation == "or":
        return left | right
    if operation == "slt":
        return int(left < right)
    raise ValueError(f"unknown ALU operation {operation}")


def branch_taken(name, alu_result):
    """Whether a branch is taken, from the ALU's zero flag.

    The comparison is a subtraction and the branch reads the zero flag, so no
    separate comparator is needed. That reuse is why `beq` and `bne` are cheap
    and why comparisons against zero are the ones every instruction set gets
    first.
    """
    zero = alu_result == 0
    if name == "beq":
        return zero
    if name == "bne":
        return not zero
    raise ValueError(f"{name} is not a branch")


STAGES = ["fetch", "decode", "execute", "memory", "writeback"]
"""The five steps, in order."""

STAGES_USED = {
    "lw": ["fetch", "decode", "execute", "memory", "writeback"],
    "sw": ["fetch", "decode", "execute", "memory"],
    "add": ["fetch", "decode", "execute", "writeback"],
    "addi": ["fetch", "decode", "execute", "writeback"],
    "bne": ["fetch", "decode", "execute"],
}
"""Which stages each instruction actually needs."""


def single_cycle_period(times):
    """Clock period of a single-cycle machine: the sum of every stage.

    Set by the longest instruction, which is the load, and paid by every
    instruction including the branch that needs three of the five stages.
    """
    return sum(times[stage] for stage in STAGES)


def multicycle_period(times):
    """Clock period of a multicycle machine: the longest single stage."""
    return max(times[stage] for stage in STAGES)


def single_cycle_time(times, mix):
    """Average time per instruction on a single-cycle machine."""
    return single_cycle_period(times)


def multicycle_time(times, mix):
    """Average time per instruction on a multicycle machine.

    Each instruction takes as many cycles as it has stages, and each cycle is
    the longest stage. The machine wins whenever the mix is dominated by short
    instructions, which every real mix is.
    """
    period = multicycle_period(times)
    return sum(share * len(STAGES_USED[name]) * period
               for name, share in mix.items())


def cycles_per_instruction(mix):
    """The CPI of a multicycle machine, from the instruction mix."""
    return sum(share * len(STAGES_USED[name]) for name, share in mix.items())
