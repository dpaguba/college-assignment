# Betriebssysteme

The course material is the practical half: three assignments and their
tutorials, no lecture slides. The library covers the concepts those
assignments and their theory questions are about.

| Topic | |
|---|---|
| [process-management](process-management/) | fork, exec, wait, zombies, the fork bomb |
| [scheduling](scheduling/) | first come first served to virtual round robin |
| [synchronisation](synchronisation/) | races, mutexes, semaphores, bounded buffers |
| [deadlocks](deadlocks/) | the four conditions, detection, the banker's algorithm |

The C programs the assignments ask for are in
[bs-practice](../bs-practice/), one folder per task.

## The measurement worth keeping

The assignment's unsynchronised thread program gives the **wrong** answer in 90
of 300 runs and the right one in 210. A race is not a bug that shows up when
you run the program; it is a bug that shows up when you run it enough times,
which is why the fix is reasoned about rather than tested for.
