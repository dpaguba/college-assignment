# VBA

Tutorials ten to thirteen. The exercises cannot be run here, so these modules
implement the semantics in Python and record where VBA differs from what a
reader coming from another language expects.

| Module | Topic |
|---|---|
| [control-flow](control-flow/) | If, Select Case, and Offset |
| [loops](loops/) | For, Do While, Do Until |
| [arrays](arrays/) | bounds, Option Base, ReDim Preserve |
| [user-defined-function](user-defined-function/) | Sub against Function, ByRef |

Four of the differences cost real time when first met: `Dim a(5)` gives six
elements, `Offset` counts from zero while rows count from one, the loop
variable survives the loop, and arguments are passed by reference unless
stated otherwise.
