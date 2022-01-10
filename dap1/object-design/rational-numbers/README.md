# Rational numbers

The class chapter three writes twice: first with public fields, then with the
fields hidden. Only the second version can keep a promise.

A fraction is normalised when it is made, cancelled down with the sign in the
numerator, so `2/4` and `1/2` are the same object content and comparison never
has to think about it. That promise holds only because nothing outside the
class can write a field, and it stays cheap only because the object is
immutable: arithmetic returns new fractions instead of changing this one, so
a fraction handed to someone else can never change underneath them.

## Exactness has a range

Adding a thousand fractions with denominators near 100 000 needs a common
denominator near 10 000 000 000, which does not fit in an `int`. The first
version of this class computed in `int` and returned `199991/1409165408` for
`1/100000 + 1/99991`, a wrong answer with no sign of anything having gone
wrong.

The arithmetic now runs in `long` and the range is checked after cancelling
rather than before, because an intermediate result is routinely too large
while the fraction itself fits: `1073741823/2147483646 + 1/2` is exactly `1`.
When the cancelled result still does not fit, the class throws instead of
wrapping around.

That is the trade an exact representation makes. Floating point never
overflows here and is never exact; the fraction is exact and has a range. A
telescoping sum of sixty terms comes out as exactly `60/61`, which no
`double` sum would.

## Comparison stays in integers

Comparing by dividing would introduce a rounding error the class exists to
avoid, so `compareTo` cross-multiplies in `long`. The array methods of the
second practical sheet then read as the integer versions with two changes:
comparison through `compareTo`, arithmetic through the object's own methods.
Everything else about those loops is unchanged, which is the argument for
defining a type at all.
