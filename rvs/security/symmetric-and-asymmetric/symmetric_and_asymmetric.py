"""Symmetric and asymmetric cryptography, and why both are used.

A symmetric cipher uses one key for both directions. It is fast, and it needs
the key to be shared in advance, which for `n` parties means `n(n-1)/2` keys.

An asymmetric cipher uses a pair: what one key encrypts only the other
decrypts. It removes the distribution problem, needing `2n` keys for `n`
parties, and it is orders of magnitude slower.

So real systems use both: the asymmetric algorithm transports a fresh symmetric
key, and the symmetric algorithm carries the data. That is what every TLS
handshake does.

The RSA here uses tiny primes and no padding. It demonstrates the arithmetic
and is not usable for anything.
"""

from __future__ import annotations

import math
import random


def random_key(length):
    """A random symmetric key of a given byte length."""
    return bytes(random.randrange(256) for _ in range(length))


def symmetric_encrypt(message, key):
    """Encrypt by exclusive or with a repeating key.

    A stream cipher with a badly reused keystream, which is exactly what makes
    it a teaching example: it round-trips, it is fast, and reusing the key on
    two messages leaks their exclusive or. A real cipher solves that with a
    nonce, not with a longer key.
    """
    return bytes(byte ^ key[index % len(key)] for index, byte in enumerate(message))


def symmetric_decrypt(cipher, key):
    """Decrypt, which for this cipher is the same operation."""
    return symmetric_encrypt(cipher, key)


def symmetric_key_count(parties):
    """Keys needed so that every pair can talk: `n(n-1)/2`."""
    return parties * (parties - 1) // 2


def asymmetric_key_count(parties):
    """Keys needed with a public key system: two per party."""
    return 2 * parties


def generate_pair(bits=16):
    """A toy RSA key pair.

    Two primes, their product as the modulus, an exponent coprime with the
    totient and its inverse. The security rests on factoring the modulus being
    hard, which for the sizes used here it is not.
    """
    primes = [number for number in range(1 << (bits // 2 - 1), 1 << (bits // 2))
              if _is_prime(number)]
    first, second = random.sample(primes, 2)

    modulus = first * second
    totient = (first - 1) * (second - 1)

    exponent = 65537 if math.gcd(65537, totient) == 1 else next(
        candidate for candidate in range(3, totient, 2)
        if math.gcd(candidate, totient) == 1)

    private = pow(exponent, -1, totient)
    return {"exponent": exponent, "modulus": modulus}, \
        {"exponent": private, "modulus": modulus}


def _is_prime(number):
    """Trial division, adequate for the small numbers used here."""
    if number < 2:
        return False
    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False
    return True


def encrypt(message, key):
    """Raise the message to the key's exponent, modulo the key's modulus."""
    return pow(message, key["exponent"], key["modulus"])


def decrypt(cipher, key):
    """The same operation with the other exponent.

    The symmetry is why one algorithm gives both encryption and signatures:
    encrypting with the private key produces something only the public key
    undoes, which is a signature rather than a secret.
    """
    return pow(cipher, key["exponent"], key["modulus"])


def hybrid_send(message, public_key):
    """Encrypt a message the way a real protocol does.

    A fresh symmetric key encrypts the data, and the public key encrypts the
    symmetric key. The asymmetric operation runs once on a few bytes rather
    than on the whole message, which is the only way it is affordable.
    """
    session_key = random_key(16)
    key_as_number = int.from_bytes(session_key[:2], "big")

    return {
        "encrypted_key": encrypt(key_as_number, public_key),
        "ciphertext": symmetric_encrypt(message, session_key),
        "key_bytes": len(session_key),
    }
