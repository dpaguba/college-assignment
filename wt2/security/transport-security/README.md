# Transport security

Chain validation, checked case by case: a chain reaching a trusted root
validates; a self-signed certificate fails with "no trusted root"; a chain
past its validity fails with "expired"; a chain whose leaf names another host
fails with "hostname mismatch".

A wildcard covers exactly one level: `*.example.org` matches
`www.example.org`, not `a.b.example.org` and not `example.org` itself.

## The key agreement

Diffie-Hellman, computed with small numbers so the arithmetic is visible: the
prime, the generator and both public values go over the wire, both sides
arrive at the same shared key, and that key is not among the values
transmitted.

## What it does and does not cover

Covered: nobody in between reads the traffic, nobody changes it unnoticed,
and the certificate says which server this is.

Not covered: what the server does with the data afterwards, who the caller is
unless a client certificate is used, and whether the site deserves any trust
at all. A padlock is a statement about the pipe, not about the other end.
