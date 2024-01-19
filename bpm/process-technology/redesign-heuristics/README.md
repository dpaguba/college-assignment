# Redesign heuristics

Eight heuristics, each with its effect on the four corners of the devil's
quadrangle: time, cost, quality, flexibility.

| Heuristic | Time | Cost | Quality | Flexibility |
|---|---|---|---|---|
| parallelism | better | worse | same | same |
| triage | better | same | better | worse |
| resequencing | better | better | same | same |
| task elimination | better | better | worse | same |
| task composition | better | better | same | worse |
| empower | better | better | worse | better |
| integral technology | better | worse | better | better |
| exception | better | same | better | worse |

Time improves in every row, which says less about the heuristics than about
what the collection was assembled for. The interesting column is whichever
one pays.

## Why it is called the devil's quadrangle

Pull one corner and the others move. A change that saves time usually costs
money or flexibility; one that saves both tends to cost quality. So a
proposal that improves all four corners is not good news, it is a reason to
check the assumptions.

`trade_offs` counts how often each corner improves and how often it suffers
across the eight, which is a quick way to see what a redesign programme is
implicitly optimising for.
