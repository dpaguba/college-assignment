# Synthesis into third normal form

Build a minimal cover, make one relation per left side, add a key if none of
the relations contains one, and drop any relation contained in another. The
result preserves every dependency by construction, is lossless because a key
is present, and is in third normal form.

On student, subject, teacher the synthesis returns the original schema
unchanged, because it is already in third normal form. The decomposition into
Boyce-Codd normal form splits the same schema and loses
`{student, subject} → teacher`. `compare` runs both on the same input and
reports all three facts: the decomposition loses a dependency, the synthesis
keeps it, and both are lossless.

That is the trade the two algorithms make. One buys a stronger normal form
with a dependency that can no longer be enforced locally; the other keeps
every dependency and tolerates the redundancy the third normal form still
permits.
