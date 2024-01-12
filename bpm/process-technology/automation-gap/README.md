# The automation gap

Which elements of a conceptual model an engine can interpret, and what to do
about the rest.

Readable: user, service, script, send, receive and business rule tasks. Not
readable: a manual task, a gateway with no condition, a condition whose data
has no source, a text annotation, an activity with no resource.

Each of those has a measure, and `measure_for` gives it: annotate the
gateway, add the data object the condition reads, name the role, and for the
manual task either make it a user task or isolate it.

## The loan process

The exercise sets a constraint that decides the answer: contracts need the
written form, and the electronic form is excluded. So the post and the
signature stay outside the system. They cannot be automated, and they cannot
be dropped either; the only thing left is to make them visible by having
somebody confirm them, so the engine knows when the case may continue.

That is the general shape of the answer to "what cannot be automated here":
usually not a technical limit but a legal or physical one, and the measure is
never automation but visibility.
