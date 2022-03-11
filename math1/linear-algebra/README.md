# Linear algebra

| Topic | |
|---|---|
| [vector-spaces](vector-spaces/) | span, independence, basis, dimension |
| [gaussian-elimination](gaussian-elimination/) | echelon forms and the main theorem |
| [matrix-inverse](matrix-inverse/) | Gauss-Jordan, and elimination as a factorisation |
| [linear-maps](linear-maps/) | a matrix is a map plus two bases |
| [rank-nullity](rank-nullity/) | what is lost and what is reached |
| [determinants](determinants/) | three definitions, one number |
| [eigenvalues](eigenvalues/) | directions that are only stretched |
| [eigenfaces](eigenfaces/) | the whole block applied to data |

The third part of the lecture, in exact arithmetic throughout. Every entry is
a fraction, so a rank is a rank and not a judgement about how small a number
has to be before it counts as zero. That choice is what lets the results be
compared with numpy rather than merely resembling it: 300 determinants, 200
inversions, 200 systems and 100 spectra, all agreeing.

Everything reduces to elimination. The rank decides independence, span,
dimension, solvability and invertibility; the same elimination computes the
determinant and, applied beside the identity, the inverse. The one place a
different tool is needed is the eigenvalue, and even there the characteristic
polynomial is built from determinants.

The cost table is the argument for doing it that way: for an eight by eight
matrix the definition of the determinant as a sum over permutations needs
282 240 multiplications and elimination needs 168.
