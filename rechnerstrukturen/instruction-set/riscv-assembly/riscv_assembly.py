"""RISC-V assembly: executing it, and writing it in transfer notation.

The exercise asks for each instruction's effect in register transfer notation,
`Reg[13] := Reg[14] + Reg[15]`, which is exactly what the machine does in one
step. Producing that notation and executing the instruction from the same
parsed form keeps the two descriptions from drifting apart.

Register `x0` is hard-wired to zero. Writing to it is legal and has no effect,
which is what makes `addi x0, x0, 0` the canonical no-operation and `ori a1,
x0, 30` the canonical way to load a small constant.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "riscv-encoding"))
import riscv_encoding as enc


def parse(line):
    """Parse one assembly line into a dictionary."""
    text = line.split("#")[0].strip()
    if not text:
        return None

    name, _, rest = text.partition(" ")
    operands = [part.strip() for part in rest.split(",") if part.strip()]

    if name in ("lw", "sw"):
        register_name = operands[0]
        offset, _, base = operands[1].partition("(")
        return {"name": name, "rd": register_name,
                "rs1": base.rstrip(")"), "immediate": int(offset or 0)}

    if name in ("bne", "beq"):
        return {"name": name, "rs1": operands[0], "rs2": operands[1],
                "target": operands[2]}

    if name in ("addi", "ori", "andi"):
        return {"name": name, "rd": operands[0], "rs1": operands[1],
                "immediate": int(operands[2])}

    return {"name": name, "rd": operands[0], "rs1": operands[1], "rs2": operands[2]}


def transfer_notation(instruction):
    """The instruction's effect in register transfer notation."""
    name = instruction["name"]

    if name in ("add", "sub", "and", "or"):
        symbol = {"add": "+", "sub": "-", "and": "&", "or": "|"}[name]
        return (f"Reg[{enc.register(instruction['rd'])}] := "
                f"Reg[{enc.register(instruction['rs1'])}] {symbol} "
                f"Reg[{enc.register(instruction['rs2'])}]")

    if name in ("addi", "ori", "andi"):
        symbol = {"addi": "+", "ori": "|", "andi": "&"}[name]
        return (f"Reg[{enc.register(instruction['rd'])}] := "
                f"Reg[{enc.register(instruction['rs1'])}] {symbol} "
                f"{instruction['immediate']}")

    if name == "lw":
        return (f"Reg[{enc.register(instruction['rd'])}] := "
                f"Mem[Reg[{enc.register(instruction['rs1'])}] + "
                f"{instruction['immediate']}]")

    if name == "sw":
        return (f"Mem[Reg[{enc.register(instruction['rs1'])}] + "
                f"{instruction['immediate']}] := "
                f"Reg[{enc.register(instruction['rd'])}]")

    if name in ("bne", "beq"):
        comparison = "!=" if name == "bne" else "=="
        return (f"if Reg[{enc.register(instruction['rs1'])}] {comparison} "
                f"Reg[{enc.register(instruction['rs2'])}] then PC := "
                f"{instruction['target']}")

    raise ValueError(f"no notation for {name}")


class Machine:
    """Thirty-two registers, a word-addressed memory and a program counter."""

    def __init__(self):
        """Start with every register and the program counter at zero."""
        self.registers = [0] * 32
        self.memory = {}
        self.pc = 0

    def execute(self, instruction):
        """Execute one instruction, returning what it did."""
        name = instruction["name"]

        if name in ("add", "sub", "and", "or"):
            left = self.registers[enc.register(instruction["rs1"])]
            right = self.registers[enc.register(instruction["rs2"])]
            value = {"add": left + right, "sub": left - right,
                     "and": left & right, "or": left | right}[name]
            self._write(instruction["rd"], value)
            return {"branch_taken": False}

        if name in ("addi", "ori", "andi"):
            left = self.registers[enc.register(instruction["rs1"])]
            immediate = instruction["immediate"]
            value = {"addi": left + immediate, "ori": left | immediate,
                     "andi": left & immediate}[name]
            self._write(instruction["rd"], value)
            return {"branch_taken": False}

        if name == "lw":
            address = self.registers[enc.register(instruction["rs1"])] \
                + instruction["immediate"]
            self._write(instruction["rd"], self.memory.get(address, 0))
            return {"branch_taken": False}

        if name == "sw":
            address = self.registers[enc.register(instruction["rs1"])] \
                + instruction["immediate"]
            self.memory[address] = self.registers[enc.register(instruction["rd"])]
            return {"branch_taken": False}

        if name in ("bne", "beq"):
            left = self.registers[enc.register(instruction["rs1"])]
            right = self.registers[enc.register(instruction["rs2"])]
            taken = (left != right) if name == "bne" else (left == right)
            return {"branch_taken": taken}

        raise ValueError(f"cannot execute {name}")

    def _write(self, name, value):
        """Write a register, ignoring writes to `x0`.

        The hard-wired zero is not a convention the assembler enforces, it is
        the hardware: the register file simply has no storage for that number.
        Simulating it any other way makes idioms like `ori a1, x0, 30` behave
        differently on the model than on the machine.
        """
        number = enc.register(name)
        if number != 0:
            self.registers[number] = value

    def run(self, program, limit=10000):
        """Run an assembled program until it falls off the end."""
        self.pc = 0
        steps = 0

        while 0 <= self.pc < len(program) and steps < limit:
            instruction, labels = program[self.pc], program.labels
            result = self.execute(instruction)
            steps += 1

            if result["branch_taken"]:
                self.pc = labels[instruction["target"]]
            else:
                self.pc += 1

        return steps


class Program(list):
    """A list of instructions with a label table."""

    def __init__(self, instructions, labels):
        """Store the instructions and where each label points."""
        super().__init__(instructions)
        self.labels = labels


def assemble(text):
    """Parse a program, resolving labels to instruction indices."""
    instructions = []
    labels = {}

    for line in text.strip().splitlines():
        stripped = line.split("#")[0].strip()
        if not stripped:
            continue
        if stripped.endswith(":"):
            labels[stripped[:-1]] = len(instructions)
            continue
        parsed = parse(stripped)
        if parsed:
            instructions.append(parsed)

    return Program(instructions, labels)
