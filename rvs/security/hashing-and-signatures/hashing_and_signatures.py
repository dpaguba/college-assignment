"""Hashes, message authentication codes and certificates.

A cryptographic hash maps any input to a fixed-size digest, and three
properties make it useful: the same input always gives the same digest, a
changed input gives an unrelated one, and finding two inputs with the same
digest is infeasible.

The third is weaker than it sounds. The birthday bound says a collision takes
about `2^(n/2)` attempts for an `n`-bit digest, not `2^n`, which is why a
64-bit hash is broken by `2^32` work and why every modern hash is at least 256
bits.

A **MAC** adds a key, so it proves who sent a message and not only that it is
unchanged. A **signature** goes further: it proves it to a third party, because
verification uses a public key rather than the shared secret.
"""

from __future__ import annotations

import hashlib
import hmac


def digest(data):
    """A cryptographic digest of some bytes."""
    return hashlib.sha256(data).hexdigest()


def avalanche(first, second):
    """The fraction of digest bits that differ between two inputs.

    About half for any two distinct inputs, however similar. That is the
    avalanche property, and it is what makes a digest useless for anything
    except comparison: it carries no information about how close the inputs
    were.
    """
    left = int(digest(first), 16)
    right = int(digest(second), 16)
    return bin(left ^ right).count("1") / 256


def mac(message, key):
    """A keyed message authentication code."""
    return hmac.new(key, message, hashlib.sha256).hexdigest()


def verify_mac(message, key, tag):
    """Whether a tag matches, compared in constant time.

    The comparison matters. A byte-by-byte comparison that returns early leaks
    how many bytes were right, and an attacker can recover the tag one byte at
    a time by timing it. That is a real attack on real systems, and the fix is
    one function call.
    """
    return hmac.compare_digest(mac(message, key), tag)


def collision_effort(bits):
    """How much work a collision takes, by the birthday bound.

    `2^(n/2)`, not `2^n`. A 64-bit digest falls to `2^32` operations, which is
    a few seconds, and that is the reason digest sizes are twice what the
    intuitive argument suggests.
    """
    return 2 ** (bits // 2)


def preimage_effort(bits):
    """How much work finding a specific input takes: the full `2^n`."""
    return 2 ** bits


class Authority:
    """A certificate authority that signs and verifies bindings."""

    def __init__(self, name, secret=b"authority secret"):
        """Store the authority's name and its signing secret."""
        self.name = name
        self.secret = secret

    def issue(self, subject, public_key):
        """Bind a name to a key and sign the binding.

        The certificate is the binding plus the signature, and its whole value
        is that a verifier who trusts the authority need not have met the
        subject. That is the only thing a certificate does, and it is why a
        compromised authority is so damaging: every binding it ever made
        becomes worthless.
        """
        certificate = {"subject": subject, "public_key": public_key,
                       "issuer": self.name}
        certificate["signature"] = self._sign(certificate)
        return certificate

    def verify(self, certificate):
        """Whether a certificate's signature still matches its contents."""
        claimed = certificate.get("signature")
        body = {key: value for key, value in certificate.items() if key != "signature"}
        return hmac.compare_digest(self._sign(body), claimed or "")

    def _sign(self, certificate):
        """Sign the certificate's fields in a fixed order."""
        body = "|".join(f"{key}={certificate[key]}"
                        for key in sorted(certificate) if key != "signature")
        return mac(body.encode(), self.secret)
