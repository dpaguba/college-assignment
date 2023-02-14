# TCP connection management

Three messages to open and four to close, and the asymmetry is not an accident:
a connection is two independent byte streams, so each direction closes
separately.

Three rather than two on the way in, because both sides must choose an initial
sequence number and learn the other's. Two would leave one side's number
unacknowledged, and a delayed duplicate of an old request could then be
accepted as a new connection.

## TIME_WAIT

The side that closes first waits twice the maximum segment lifetime, 240
seconds for a 120-second lifetime. Once for its final acknowledgement to
arrive, once for any retransmitted FIN to die. That wait is why a just-restarted
server cannot immediately rebind its port, and why the option to override it
exists and is dangerous.

## Three duplicate acknowledgements, not one

A single duplicate is usually reordering, and halving the window every time a
packet took a different route would be ruinous. Three is a threshold chosen by
measurement rather than derived, which is worth saying plainly: parts of TCP
are engineering constants.

## Flow control is not congestion control

The receive window protects the **receiver** from a fast sender. The congestion
window protects the **network**. A sender is limited by the smaller of the two,
and confusing them is the standard mistake.
