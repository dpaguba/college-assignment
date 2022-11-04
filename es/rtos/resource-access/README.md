# Resource access protocols

| protocol | blocking per task | deadlock |
|---|---|---|
| none | unbounded | possible |
| priority inheritance | one section per resource | possible |
| priority ceiling | one section in total | impossible |

Priority inheritance raises the holder of a resource to the priority of the
task waiting for it, which bounds the blocking by the lengths of the critical
sections. It does not prevent a chain of them, and it does not prevent
deadlock.

The ceiling protocol gives every resource the priority of the highest task
that may use it and refuses a lock that could start a chain. A task is then
blocked at most once, for at most one critical section, whatever the number
of resources, and deadlock becomes impossible because a cycle cannot form.

Blocking enters the schedulability test as an extra term in the response
time, so a protocol is not only a correctness measure: it changes the number
the analysis produces, and a bound that cannot be computed cannot be
designed against.
