# Restaurant, synchronised

Assignment 2b: the same program with a mutex around the counter.

```
gcc -Wall -std=c11 -Wpedantic -Werror -O0 -D _POSIX_C_SOURCE=200809L -pthread \
    -o aufgabe2b aufgabe2b.c
./aufgabe2b
```

Run 300 times, it prints 12 every time, against 210 of 300 for the
[unsynchronised version](../restaurant-threads/).

## The critical section is one line

Everything expensive stays outside it. The cooking, which is where all the time
goes, happens before the lock is taken, so the threads still run in parallel
and serialise only on the increment.

That is the general shape of a correct fix: not "lock the function" but "lock
the shared object, for as short a time as the invariant allows". Locking the
whole of `bedienen` would also be correct and would make the program
single-threaded.

## Errors are checked

`pthread_mutex_lock` and `pthread_mutex_unlock` return an error code rather
than setting `errno`, which is why they are checked with `strerror` on the
return value and not with `perror`. Every pthread function in the assignment
behaves that way, and it is the most common mistake in a submission.
