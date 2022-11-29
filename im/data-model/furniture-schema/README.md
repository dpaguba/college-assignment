# The schema

Five entity types: kunde, artikel, lager, verkaeufer, kassenbon. Five
relations, of which two are the interesting ones.

**kunde_wirbt_kunde** connects the customer with itself: one customer may
recruit several, a recruited one has at most one recruiter. Both ends of the
diamond touch the same rectangle.

**betreut** connects receipt, article and seller. It cannot be replaced by
three binary relations: from "seller served article" and "article is on
receipt" it does not follow which seller sold that article on that receipt,
and that is precisely what the commission accounting needs.

## Where the capacity figures live

Three numbers, three places, and the rule is the same each time: a value
belongs where it depends on.

| Value | Table | Depends on |
|---|---|---|
| kapazitaet | lager | the warehouse alone |
| kap_beanspruchung | artikel | the article alone |
| menge | liegt_in | both |

The capacity requirement of an article is the same wherever it is stored, so
it belongs to the article. The quantity depends on article and warehouse
together, so it belongs to the relation between them.
