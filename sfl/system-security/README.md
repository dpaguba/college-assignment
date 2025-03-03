# System security

Four modules: the channels that carry information where none was meant to go,
the permission bits of a UNIX file, the two classical policy models, and the
separation the operating system provides.

Two results are checked against the published solution of exercise 1: the
Bell-LaPadula and Biba table, line for line, and the reading of the
parliament listing, where the set-user-id bit on `omicron.sh` is what the
question is really about.

The recurring theme is what a mechanism does not cover. Isolation closes the
storage channel and leaves the timing channel open; the two policy models
each cover one direction and together cover nothing.
