# Switching and address resolution

A switch learns where a host is from the **source** address of the frames it
receives and forwards by the **destination**. Three outcomes:

| destination | action |
|---|---|
| unknown | flood to every other port |
| known, another port | forward |
| known, the same port | drop |

The third case is the one people forget: two hosts on the same segment have
already heard each other, so repeating the frame would be pure noise.

Flooding is correct, wasteful and self-correcting, since the reply teaches the
switch the way back. That is the whole algorithm, and it is why a switch is
plug-and-play in a way a router is not.

Entries age out, because hosts move. Without ageing, moving a machine to
another port would black-hole its traffic until the switch was restarted.

## ARP fills caches nobody asked to fill

A host that needs a hardware address broadcasts the question to the segment and
the owner answers. Everyone else hears both, which is why an ARP cache
populates itself and why forging a reply is trivial.

## Layers decide capabilities

A switch reads hardware addresses and needs none of its own; a router reads
network addresses and has one per interface. A switch therefore cannot split a
broadcast domain, and a router cannot avoid being configured. Everything else
about where to put which device follows from those two sentences.
