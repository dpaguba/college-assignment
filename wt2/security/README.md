# Security

Five attacks and what actually stops them, each demonstrated rather than
described: scripting through the output context, injection through string
concatenation, forgery through the browser's own cookie handling, the limits
of what an encrypted connection promises, and the arithmetic of a challenge
meant to tell a human from a program.

The measurement worth carrying away is the injection one: the textbook
payload in the name field does not work, because AND binds tighter than OR.
