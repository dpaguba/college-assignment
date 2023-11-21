# Principal components

The first component is the direction of greatest variance, the next is the
best one perpendicular to it, and projecting onto the first few keeps most of
the variance.

On the four penguin measurements:

| | first component | first two |
|---|---:|---:|
| raw | 0.9999 | 1.0000 |
| standardised | 0.6458 | 0.8466 |

The raw answer is meaningless. Body mass runs into the thousands of grams and
the bill into the tens of millimetres, so the first component is body mass
with a rounding error and the method has found the units rather than the
structure.

Standardising gives every measurement the same weight and the two leading
components then keep 85 percent, which is a summary of the data rather than
of the scales. Principal components without standardisation answer a question
about the measuring instruments.
