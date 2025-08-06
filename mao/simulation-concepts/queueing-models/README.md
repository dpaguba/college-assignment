# Queueing models

The single server queue has closed forms, which makes it the standard check
on a simulator.

| load | in the system |
|---|---:|
| 0.5 | 1 |
| 0.8 | 4 |
| 0.9 | 9 |
| 0.95 | 19 |
| 0.99 | 99 |

The number in the system is the load over one minus the load, so it grows
without bound as the load approaches one. Doubling the traffic from 0.5 to
0.99 multiplies the queue by 99, which is why utilisation and not throughput
is the quantity a capacity study watches.

The simulation of 40 000 customers at half load gives a response time of
1.974 against an analytical 2.0. That agreement is what the module is for:
finding a simulator's bug on a model with a known answer is far cheaper than
finding it later on a model without one.
