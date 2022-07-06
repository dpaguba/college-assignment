# Database design

From a diagram to a schema, and from a schema to a better one. Functional
dependencies carry the argument: the closure decides which dependencies hold,
which attribute sets are keys and which normal form a schema reaches.

Two algorithms end the block. Decomposition reaches Boyce-Codd normal form
and can lose a dependency; synthesis keeps every dependency and stops at the
third normal form. The same schema, student-subject-teacher, is run through
both to show the difference.
