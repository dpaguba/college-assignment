"""Bootstrapping and T-diagrams.

A compiler has three languages, not one: the language it translates, the
language it produces, and the language it is written in. A T-diagram is the
notation that keeps them apart, and every bootstrapping trick is two diagrams
combined in one of two ways.

The chicken-and-egg problem is real. A compiler for a language written in that
same language cannot be run until it has been compiled, and the way out is to
write a small subset compiler in something else, then use it to compile the
full compiler, then use that to compile itself.
"""

from __future__ import annotations


class DiagramError(Exception):
    """Two diagrams cannot be combined because their languages do not match."""


class Compiler:
    """A T-diagram: source language, target language, implementation language."""

    def __init__(self, source, target, implementation):
        """Fix the three languages of one T-diagram."""
        self.source = source
        self.target = target
        self.implementation = implementation

    def runs_on(self, machine):
        """Whether this compiler can execute on a given machine.

        It can exactly when it is written in that machine's own language.
        Everything else about bootstrapping follows from this one condition.
        """
        return self.implementation == machine

    def __repr__(self):
        """The diagram in the usual `S -> T` form, with the implementation."""
        return f"[{self.source} -> {self.target} | {self.implementation}]"

    def __eq__(self, other):
        """Two diagrams are equal when all three languages agree."""
        return (isinstance(other, Compiler) and self.source == other.source
                and self.target == other.target
                and self.implementation == other.implementation)


def translate(compiler, translator):
    """Compile a compiler, changing its implementation language.

    The first way T-diagrams combine. A compiler written in `I1` is fed to a
    compiler from `I1` to `I2`, and the result is the same compiler written in
    `I2`. Source and target are untouched, which is the point: the compiler
    now runs somewhere else and still does the same job.
    """
    if translator.source != compiler.implementation:
        raise DiagramError(f"{translator.source} cannot compile "
                           f"{compiler.implementation}")
    return Compiler(compiler.source, compiler.target, translator.target)


def compose(front, back):
    """Chain two compilers through an intermediate language.

    The second way. A front end from `P` to `Z` and a back end from `Z` to `M`
    give a compiler from `P` to `M`, provided both run on the same machine.
    This is why intermediate languages exist: `n` languages and `m` machines
    need `n + m` pieces rather than `n * m` compilers.
    """
    if front.target != back.source:
        raise DiagramError(f"{front.target} does not match {back.source}")
    if front.implementation != back.implementation:
        raise DiagramError("both compilers must run on the same machine")
    return Compiler(front.source, back.target, front.implementation)


def bootstrap(subset, full, machine, host):
    """The classic three-step bootstrap, returning the diagram at each step.

    1. Write a compiler for a **subset** of the language, in an existing
       language, and compile it with an existing compiler. Now the subset
       compiler runs on the machine.
    2. Write the **full** compiler in that subset, and compile it with the
       result of step 1. Now the full compiler runs on the machine.
    3. Recompile the full compiler with itself. Nothing changes about what it
       accepts, and everything changes about what it was built with: the
       language is now self-hosting.

    Step 3 looks pointless and is the whole point. It proves the compiler can
    compile itself, and from then on the original host language is never
    needed again.
    """
    written_in_host = Compiler(subset, machine, host)
    host_compiler = Compiler(host, machine, machine)
    step_one = translate(written_in_host, host_compiler)

    written_in_subset = Compiler(full, machine, subset)
    step_two = translate(written_in_subset, step_one)

    written_in_full = Compiler(full, machine, full)
    step_three = translate(written_in_full, step_two)

    return [step_one, step_two, step_three]


def cross_compiler(compiler, other_machine):
    """A compiler producing code for a machine it does not run on.

    The other standard use of the diagrams. Porting a language to a new machine
    means writing a back end that emits its code while still running on the old
    one, then using it to compile the compiler for the new machine, which is
    step one of a bootstrap performed across two machines.
    """
    return Compiler(compiler.source, other_machine, compiler.implementation)
