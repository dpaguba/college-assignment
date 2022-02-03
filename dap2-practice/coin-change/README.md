# Coin change

Greedy change-making in two currencies. Practical sheet 5, task 5.1.

```
java CoinChange Mira 432
Auszugebendes Wechselgeld: 432 Mira
(200,2,32)
(20,1,12)
(10,1,2)
(2,1,0)
Ausgegebenes Wechselgeld: 432 Mira
```

## The two currencies

**Euro:** 1, 2, 5, 10, 20, 50, 100, 200.
**Mira**, invented for the sheet: the same set plus 7 and 9.

Those two extra coins are the point. Euro is a *canonical* coin system, meaning
greedy is optimal for every amount. Mira is not.

## The question the sheet ends with

"Does the procedure always deliver optimal solutions?" No, and
`CoinChangeOptimality` in this folder answers it by computing the optimum with
dynamic programming and comparing:

- Euro, amounts 0 to 5000: **0** disagreements.
- Mira, amounts 0 to 5000: **600** disagreements, the smallest at 14, where
  greedy pays 10 + 2 + 2 and two 7s would do.

It is a separate class on purpose, so that `CoinChange` keeps exactly the output
format the sheet prescribes.

## Why the loop always terminates with nothing owed

Because the smallest coin has value 1, which the sheet states as part of the
currency definition. Drop that and the greedy loop can end holding an amount it
cannot pay at all, which the assertion in `change` would catch.

## Verification

Both sample calls, the result array {2,0,1,0,0,1,0,0} for 455 Euro, and all four
error messages in the prescribed order.
