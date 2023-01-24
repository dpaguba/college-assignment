# Revenue management

Fixed capacity, a good that perishes at departure, very different willingness
to pay, and advance sale. Littlewood's rule protects seats for the expensive
class as long as the expected revenue from doing so exceeds the certain cheap
fare: `P(D_high ≥ y)·h ≥ l`.

## The off-by-one

The first version used `P(D > y)`, which is one demand level too few: it
protected 20 seats where the exhaustive search over every protection level
found 30, worth 1 100 € of expected revenue. The y-th protected seat is sold
when demand is **at least** y, not more than y, and with a distribution that
jumps in steps of ten the difference is a whole step.

With the comparison corrected the rule matches the search at every price ratio
tested: 30 seats at 150/400, 40 at 80/400, 20 at 300/400, 10 at 350/400.

The search is what caught it. The rule alone looks right either way.

## Only the ratio matters

The absolute fares do not enter, only `l/h`. The closer the cheap fare to the
expensive one, the less is held back, because the certain revenue becomes more
attractive.

## The cost to the customer

The method extracts willingness to pay and customers notice. Sitting next to
someone who paid half feels like a penalty rather than a market outcome. The
industries where it works either have a rule the customer can act on, such as
booking early, or leave the customer no choice at all. The explanation is part
of the method.
