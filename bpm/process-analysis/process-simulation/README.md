# Process simulation

Hypothetical cases, played through the model, producing a synthetic log.
What flow analysis cannot give: a distribution rather than a mean, and cost
figures that follow the resources.

The model here is the app release from Zettel 4, with the numbers the sheet
gives: planning varies by an hour, publication by half an hour, bug fixing by
four hours, feature development by a working day. The project manager costs
55 euro an hour, the developers 50, the working student 20.

## What the simulation shows that the formula does not

Both branches of a parallel block cost money; only the longer one costs
time. The mean duration comes out at 24.6 hours, the same as the analytic
value, but the cost is driven by which branches ran, not by how long the case
took. A case that fixes bugs and develops features costs both and takes the
longer of the two.

The spread is the other output the formula cannot produce, and measuring it
turned up something worth keeping. Set every deviation to zero and the
standard deviation is still 8.26 hours: 30 % of releases fix bugs only and
take 12 hours, the other 70 % develop features and take 30. The variation
inside the activities barely adds to that. With the sheet's own deviations
the standard deviation is 10.8, so the branch choice accounts for four fifths
of the spread and the noise for one fifth.

The practical reading: to make the duration of this process predictable, the
lever is the mix of releases, not the discipline of the developers.

One artefact to note. Setting every deviation to 4 hours also moves the mean,
from 24.6 to 25.7, and that is not a real effect: planning has a mean of four
hours, so a deviation of four puts sixteen percent of its draws below zero,
and clipping them at zero pushes the average up. A normal distribution is a
poor model for a short duration, which is worth knowing before trusting a
tool that offers it as the default.

## The caveats the lecture attaches

The results rest on a model and on simplified assumptions; they depend on the
accuracy of the input numbers, so run a sensitivity check; and people are not
machines, so verify the numbers with the people who do the work.
`what_to_watch_out_for` keeps all three, because a simulation output looks
authoritative in a way its inputs usually do not deserve.
