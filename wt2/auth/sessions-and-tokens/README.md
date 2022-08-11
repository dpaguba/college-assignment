# Sessions and tokens

A session is an entry on the server; a token carries its claims and a
signature. The difference shows up in two places.

## Revocation

Logging out of a session deletes the entry and the identifier is worthless
immediately. A token stays valid until it expires, because there is nothing
on the server to delete. The module measures both: the session is dead at
once, the token is valid until its expiry at 1000.

## Storage

For 1000 users the session server keeps 64 KB; the token server keeps zero.
That is the argument for tokens, and it is undone the moment revocation is
needed: a deny list brings the state back, and with it the shared store that
tokens were supposed to avoid.

| | session | token |
|---|---|---|
| state | on the server | with the caller |
| revocation | immediate | at expiry |
| scaling | needs a shared store | nothing to share |
