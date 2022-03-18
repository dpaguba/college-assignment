# Text encodings

ASCII is seven bits. UTF-8 extends it to every Unicode code point while leaving
ASCII byte-for-byte unchanged, which is why it displaced every alternative:
existing files were already valid.

| code point | bytes | lead byte |
|---|---|---|
| up to 7 bits | 1 | `0xxxxxxx` |
| up to 11 | 2 | `110xxxxx` |
| up to 16 | 3 | `1110xxxx` |
| up to 21 | 4 | `11110xxx` |

Continuation bytes always start with `10`, verified against the platform
encoder for a mix of Latin, Cyrillic, currency and musical characters.

## Self-synchronisation

Because no continuation byte can start a character, a reader that lands in the
middle of one finds the next boundary by scanning forward. A corrupted byte
costs one character rather than the rest of the file, which is exactly what
`resynchronise` does and what UTF-16 cannot do.

## Bytes are not characters

`encoded_length` is not the character count, and the difference is behind every
truncated string that ends in half a character. A language with a fixed-width
string type hides the distinction; a byte-oriented one does not.
