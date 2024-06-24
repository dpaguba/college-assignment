# Slowly changing dimensions

A customer moves. Three answers, and they are three different statements
about what the warehouse is for.

| type | what happens | history | rows per key after 5 changes |
|---|---|---|---:|
| 1 | overwrite | lost | 1 |
| 2 | new row with a validity range | kept | 6 |
| 3 | keep one previous value in a column | one step | 1 |

Only type two answers a question about the past, and it is the only one whose
dimension grows. Type one is not a mistake: for a corrected spelling it is
exactly right, and using type two there would create a version of history in
which the name really was misspelled.

The choice is per attribute rather than per dimension, which is the part that
is easy to miss: a customer's address may be type two while the same
customer's corrected surname is type one.
