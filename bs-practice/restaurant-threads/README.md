# Restaurant, without synchronisation

Assignment 2a: the opening party as POSIX threads. Four members of staff each
serve their own share of twelve guests, cooking with five stirs per guest.

```
gcc -Wall -std=c11 -Wpedantic -Werror -O0 -D _POSIX_C_SOURCE=200809L -pthread \
    -o aufgabe2a aufgabe2a.c
./aufgabe2a
```

This version is **deliberately wrong**, and the assignment asks what goes
wrong. The counter of served guests is shared and unguarded, so reading it,
adding one and writing it back can interleave with another thread doing the
same.

Run 300 times, it prints the right total 210 times and a wrong one 90 times,
with counts as low as 6 out of 12. Seven runs in ten look correct.

## Two details that are not about the race

The argument passed to each thread lives in an array in `main`, not in the loop
body, because `pthread_create` returns before the thread runs and a local would
be gone by the time it is read.

The staff number is passed in rather than derived from `pthread_self`, because
a `pthread_t` is opaque and unordered: unique, not a small integer, and useless
as an index.

The fixed version is in [restaurant-synchronised](../restaurant-synchronised/).
