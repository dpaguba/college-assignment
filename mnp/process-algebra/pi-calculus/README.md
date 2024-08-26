# The pi-calculus

CCS fixes who can talk to whom when the process is written. The pi-calculus
sends names over channels, so a received name becomes a channel the receiver
can use next.

```
x<y>.0 | x(z).z<w>.0   ->   0 | y<w>.0
```

The receiver never mentioned `y`. After one communication it is sending on it,
and the set of channels in use has changed, which is the whole difference from
CCS in one reduction. Mobility, reconfiguration, and passing a callback are
all this rule.

## Scope extrusion

`(new x) P` makes `x` private to P. Sending `x` out of that scope widens the
restriction to cover the receiver rather than making `x` public, so the name
stays private to the two parties. This is how a fresh session channel is
handed to a partner, and it is the formal content of "here is a reference only
you and I have".

## Encodings

Booleans and lists need no data types. A boolean is a process that signals on
one of two channels, and conjunction consults the second only when the first
answered true. A list is nested outputs ending in an empty-list signal, and
reading it back is a sequence of receives.

The point of the encodings is not economy. Anything encodable this way is
computation the calculus already contains, so a proof about processes covers
data as well, and there is no separate theory of values to keep consistent
with the theory of communication.
