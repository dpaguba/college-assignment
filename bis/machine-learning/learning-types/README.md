# The three kinds of learning

**Supervised:** input vectors with their target vectors. The goal is a model
that maps input to output, including for inputs it has not seen. Two tasks:
classification predicts a discrete category, regression a continuous value.

**Unsupervised:** only the inputs. The goal is structure, without knowing in
advance what structure. Clustering, dimension reduction, outlier detection.

**Reinforcement:** no fixed data set but an environment where actions have
consequences. The goal is a policy that maximises reward over time.

## The spam filter

The sheet's own discussion question. The filter's input is the messages:
sender, subject, body, headers. The labels are the decisions people made,
mostly by moving mail into the spam folder. So it is supervised learning with
two classes.

The catch is in where the labels come from. Different people file differently,
and a message one recipient reports is one another keeps. The labels are not
ground truth; they are a record of decisions, and the next module measures
what that costs.
