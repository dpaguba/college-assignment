# Symmetric cryptography

Five modules along the exercise sheet: the shift cipher, the substitution
cipher and its break, the one-time pad, the modes of a block cipher and the
stream cipher.

Two published answers are reproduced. The Caesar ciphertext decodes with key
13 to Kerckhoffs's principle. The substitution ciphertext is the opening of
Shannon's *A Mathematical Theory of Communication*, recovered by frequency
analysis and hill climbing on quadruple frequencies rather than by looking it
up.

The thread running through the block is the difference between a key space
and a security level. The substitution cipher has 26 factorial keys and falls
to statistics. The one-time pad is provably perfect and still leaks the exam
results through the length of its messages. A cipher is broken at whatever it
did not promise to hide.
