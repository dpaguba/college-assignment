# Binary numbers

The exam's type, with the marker at the least significant end:

```haskell
data Bin = LSB | Zero Bin | One Bin
```

| term | value |
|---|---:|
| `LSB` | 0 |
| `Zero LSB` | 0 |
| `One LSB` | 1 |
| `One (Zero LSB)` | 2 |
| `One (Zero (Zero LSB))` | 4 |

All four examples are reproduced. The direction is the thing to get right:
the constructor next to the marker is the lowest place, so the outermost one
is the most significant, and every function in the module depends on it.

## The obvious fold computes the wrong number

The fold traverses from the marker outwards, so the naive algebra that
doubles and adds gives the value of the **reversed** bit string. On the term
for 13 it returns 11, and on the term for 6 it returns 3. Nine of the sixteen
numbers below sixteen come out wrong, and the seven that agree are the ones
whose bit strings are palindromes.

The correct fold carries a pair, the value so far and the place value of the
next bit. Both are implemented, because the wrong one is the one most people
write first and it fails silently.

The rest is what the exam asks for: `shift` doubles by adding a zero bit,
written with the fold, and it is checked for every number below twenty;
`rlz` drops the leading zeros, which are the outermost constructors; and the
`Eq` instance compares after `rlz`, so different representations of the same
number are equal.
