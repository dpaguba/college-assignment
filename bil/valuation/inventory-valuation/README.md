# Inventory valuation

Three purchases of 100 units at 10 €, 12 € and 15 €, 150 units used. The goods
available are worth 3 700 €, and each method splits that same 3 700 € between
expense and closing stock.

| Method | Cost of goods sold | Closing stock |
|---|---:|---:|
| FIFO | 1 600 | 2 100 |
| average | 1 850 | 1 850 |
| LIFO | 2 100 | 1 600 |

Verified against a list of the individual units: FIFO takes the first 150
prices, LIFO the last 150, and the average takes 150 times the weighted mean.
Every split adds back to 3 700 €. No method creates or destroys value; each
one only decides how much of it becomes expense now and how much later.

## The rule that only half holds

"LIFO lowers the profit" is quoted without its condition. It holds while
prices rise. Reverse the price series to 15 €, 12 €, 10 € and FIFO becomes the
method with the lowest profit. The module runs both directions and reports
which method is lowest in each.

## The trade-off

FIFO leaves a closing stock near the current price and an expense that lags
behind it. LIFO does the opposite: the expense is current, the stock is stale.
One of the two figures is always out of date, and which one matters depends on
whether the reader is looking at the result or at the balance sheet.
