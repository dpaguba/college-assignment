# The pumping lemma

For a regular language there is a length n such that every word `w` in it with
`|w| >= n` splits as `w = xyz` with `|xy| <= n`, `|y| >= 1`, and `xy^i z` in
the language for every `i >= 0`.

It is a **necessary** condition only. It proves languages non-regular by
contradiction and never proves one regular, and there are non-regular languages
that pump perfectly well.

## The game

The quantifiers are where exercises go wrong, so the module makes them moves:

1. the adversary picks `n`
2. **you** pick a word in the language with `|w| >= n`
3. the adversary splits it, respecting both constraints
4. **you** pick `i` and show `xy^i z` leaves the language

You win a round by having an answer for **every** split. One surviving split
loses it. Winning for every `n` is the proof, and `refute_regular` plays it and
returns the transcript.

Verified on the three standard languages: `a^n b^n`, palindromes, and
`a^(n²)`.

## The control

`survives_pumping` runs the game the other way, on a language that **is**
regular, and checks that a surviving split exists. Without that control a bug
in the search would happily "prove" that every language is irregular, and the
transcript would look just as convincing.
