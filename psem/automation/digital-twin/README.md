# Model, shadow, twin

The classification turns on exactly two questions: does data flow from the
thing to the model, and do changes to the model act on the thing.

| | from the thing | to the thing |
|---|---|---|
| digital model | no | no |
| digital shadow | yes | no |
| digital twin | yes | yes |

Most installations called twins are shadows, and for three of the four
purposes that is enough: monitoring, prediction and simulation all run on a
shadow. Only control needs the return channel.

## What decides the technology

Not the word but the latency the purpose requires: hours for prediction,
minutes for monitoring, milliseconds for control, and none at all for
simulation, which runs on its own. That figure decides the cost, and it is the
question to ask before the word twin is used.

The requirement that is missing from demonstrations is the last one on the
list: something that notices when the thing and the model have drifted apart,
rather than smoothing the difference away. That is the same problem as anomaly
detection, in a different vocabulary.
