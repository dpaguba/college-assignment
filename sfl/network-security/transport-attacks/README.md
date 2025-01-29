# Attacks on the encrypted connection

Four attacks, and none of them breaks a cipher.

## Downgrade

The version is negotiated, so whoever controls the connection removes the
strong offers and both sides settle on the weakest both still accept. A
minimum version on the server side removes the choice; `downgrade_possible`
returns exactly that difference.

## Stripping

The first visit to an address usually goes out unencrypted and is redirected.
An attacker in the middle answers it, speaks encrypted to the server and
unencrypted to the user. Strict transport security closes it once the header
has been seen, which leaves the very first visit, and the preload list
shipped with the browser closes that.

## Compression side channel

If attacker-controlled text and a secret are compressed in the same message,
the size of the result depends on whether the attacker's guess matches the
secret: a match creates a longer repetition and the output shrinks.
`compression_leak` recovers the secret character by character from the sizes
alone.

The compression here is modelled as the length minus the longest repeated
substring, which is what a dictionary compressor is doing at its core; the
module also reports what zlib produces for the final guess. The fix is not a
better cipher, it is not compressing a message that mixes attacker input with
a secret.

## Padding oracle

If the server's answer differs depending on whether the padding was valid,
the ciphertext can be decrypted without the key. Changing the preceding block
byte by byte and watching the answer reveals the intermediate value of the
decryption, and the real preceding block turns that into the plaintext.
`padding_oracle` runs the attack, byte by byte from the last, with the usual
check against a false hit on the final byte, and reports how many oracle
queries it needed.

## What they have in common

All four read something other than the ciphertext: the negotiated version,
the size, the answer, the timing. The fixes are the same list every time:
authenticated encryption, a minimum version negotiated under a signature,
strict transport security with preloading, no compression over mixed content,
and answers that look identical whatever went wrong.
