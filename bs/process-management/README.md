# Processes

`fork` returns twice, which is the single strangest thing in the UNIX
interface: zero in the child, the child's id in the parent, both continuing
from the same line with the same memory. The asymmetry is deliberate, since the
child can find its parent with `getppid` and the parent has no other way to
learn the child's id.

`exec` replaces the program and keeps the identity: same process id, same open
files, same working directory. That split is what makes shell redirection
possible, because the child adjusts its own descriptors between the two calls.

## The two commands that look alike

| command | runs | output goes to |
|---|---|---|
| `ls -l > sort` | **one** program | a **file** named `sort` |
| `ls -l \| sort` | **two** programs | the second program's input |

The trap in the exercise is that the file in the first case is named after the
program in the second. They share almost nothing.

## Zombies and orphans

A terminated process keeps its exit status until someone reads it, and until
then it is a zombie holding a process table slot.

| situation | outcome |
|---|---|
| child exits, parent does not wait | zombie |
| parent then waits | reaped |
| parent exits first | child is reparented to init and keeps running |
| orphan then exits | init reaps it automatically |

That last row is why init exists as process 1: it waits in a loop and does
nothing else.

## The fork bomb

`for (;;) fork();` doubles the process count every generation: 1, 2, 4, 8, and
1024 after ten. That is why it makes a machine unusable in seconds and why
process limits are a per-user setting rather than a global one.

## fork against vfork

`vfork` skipped the address space copy for the case where the child
immediately calls `exec`, and copy-on-write made `fork` nearly as cheap by
sharing pages until one side writes. What is left is a marginal saving and a
large footgun: the child shares the parent's stack, so returning from the
calling function corrupts the parent.
