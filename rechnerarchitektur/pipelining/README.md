# Pipelining

| Topic | |
|---|---|
| [pipeline-simulation](pipeline-simulation/) | the five stages, cycle by cycle |
| [hazards-and-forwarding](hazards-and-forwarding/) | the three hazards and what each costs |
| [instruction-scheduling](instruction-scheduling/) | filling the stalls at compile time |

Pipelining improves throughput and not latency, and every complication after
that is a consequence: instructions in flight together can conflict, and the
three ways they can are the three hazards.
