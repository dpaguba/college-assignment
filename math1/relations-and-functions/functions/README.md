# Functions

Injective, surjective, bijective, and how many maps of each kind there are.

Between a three-element and a four-element set:

| | count |
|---|---:|
| all maps | 64 |
| injective | 24 |
| surjective onto three elements (from four) | 36 |
| bijective (equal sizes, four elements) | 24 |

The surjection count is inclusion and exclusion again, applied to the values
that might be missed, and it is checked against enumeration for the small
cases, so the formula and the count agree rather than being asserted
separately.

## The pigeonhole principle with a witness

A map from a larger set into a smaller one cannot be injective, and the
module returns the colliding pair rather than a boolean. The witness is what
turns the principle into a usable step in a proof: the interesting
applications name the two objects that collide.

Composition and inverses close the module. The inverse exists exactly for a
bijection, which is the finite version of the statement that a map is
invertible exactly when it loses nothing and misses nothing.
