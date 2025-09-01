# Bootstrapping and T-diagrams

A compiler has three languages: the one it translates, the one it produces, and
the one it is written in. A T-diagram keeps them apart, and it can execute
exactly when the third one is the machine's own language.

Every bootstrapping trick is two diagrams combined in one of two ways, which is
what the sheet asks to sketch.

**Translating the implementation language.** A compiler `[P -> M | I1]` fed to a
compiler `[I1 -> I2 | I2]` gives `[P -> M | I2]`. Source and target are
untouched; the compiler now runs somewhere else and still does the same job.

**Composing through an intermediate language.** A front end `[P -> Z | M]` and a
back end `[Z -> M | M]` give `[P -> M | M]`, provided both run on the same
machine. This is why intermediate languages exist: `n` languages and `m`
machines need `n + m` pieces rather than `n * m` compilers.

## The three-step bootstrap

Compiling a language in itself is a chicken-and-egg problem, and the way out is
three diagrams:

| step | result |
|---|---|
| 1. compile a **subset** compiler written in an existing language | `[P0 -> M \| M]` |
| 2. compile the **full** compiler, written in that subset | `[P -> M \| M]` |
| 3. recompile the full compiler **with itself** | `[P -> M \| M]` |

Steps 2 and 3 produce diagrams that look identical, and that is the point. Step
3 changes nothing about what the compiler accepts and everything about what it
was built with: the language is now self-hosting, and the original host is
never needed again.

## Cross compilation

The same diagrams cover porting. A back end emitting code for a new machine
while still running on the old one is step 1 of a bootstrap performed across two
machines, which is how every new architecture gets its first compiler.
