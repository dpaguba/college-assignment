# Data representation

| Topic | |
|---|---|
| [integer-representation](integer-representation/) | four encodings, and why one won |
| [floating-point](floating-point/) | IEEE 754, and what it cannot represent |
| [text-encoding](text-encoding/) | ASCII and UTF-8 |

Each of the three is a choice with a consequence that shows up much later: the
integer encoding decides how an adder is built, the float encoding decides that
arithmetic is not associative, and the text encoding decides whether a string
can be cut in the middle.
