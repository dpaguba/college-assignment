# Readers and writers

Three policies, and the property each one gives up.

| Policy | Starves a reader | Starves a writer | Concurrency with 5 readers and 1 writer |
|---|---|---|---|
| reader priority | no | yes | 5 |
| writer priority | yes | no | 1 |
| fair (arrival order) | no | no | 1 |

Reader priority admits a reader whenever any reader holds the lock, so a
steady stream of readers postpones the writer indefinitely. Writer priority
mirrors it. The fair policy serves in arrival order and starves nobody, and it
pays for that by serialising: a writer that arrived early blocks the readers
behind it even though they could all have run together.

There is no policy that maximises concurrency and starves nobody, and the
table is the reason. Concurrency comes from letting later readers join a run
in progress, and joining a run in progress is exactly what postpones the
writer.

## When the lock is not worth it

A reader-writer lock has more state to update than a mutex, so it costs more
per acquisition. It repays that only when reads are frequent *and* long enough
for the parallelism to matter. Short critical sections run faster under a
plain mutex, which is the measurement that decides between them rather than
the shape of the workload on paper.
