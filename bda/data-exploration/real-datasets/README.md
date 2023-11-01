# A real data set

Thirty-six rows of the Palmer penguins, twelve per species, embedded so the
module runs without the file, with a loader for the full one.

| species | mean body mass | mean bill length |
|---|---:|---:|
| Adelie | 3704 g | 37.9 mm |
| Chinstrap | 3706 g | 49.1 mm |
| Gentoo | 5238 g | 48.3 mm |

Two things are visible immediately. The overall mean of 4216 grams describes
no species: the closest is more than 400 grams away. And the two measurements
separate different pairs, since the mass tells Gentoo from the rest and says
nothing about Adelie against Chinstrap, while the bill length does the
opposite.

That is why a classifier is given several features and why a summary computed
over everything is the wrong first look at grouped data.
