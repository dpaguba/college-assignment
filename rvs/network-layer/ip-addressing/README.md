# IP addressing and subnetting

An address is 32 bits and a prefix says how many name the network. Two host
combinations are reserved, so a `/24` holds 256 addresses and 254 usable ones.

## The published allocation

The exercise gives `9.23.96.0/20`, 4096 addresses from `9.23.96.0` to
`9.23.111.255`, and eleven subnets to fit into it. The allocation matches the
published solution for every host subnet:

| subnet | hosts | needs | allocated |
|---|---|---|---|
| N1 | 1971 | 2048 | `9.23.96.0/21` |
| N2 | 1005 | 1024 | `9.23.104.0/22` |
| N3 | 242 | 256 | `9.23.108.0/24` |
| N4 | 112 | 128 | `9.23.109.0/25` |
| N5 | 98 | 128 | `9.23.109.128/25` |
| N6 | 55 | 64 | `9.23.110.0/26` |
| N7 | 29 | 32 | `9.23.110.64/27` |

The four router-to-router links get `/30` blocks. The published solution puts
them at `9.23.111.0` and leaves a gap; this allocation packs them immediately
after N7. Both are correct, and the difference is where the slack sits.

The block ends up **90.2%** used, and the missing tenth is the alignment rule:
every subnet is rounded up to a power of two.

## Largest first is not a preference

A subnet must start at a multiple of its own size, so a small one placed early
leaves a gap no larger one can use. Demands of 2, 120 and 60 hosts fit in a
`/24` when allocated largest first and **do not fit at all** in the given
order, which is the shortest demonstration of why the rule exists.

## The two reserved addresses

Forgetting them is the classic error, and it only shows up when a demand is
exactly a power of two: 1971 hosts need 1973 addresses and therefore 2048, but
1024 hosts need 1026 and therefore 2048 as well.
