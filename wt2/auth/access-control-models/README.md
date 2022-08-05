# Access control models

An access list names, per object, who may do what. A role model groups
permissions into roles and assigns roles to users. An attribute model
evaluates a rule at the moment of the request.

## The arithmetic

100 users and 50 objects: an access list has up to 5000 entries. With 5 roles
the role model has 100 assignments plus 250 role-object entries, 350 in all.
That is the argument for roles.

It fails when every user needs an individual set of rights: one role per user
plus the shared ones, and the count exceeds the number of users. The role
explosion is the standard failure of the model, and it comes from roles that
were derived from individuals rather than from the organisation.

The attribute model decides at request time, which lets it use the hour, the
location or the state of the object. What it gives up is the ability to
answer "who can read this file" without running every rule.
