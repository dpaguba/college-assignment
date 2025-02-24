# Authentication

Three modules: how a password is stored, how a session key can be derived
from one without exposing it, and what a second factor adds.

The two book chapters that came with the course sit behind the middle module:
Menezes on passwords and Boyd and Mathuria on password-based key
establishment. Their point is the same one the module measures: a password is
short and guessable, so the protocol must ensure that every guess costs an
interaction with the server rather than a computation the attacker does
alone.

The other measured figures: a six-digit code falls to a hundred thousand
attempts with probability about a tenth, and four random words carry more
entropy than eight characters chosen by a person.
