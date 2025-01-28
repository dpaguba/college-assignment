# Public key infrastructure

Exercise 7.2 asks the reader to look at their own browser: which roots it
trusts, how many there are, what the chain for github.com looks like and
until when it is valid. The answers depend on the browser and the day; what
does not depend on either is the structure the questions are pointing at.

A chain runs from the leaf through one or more intermediates to a root the
browser already holds. `validate` checks the name, the revocation list, the
validity periods, the issuer links and the anchor, and names the first
failure: hostname mismatch, revoked, expired, broken chain or no trusted
root.

A wildcard covers exactly one label: `*.example.org` matches
`www.example.org` and neither `a.b.example.org` nor `example.org` itself.

## One bad authority is enough

A browser trusts on the order of 150 roots, and every one of them may issue
for every name. `weakest_link` states the consequence: the number that has to
be compromised is **one**, however carefully the other 149 work. DigiNotar,
Comodo and TrustWave are the cases the lecture names.

## Revocation mostly does not work

The check has to reach a responder, and when it cannot, browsers continue
rather than refuse, because hard failure would break browsing whenever a
responder is down. An attacker who controls the connection also controls the
check. The answers in use are short-lived certificates, stapling and lists of
the important revocations pushed with the browser.

Pinning narrows the trust to a known key, so a valid certificate from another
authority no longer helps; the price is that an unprepared key change takes
the service off the air.

Certificate transparency does not prevent a wrong issuance. It records every
certificate in a public append-only log, so the affected domain owner can
find it afterwards. Detection instead of prevention, which is the realistic
goal in a system with 150 equal roots.
