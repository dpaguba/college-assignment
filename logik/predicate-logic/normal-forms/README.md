# Prenex form, Skolemisation and clause form

Resolution needs clauses, and a first-order formula is not one. Three steps get
it there, and they do **not** all preserve the same thing.

| step | preserves |
|---|---|
| rename apart | equivalence |
| prenex form | equivalence |
| Skolemisation | **satisfiability only** |

Conflating the last two is the standard mistake and it matters:
`forall x exists y R(x,y)` and `forall x1 R(x1,f1(x1))` have different models,
and either both or neither has one.

    forall x exists y R(x,y)
    forall x1 exists y2 R(x1,y2)        prenex, after renaming apart
    forall x1 R(x1,f1(x1))              Skolem form

## Renaming apart is not cosmetic

Pulling two quantifiers that bind the same name to the front makes one capture
what the other bound. The published derivations rename first, with numbered
names, for exactly that reason, and this module produces the same shape:
`exists x P(x) & forall x Q(x)` becomes `exists x1 ... forall x2 ...`.

## The Skolem function takes the enclosing universals

`forall x forall y exists z R(x,y,z)` becomes `forall x1 forall y2
R(x1,y2,f1(x1,y2))`. A leading existential becomes a constant, which is the same
rule with zero arguments rather than a special case.

## The two checks are different questions

`same_models` compares two formulas over every small structure and is the right
check for the prenex step. `satisfiability_agrees` asks only whether both have
a model, and is the right check for Skolemisation.

Calling the first on a Skolem form is the natural thing to try and the wrong
question, so it raises instead of silently mishandling the function symbols.
