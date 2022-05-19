# Condition/event nets

A place holds at most one token, because a place is a condition and a
condition either holds or does not. An event may occur when every place in
its preset is marked **and** no place in its postset is, and that second
clause is what keeps any place from receiving a second token.

## The server of sheet 11

Two clients access one server in parallel, and the server accepts two
requests at once. A condition/event net cannot count, so a capacity of two
becomes two places, `frei1` and `frei2`, one per slot. The module checks the
requirement the exercise states: a marking in which both clients are waiting
is reachable.

That translation is the lesson. Anything that would need counting in a B/E
net has to be unfolded into places, and the size of the net grows with the
capacity. The place/transition net exists to avoid exactly that.
