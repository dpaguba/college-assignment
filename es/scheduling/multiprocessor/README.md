# Several processors

Neither of the uniprocessor results survives.

**Partitioning** assigns each task to a processor once, which turns
scheduling into bin packing and inherits its waste: three tasks of
utilisation 0.6 do not fit on two processors although the total is 1.8, and
no packing rule repairs it.

**Global scheduling** lets tasks migrate and fails differently. Dhall's
effect is the standard example, reproduced here: two tiny tasks and one task
of utilisation 0.99, total 1.01 on two processors, and the deadlines are
missed. A single task cannot use more than one processor, so a heavy task
forces the bound down whatever the rest of the set looks like.

That is why the global utilisation bound is far below the processor count,
and why multiprocessor real-time scheduling is a research area rather than a
corollary of the single processor theory.
