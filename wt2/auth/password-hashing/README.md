# Password hashing

A record holds a fresh salt, the derived key and the iteration count. The
derivation is PBKDF2 with HMAC-SHA256 from the standard library; the
comparison is `hmac.compare_digest`, which takes the same time whatever the
first differing byte is.

## What the salt buys

A precomputed table of common passwords cracks the unsalted records at once;
the module measures how many. Against the salted records the same table finds
nothing, because each record was derived with a different salt and the table
would have to be rebuilt per record.

## What the iterations buy

The measured rate says it plainly: a plain SHA-256 runs hundreds of thousands
of times a second, and the derivation at 100000 iterations runs a few dozen.
A hash function built to be fast is exactly the wrong tool, because speed is
what the attacker needs. Raising the iteration count raises the attacker's
cost linearly and the login's cost by a moment nobody notices.

The rules: a fresh salt per record, a function built to be slow, enough
iterations to be felt, a comparison that does not leak its progress, and
never the password itself anywhere, a log included.
