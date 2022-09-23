# Webtechnologien 2

Thirty-four modules across eight blocks, from the eleven lectures of the
course: build and dependency management, persistence, REST, the frontend,
authentication and authorization, security, active automata learning, and
delivery.

The folder holds slides only, with no exercises, no solutions and no code, so
what could be verified had to be verified against something else: sqlite3 for
the injection, the standard library's HTML parser for the escaping, an
independently computed HMAC for the token signature, a separately written
partition refinement for the automata, and the documented permission table
for Shiro.

## What the measurements showed

- **The textbook SQL payload fails in the textbook place.** `' OR '1'='1` in
  the name field returns nothing, because AND binds tighter than OR and the
  password check survives. In the password field the same string returns
  every row.
- **L\* learns 55 random automata correctly and minimally**, checked against
  an independent minimisation. With an equivalence oracle that looks only two
  letters deep it returns a one-state model for a four-state language and
  reports success.
- **Nearest wins is decided by declaration order on a tie.** Swapping two
  lines in the project file changes which version of a transitive dependency
  is built.
- **The n+1 problem costs 4 queries where 1 would do**, and the join that
  fixes it reads fewer rows while repeating the parent's columns in each.
- **A single page application transfers less than a server-rendered site only
  after about eleven views.** At five it is still 362 KB against 200.
- **A PATCH is idempotent or not depending on its body**, not its method,
  which is why the specification declines to promise either.
- **A solver that reads four of six CAPTCHA characters succeeds once in
  1296**, from a challenge whose nominal space is two billion.
- **Changing line *p* of a Dockerfile rebuilds every layer from *p* down**,
  and putting the five-second check before the five-minute one turns a
  305-second failure into a 5-second one.
