# Denial of service

Exercise 7.3 asks which kinds exist, what can be done, and why the
distributed form is harder.

A flood is arithmetic: capacity 100, incoming 1000, served 100. The damage is
not that the attacker gets something, it is that everyone else does not.

## Amplification

The attacker sends a small request with a forged source address and the large
answer goes to the victim. `amplification` returns the ratio; for a 64-byte
request and a 3000-byte answer it is about 47. The published figures for real
services run from about 50 for DNS to 550 for an NTP monlist query and four
digits for exposed memcached servers.

Two things are needed: a protocol over UDP, which does not check who is
asking, and a network that lets a forged source address out. The second is
fixable and requires every network operator to take part, which is why it has
not been fixed.

## The asymmetry

A half-open connection costs the server a table entry and the attacker
nothing: it sends a request and never answers. `syn_flood` returns the state
each side holds, and with cookies the server's side falls to zero, because
the necessary information is carried inside its own reply and read back from
what returns. The cost is that some connection options cannot be carried that
way.

## Why distributed is worse

With one source, one block. With ten thousand, each looks like an ordinary
visitor and a block by address either misses the attack or catches the
customers. `distributed` answers the question directly: blocking one address
helps only when there is one. The traffic also has to be stopped before the
link fills, which means upstream, at someone else's network.

The root cause does not go away: serving a request costs more than sending
one. The defence is to reverse that ratio or to stop the traffic far enough
from the target, and neither is a solution.
