# Firewalls

Rules are matched in order and the first one that fits decides. A field left
out matches anything; the last rule is the default policy, and it must drop.
A rule set without one permits whatever nobody thought of.

## Exercise 7.1a

Internal hosts in 192.168.0.0/24 may act as HTTP and HTTPS clients, nothing
else:

| action | source | source port | destination | dest. port | protocol | state |
|---|---|---|---|---|---|---|
| allow | 192.168.0.0/24 | any | any | 80 | tcp | new |
| allow | 192.168.0.0/24 | any | any | 443 | tcp | new |
| allow | any | 80, 443 | 192.168.0.0/24 | any | tcp | established |
| drop | any | any | any | any | any | any |

## Exercise 7.1b

All outgoing connections and their answers, except to and from two servers:

| action | source | destination | state |
|---|---|---|---|
| drop | any | 6.6.6.6/32 | any |
| drop | any | 66.66.66.66/32 | any |
| drop | 6.6.6.6/32 | any | any |
| drop | 66.66.66.66/32 | any | any |
| allow | 192.168.0.0/24 | any | new |
| allow | any | 192.168.0.0/24 | established |
| drop | any | any | any |

The blocks stand first on purpose. `order_matters` runs the same pair of rules
in both orders and returns different verdicts for the same packet: a rule
placed after a matching one is never reached.

## Why state is worth having

A stateless filter sees each packet alone and cannot tell an answer from an
unsolicited packet. To let answers back it must allow everything with a
source port of 80 or 443 to the high destination ports, and an attacker can
set a source port as easily as anyone. With connection state the filter
remembers the outgoing connection and admits only its answer.
