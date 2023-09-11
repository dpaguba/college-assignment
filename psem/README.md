# Proseminar Enterprise Computing

A seminar, so the folder holds method rather than lectures: a kick-off, three
decks on writing and presenting, a library course on searching, a slide
template, a sample extended abstract and an excursus on generative language
models. The student's
own paper is not in it.

What is in it is nineteen papers of entry literature for ten topics, and those
are the seminar. Sixteen modules follow them.

| Block | Modules | What it holds |
|---|---:|---|
| [explainable-ai](explainable-ai/) | 5 | Shapley values, SHAP, surrogates, box colours, process mining |
| [anomaly-detection](anomaly-detection/) | 5 | the taxonomy, three detectors, and how to score them |
| [automation](automation/) | 3 | RPA to IPA, what automates, digital twins |
| [adoption](adoption/) | 3 | UTAUT, real-time analytics, classifier systems |

## Two findings about the folder itself

`01-01.pdf` and `02-01.pdf` are byte-identical, and so are `01-02.pdf` and
`02-02.pdf`: topic 2 reuses two of topic 1's three papers, and only its third
is its own.

That third one, `02-03.pdf`, yields no usable text. It is a scan whose text
layer is a vertical watermark, so a text extractor returns a column of single
letters. Rendered as an image it reads normally: Dunia, Qin, Edgar and McAvoy,
"Identification of Faulty Sensors Using Principal Component Analysis", AIChE
Journal 1996. That paper is the basis of the PCA module.

## Four measured results

**A z-score misses the outlier it is meant to find.** In 10, 11, 9, 10, 12,
11, 10, 9, 200 the 200 has a z-score of 2.83 and stays under the usual
threshold of 3, because it raises the mean and the deviation it is measured
against. The interquartile rule finds it.

**A local outlier factor sees what a distance cannot.** On data with a dense
and a sparse cluster, a point inserted just outside the dense one ranks 14th
of 92 by distance to its fifth neighbour and 2nd by local factor.

**A sensor fault inside the normal range is detectable and not
identifiable.** With four correlated sensors and two components, every
injected fault is detected well below the sensor's own limits, and only two of
four are attributed to the right sensor. That is the identifiability condition
of the paper: two fault directions have to differ in the residual space, and
four directions do not fit distinguishably into two dimensions.

**The interpretable model costs 44 points on one task and nothing on
another.** On the sign of a product of two features a decision stump gets
51.8 % against 95.8 % for nearest neighbours; on the sign of a single feature
the stump gets 100 % and the neighbours 98.5 %. The question is never whether
interpretability costs accuracy but whether it costs it here.
