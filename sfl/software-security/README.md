# Software security

Five modules following the shape of the exercise sheet: the arithmetic that
produces a wrong length, the copy that uses it, the guard that catches the
copy, the output function that leaks the guard, and the measures that raise
the cost of all of it.

The chain is the point. Exercise 3.1 asks for two positive numbers whose sum
is negative; exercise 3.3 asks to pass a check without the password; and the
two are the same bug seen twice, once as arithmetic and once as memory.

Three measurements worth keeping:

- Twenty bytes into an eight-byte buffer reach the saved base pointer and not
  the return address; the frame is corrupt and the flow is not yet hijacked.
  Thirty-two bytes hijack it.
- A signed length check passes with −1, and the unsigned copy that follows
  takes it as 4294967295.
- With 28 bits of address entropy a blind attacker needs about 134 million
  attempts, and one leaked pointer reduces that to one.
