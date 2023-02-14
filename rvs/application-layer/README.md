# Application layer

| Topic | |
|---|---|
| [http](http/) | requests, responses, and where the latency goes |
| [dns](dns/) | resolving a name by walking a tree |
| [client-server-and-p2p](client-server-and-p2p/) | why the architecture is a function of scale |

All three are about latency and scale rather than about bandwidth, which is the
layer's characteristic concern: the network below is fast, and what makes an
application slow is how many times it has to wait for it.
