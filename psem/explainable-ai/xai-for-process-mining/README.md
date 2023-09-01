# Explaining a prediction about a running case

A small model predicts whether a case will end in a payout, from three
features of the trace so far: whether documents were requested again, whether
it was escalated, and whether the trace is longer than four events.

The Shapley contributions put most of the weight on the length. The length is
not a cause of the payout; it is a consequence of the same thing, because an
approved case has one more event in it, namely the payout. The model has
learned to recognise the outcome from the outcome.

That is what the explanation is for here. Not to make the prediction look
plausible, but to show that the model uses a feature which cannot be known at
prediction time. It is a leak from the future, and the abstraction from trace
to features is exactly where it entered.
