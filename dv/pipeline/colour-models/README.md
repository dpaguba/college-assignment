# Colour models

RGB is additive and made for screens, CMY subtractive and made for print,
HSV separates what a colour is from how strong and how bright it is, and CIE
Lab is built so that equal steps look equally large.

The conversion here is checked against `colorsys` from the standard library
for every colour tried, and inverting it returns the original to nine
decimals.

## Grey is not the mean of the channels

`rgb_to_grey` weights the channels 0.2126, 0.7152 and 0.0722. Pure green
comes out at 0.72 and pure blue at 0.07, because the eye is far more
sensitive to green. Averaging the three channels would make them equally
bright, which is wrong in a way that is easy to see once the image is next to
the correct one.

## The path between two colours depends on the model

Mixing red and green halfway in RGB gives a dark yellow-brown; doing it in
HSV walks around the hue circle and gives a saturated yellow. The two
midpoints are far apart, which the module measures. Neither is the correct
answer: the model decides what "halfway" means.
