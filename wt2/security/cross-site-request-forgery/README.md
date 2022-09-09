# Cross-site request forgery

The browser attaches the session cookie by destination, not by origin. A page
on a different site can therefore cause a request that arrives fully
authenticated, without the attacker ever seeing the answer. The attack is
blind and effective.

The module runs it both ways: without the token the transfer succeeds and the
balance drops by 500; with the token required the request is refused, because
the attacker cannot read the token out of a page belonging to another origin.

## What helps

| measure | what it does |
|---|---|
| token in the form | the attacker cannot read it |
| SameSite cookie | the browser does not send the card cross-site |
| origin header check | the browser states where the request came from |
| no state change on GET | removes the easiest way in |

A state-changing GET is the easiest target of all: an `<img src="...">` on
any page triggers it with no interaction. `is_dangerous` marks exactly that
combination.

`SameSite=Strict` and `Lax` both stop the cross-site request; `None` does
not, and that is the setting that exists for the cases where cross-site
requests are wanted.
