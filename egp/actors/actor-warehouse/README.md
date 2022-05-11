# The warehouse

Exercise 2 of sheet 4. Three workers each decide at random to store or
retrieve one unit. The store must guarantee that nothing is taken from an
empty store; a worker who tries gets an error and stops asking. The store
starts with three units.

The guarantee costs nothing to implement, because it follows from the model:
the store handles one message at a time, so two workers cannot both take the
last unit. Checked over forty runs, the stock never goes below zero.

## What would break it

Move the decision out of the store. If a worker first asks for the level and
then decides whether to take, another worker can get in between, and both
take the last unit. The model does not prevent that; it only prevents two
messages being handled at once.

The rule that follows is short: the decision belongs where the state is.

## The runs do not all end

A worker only stops after an error, and an error only happens when the store
is empty. If the random decisions keep the store stocked, nobody stops. Some
runs therefore reach the message limit with workers still active, which is
the behaviour of the system and not a defect in the simulation.
