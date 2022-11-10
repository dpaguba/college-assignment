# Servers

A periodic system has no room for aperiodic work unless something is reserved
for it, and the reservation is what a server is.

| server | request at 1, period 5, cost 1 | budget kept |
|---|---:|---|
| polling | waits 4, responds at 5 | no |
| deferrable | waits 0, responds at 1 | yes |

A polling server looks for work only when its period comes round, so a
request arriving just after a poll waits a full period. A deferrable server
keeps its budget until something needs it, which answers immediately.

The price is the utilisation bound for the rest of the system. A deferrable
server can hold its budget and then spend it at the worst possible moment, so
the periodic tasks beside it get a lower bound than they would with an
ordinary task of the same utilisation. Better response time, less room for
everything else.
