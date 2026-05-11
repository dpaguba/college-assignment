# Bilanzierung

Sixteen modules on financial accounting under the German commercial code: the
mechanics of bookkeeping, the valuation rules, the principles behind them, and
what can be read out of the finished accounts.

| Block | Modules | What it holds |
|---|---:|---|
| [bookkeeping](bookkeeping/) | 5 | accounts, entries, the equation, the two formats, the close |
| [valuation](valuation/) | 4 | depreciation, inventory, lower of cost, accruals |
| [principles](principles/) | 3 | the GoB, the structure of the sheet, the measurement rules |
| [analysis](analysis/) | 4 | ratios, DuPont, cash flow, window dressing |

## What the checks found

**A sign error in the accounting equation.** Expense and revenue accounts move
equity in opposite directions, and the first version moved both the same way.
Five entries put the two sides of the balance sheet at 181 000 against
151 000. Both cases now use one formula with the sign of the side, and two
thousand random sequences of eight entries keep the equation.

**The base of the declining rate.** The rate applies to the book value, not to
the book value less the salvage value. The cross-check used the wrong base and
disagreed with the module by a whole switch year; the module was right. With
100 000 €, 10 000 € salvage, five years and 30 %, the switch falls in year 4.

**A parameter that did nothing.** The accrual module took a `months_in_year`
argument, ignored it, and hard-coded one month into the old year. It is now
`months_this_year`, it is used, and an impossible split is rejected.

**"LIFO lowers the profit" is half a rule.** It holds while prices rise.
Reversed to 15, 12, 10 €, FIFO becomes the method with the lowest profit. The
module reports the answer for both directions rather than the slogan.

**The cash flow statement, proved against payments.** Five hundred random sets
of transactions were run through both the indirect method and a direct
computation from the payment flows. The change in cash and the operating
figure agree in every one.

## Two numbers worth keeping

The leverage amplification is the debt-to-equity ratio and it works in both
directions with the same force: one million in assets on 250 000 € of equity
turns a 10 % return on assets into 25 % on equity, and a 5 % return against an
8 % interest rate into **−4 %**. The same 3.0 both times.

Three companies with a 20 % return on equity: one at a 20 % margin, one at 2.5
turns of assets, one at eight times leverage. The ratio is identical, the risk
is not, and the ratio does not say which is which.

## The thread through the subject

Every valuation rule in the middle two blocks distributes a settled total over
time, and every one of them leaves a choice about **when**. The analysis block
then reads ratios that depend on exactly those choices. The last module closes
the circle: the equity ratio moves from 40.0 % to 42.9 % through a sale and
lease back in which nothing about the business changed at all.
