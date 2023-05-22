# Transformation

Three tools for the same problem: two records referring to the same thing
rarely match exactly.

**Edit distance** counts single character changes, and it is a metric, which
the module checks: symmetric, and satisfying the triangle inequality. That is
what makes a threshold meaningful.

**Soundex** maps names that sound alike to the same four character code, so
Robert and Rupert agree and Smith does not. It is crude and it is language
specific, and it catches the errors a distance misses, such as two spellings
of the same sound.

**Date parsing** is the one where the separator carries the meaning.
`05.03.2024` is the fifth of March and `03/05/2024` is the same day written
the American way, and no parser can tell from the digits alone unless one
exceeds twelve. The module decides by the separator and refuses what it
cannot read, because a transformation that guesses moves the error somewhere
it is no longer visible.
