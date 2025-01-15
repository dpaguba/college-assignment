# Multiple factors

Three kinds: something known, something held, something one is. A password
and a PIN are both knowledge, so requiring both is one factor asked twice;
`is_multi_factor` rejects that pair and accepts a password with a token.

## The time-based code

`time_code` implements the construction of RFC 6238: an HMAC over the time
slice rather than the second, so both sides agree despite small clock
differences. Codes within one thirty-second window are equal and codes in
different windows are not.

Six digits is a million possibilities. `guessing` computes what that is worth
without a limit on attempts: a hundred thousand tries succeed with
probability about 0.095. The strength of the second factor is not in the
digits, it is in counting the attempts.

## What a second factor does not cover

A one-time code is typed in, so a page pretending to be the real one collects
it and passes it on immediately. A security key signs the origin along with
the challenge, and on the wrong origin the signature does not fit;
`stops_phishing` separates the two on exactly that property.

And the recovery path is usually the weakest link: backup codes written down,
security questions whose answers are public, a support desk that can be
talked to, a phone number that can be moved. The way around the second factor
needs the same strength as the way through it, and it rarely has it.
