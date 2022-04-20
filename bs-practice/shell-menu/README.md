# Shell menu

Assignment 1: a menu that runs `ls` with a chosen argument in a child process.

```
gcc -std=c11 -Wall -Wpedantic -Werror -o shell_menue shell_menue.c
./shell_menue
```

## The three calls

`fork` returns twice. The child gets zero and calls `execlp`, which replaces
the program and **returns only on failure**, so the code after it is the error
path and nothing else. The parent gets the child's id and calls `waitpid`.

Waiting is not optional here. Without it the finished child stays a zombie and
the menu reappears before `ls` has printed anything, so the output interleaves.
The assignment asks for neither zombies nor orphans, and one `waitpid` gives
both.

## The input loop that does not spin

A non-numeric input leaves the offending characters in the buffer, so the next
`scanf` fails the same way and the program loops forever printing the menu.
Discarding the rest of the line after a failed conversion is what stops it, and
it is the difference between a program that rejects bad input and one that
hangs on it.
