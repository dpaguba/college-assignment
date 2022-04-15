# Betriebssysteme, practical assignments

The C programs the three assignments ask for, one folder per task.

| Folder | Assignment |
|---|---|
| [fibonacci](fibonacci/) | 0, the C warm-up |
| [shell-menu](shell-menu/) | 1, fork, execlp and wait |
| [restaurant-threads](restaurant-threads/) | 2a, threads without synchronisation |
| [restaurant-synchronised](restaurant-synchronised/) | 2b, the same with a mutex |

Every program compiles with `-Wall -Wpedantic -Werror` and checks the return
value of every system and library call it makes, which is what the assignments
ask for and what makes the difference between a program that reports a failure
and one that continues with a wrong value.

The concepts behind the theory questions are in [bs](../bs/).
