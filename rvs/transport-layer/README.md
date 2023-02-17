# Transport layer

| Topic | |
|---|---|
| [reliable-transfer](reliable-transfer/) | turning a lossy channel into a stream |
| [tcp-connection](tcp-connection/) | opening, closing, and the states between |
| [congestion-control](congestion-control/) | probing for a rate nobody publishes |

The layer's job is to make an unreliable, unordered, congested network look
like a byte pipe between two processes. Each module is one part of that lie and
the cost of maintaining it.
