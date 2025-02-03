# Format strings

The output function reads its specifiers from the format string and fetches
one argument per specifier. It does not know how many arguments it was given,
so it keeps reading past them and into the stack.

`render("%x %x %x", stack=[1, 2, 3])` with no arguments reads three values
from the stack; `render("hello", ...)` reads none. The difference is entirely
in who wrote the format string.

## What it gives an attacker

Reading the stack with repeated `%x` reveals canaries, pointers and the
layout, which is the leak the canary module needs. `%s` with an address
placed in the buffer reads any memory. And `%n` writes the number of
characters printed so far to an address, which turns the leak into an
arbitrary write; the width field controls the value.

`can_write` marks `%n` as the dangerous one and `%x` as harmless by
comparison.

## The fix is one character

`printf(user_text)` is the mistake, `printf("%s", user_text)` is the fix. The
first treats the user's text as a program, the second as data. Compilers warn
about it, but only where they can see the format string as a literal, so it
survives wherever the string comes from a variable or a translation table.
