# Stack canaries

A value placed between the buffer and the saved data, set on entry and
checked on return. A sequential copy past the end of the buffer must cross
it, so the check fails and the program aborts instead of returning into the
attacker's address.

Measured on an eight-byte buffer with the canary at offset 8, the saved base
pointer at 16 and the return address at 24:

| input length | with canary | without |
|---|---|---|
| 4 | normal | normal |
| 20 | aborted | corrupted |
| 32 | aborted | control flow hijacked |

The middle row is worth reading twice. Twenty bytes pass the canary and reach
the saved base pointer but not the return address: without the canary the
frame is corrupt and the flow is not yet hijacked. Reaching the return
address needs the whole frame.

## Three ways past it

The canary is checked at the return, so whatever the overflow did on the way
has already happened. It protects the return address and not the other
locals.

A leaked canary defeats it: the attacker writes the value back and the check
finds it unchanged. Leaks come from format strings, uninitialised reads and
error messages that print too much.

A non-sequential write defeats it too. An index computed from input writes
straight at the return address, and the canary sitting in between is never
touched.

The cost is one store, one load and one compare per protected function, plus
eight bytes of frame, which is why compilers apply it only where a local
array exists.
