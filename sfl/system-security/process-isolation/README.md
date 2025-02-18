# Process isolation

Each process gets its own address space, and reading another's raises rather
than returning a value. Shared memory is the exception both sides arrange
explicitly, and the module models exactly that: a page becomes visible only
after both processes agree to share it.

The measures, from the hardware upwards: virtual memory so each process sees
its own addresses, privilege rings so user code cannot execute privileged
instructions, system calls as the only checked door into the kernel,
namespaces so a process sees only part of the system, and sandboxing to
narrow the set of calls it may make at all.

## What it does not close

Isolation closes the storage channel and not the timing channel. The address
spaces are separate; the cache, the bus and the processor are not, and their
load stays measurable from both sides. `against_covert_channels` returns that
pair of answers, and it is the reason side channels are a separate subject
from access control.

Behind all of it stands one rule: every part gets exactly the rights it
needs. The measure of a design is not whether it can be broken into but how
far an attacker gets once one process is theirs.
