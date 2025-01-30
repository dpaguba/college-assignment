# Buffer overflow

The frame holds an eight-byte buffer, then the saved base pointer, then the
return address. Copying four bytes leaves both intact; copying twenty
overwrites both, which the module reports separately so the order of damage
is visible.

A bounded copy raises instead. That is the whole difference between `strcpy`
and `strncpy`, and it is a difference the language does not make for you: an
array carries no length, a string ends at a byte rather than at a bound, and
the standard functions check nothing.

## Exercise 3.3c

Passing the check without knowing the password does not require touching the
return address at all. A flag sits next to the buffer, and an input one byte
longer than the buffer overwrites it. The password comparison then fails,
the flag is non-zero, and access is granted. The module returns the input,
the real password, the failed comparison and the granted access side by side.

## The two kinds

A stack overflow overwrites the saved base pointer and the return address, so
the function returns where the attacker chooses. A heap overflow overwrites
the allocator's bookkeeping, so a later free or allocation writes where the
attacker chooses. Both turn a write past the end into control over the
program.

The defences, strongest first: bounded functions, a language that checks its
indices, canaries, a non-executable stack, address randomisation, and
compiler warnings that are actually read.
