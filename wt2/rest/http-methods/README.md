# HTTP methods

Safe means the state does not change: GET, HEAD, OPTIONS, TRACE. Idempotent
means doing it twice leaves the same state as doing it once: the safe methods
plus PUT and DELETE.

The claim is checked on a state model rather than quoted. Every method is
applied once and twice to 200 random states and the answers are compared with
the table; they agree throughout.

Two POSTs create two resources, which the module counts as 1 then 2. Two PUTs
to the same address leave one. Every safe method is idempotent, and DELETE
shows the converse fails: it changes the state and repeating it is still
harmless.

## PATCH

PATCH is not listed as idempotent, and measuring shows why the specification
leaves it out. A body that sets a value is idempotent; a body that says
"increase the count by one" is not, and the module measures the view count
going 5 → 6 → 7. The method does not decide; the body does.
