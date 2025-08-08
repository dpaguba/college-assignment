# Input modelling

| Topic | |
|---|---|
| [distribution-fitting](distribution-fitting/) | the family, then the parameters |
| [goodness-of-fit](goodness-of-fit/) | testing the choice |
| [empirical-distributions](empirical-distributions/) | using the data itself |

Chapter four, and the place where a simulation study is most often lost. The
fourth item on the ninth sheet's list of typical mistakes is modelling the
input data wrongly, and the sixth is using means instead of distributions.

The block's concrete result is the limitation of the empirical distribution:
it can never produce a value outside the data, so the tail that fills a
buffer is exactly what it cannot supply. Fitting a family can extrapolate and
might be wrong; not fitting one cannot extrapolate and is certainly
incomplete.
