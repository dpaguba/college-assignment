# Precision and recall

Precision asks what share of the positive predictions is right; recall asks
what share of the positive cases is found. On the ninth sheet's example both
come to two thirds and the F measure, their harmonic mean, comes to two
thirds as well.

Neither number alone means anything. Predicting everything positive gives a
recall of one and a precision equal to the base rate, which the module
checks, so a recall without a precision is not a result.

The curve is the summary that keeps both. As the threshold falls, recall
rises and precision falls, and the shape of that trade is a property of the
model while the point chosen on it is a decision about the cost of each kind
of error.
