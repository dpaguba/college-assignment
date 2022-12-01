# Mapping to relations

The rules: each entity type becomes a relation with its key as primary key;
an n:m relation becomes a relation of its own whose key is both foreign keys;
a 1:n relation needs no relation, the foreign key moves to the side with the
1; attributes of a relation go into the relation's table or they are lost.

## Two places where the rules and the tutorial disagree

**kunde_wirbt_kunde.** By the rules the recruited side has at most one
recruiter, so the foreign key belongs in the customer table as `knr_alt`,
next to `knr`, and no separate table is needed. Tutorial six creates one
anyway. Both choices work, and the tutorial's has two arguments in
its favour: the customer table stays free of a column that is empty for most
customers, and the relation can acquire an attribute later, such as the date
of the referral.

**betreut.** As a ternary relation it would take a key of all three foreign
keys. In the data of the tutorial the pair of receipt and article already
determines the seller: there are no two rows with the same pair. The relation
is therefore binary with the seller as an attribute, and its key has two
columns rather than three.

Both are recorded in `where_the_rules_and_the_data_disagree` rather than
resolved silently. The rules describe what must be possible; the data says
what is actually the case, and where they differ, the difference is the
finding.

## The role name

Because both ends of the recursive relation point at the same key, the
foreign key needs a name of its own. Without renaming, the column would
appear twice under the same name in the same relation.
