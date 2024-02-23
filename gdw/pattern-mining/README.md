# Pattern mining

| Topic | |
|---|---|
| [apriori](apriori/) | one property, and the pruning it allows |
| [association-rules](association-rules/) | confidence, and why it is not enough |
| [closed-itemsets](closed-itemsets/) | keeping fewer sets, losing nothing or something |

The fifth lecture and the fourth exercise sheet. Apriori counts 8 candidates
where the lattice has 15 and agrees with brute force, which is the smallest
useful demonstration of a pruning rule.

The result worth remembering is about rules rather than itemsets: a rule with
87.5 percent confidence can be worse than guessing, because the item it
predicts occurs in 90 percent of the transactions. Confidence measures the
rule against nothing, and lift measures it against independence.
