# The four steps

Select the business process, declare the grain, identify the dimensions,
identify the facts. The order is the content.

The grain says what one row of the fact table means, and until it is fixed
neither of the last two steps is answerable: an attribute is a dimension only
relative to a grain, and a measure belongs in the table only if it is
measured at that grain or coarser.

The module checks exactly that. A design at the grain of one line item
accepts a quantity and an amount and rejects a daily store total, because a
row standing for one line cannot carry a number that belongs to a day.

The grain also decides the size. A retail warehouse at the line item grain
holds a hundred million rows and one at the receipt grain ten million, so the
declaration is a capacity decision as much as a semantic one.
