# JSON web tokens

Three base64url parts: header, payload, signature. The signature is checked
against an independently computed HMAC-SHA256 over header and payload, and
matches.

The payload is readable by anyone holding the token. It is encoded, not
encrypted, and a secret does not belong in it.

## The two forgeries

Editing the payload and keeping the signature is caught: the module builds a
token claiming `admin: false`, rewrites it to `admin: true`, confirms the new
value is readable, and confirms verification fails.

Setting the header's `alg` to `none` and dropping the signature is the more
interesting one. A verifier that reads the algorithm from the header and
does what it says will accept such a token. The header comes from the
attacker; it must not be allowed to decide how it is checked. The
implementation here requires HS256 and rejects anything else.

The signature covers the header too, so changing `HS256` to `HS512` while
keeping the signature also fails.

Expiry is checked against a supplied clock: valid at 50, refused at 200.
