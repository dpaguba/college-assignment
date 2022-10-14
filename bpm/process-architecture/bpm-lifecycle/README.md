# The BPM lifecycle

Six phases in a circle: discovery, analysis, redesign, implementation,
monitoring, and back to discovery. Identification sits before them as step
zero.

Each phase is named by what it produces, and that output is the input of the
next one:

| Phase | Produces |
|---|---|
| Prozessidentifikation | Prozessarchitektur |
| Prozesserhebung | Istprozessmodell |
| Prozessanalyse | Verständnis der Schwächen |
| Prozessverbesserung | Sollprozessmodell |
| Prozessimplementierung | Prozessausführung |
| Prozessüberwachung | Kennzahlen |

`handovers` returns exactly that chain. The last arrow does not point back to
identification but to discovery: the numbers from monitoring are the reason
to look at the process again, and the architecture rarely changes because of
them.

## Step zero

Identification is problem driven. Nobody starts the cycle because the cycle
is elegant; they start it because something takes too long or costs too
much, and the first question is which processes cause it.

How much work that is depends on the maturity of the organisation:
`effort_of_identification` counts the three questions of the lecture (were
there earlier initiatives, are the processes defined, is there
documentation) and returns the ones still open. At maturity three there is
nothing left to do, at zero there are three.
