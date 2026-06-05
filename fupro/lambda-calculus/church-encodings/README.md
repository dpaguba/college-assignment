# Church encodings

The lecture ships a file of lambda terms, and all of them are reproduced here
and checked by reducing and reading the result back:

| | |
|---|---|
| numerals | `Z`, `S`, and `ZERO` to `THREE` |
| arithmetic | `ADD`, `MULT` |
| booleans | `TRUE`, `FALSE`, `NOT`, `AND`, `OR` |
| lists | `NIL`, `CONS`, `NEZ`, `LENGTH`, `MAP`, `CONCAT` |

`ADD TWO THREE` reduces to the numeral 5 and `MULT TWO THREE` to 6.
`LENGTH NEZ` is 3, and `LENGTH (CONCAT NEZ NEZ)` is 6.

Nothing but functions is available, so a number is what it does: the numeral
n applies its first argument n times to its second. Everything else follows
from that, and the list encoding is the same idea applied to a fold.

## The argument order is not a detail

The exam writes its numerals the other way round, `zero = λz.λs. z` with the
base case first, which is the fold convention. A predicate written for one
convention computes nothing under the other, and the parity predicate `even`
is the case where it shows: with the arguments in the wrong order it returns
false for every input, including zero.

## Encoding a data type

The exam asks for a Church encoding of `data Bin = LSB | Zero Bin | One Bin`.
The rule is general: one argument per constructor, applied in the order the
term is built. The direction of nesting is what has to be got right, since
the marker sits innermost and the outermost constructor carries the highest
place value.
