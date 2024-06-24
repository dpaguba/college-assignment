"""What to do when a dimension attribute changes.

A customer moves to another city. Three answers, and they are three different
statements about what the warehouse is for.

Type one overwrites, so the history is gone and every past fact is now
attributed to the new city. Type two adds a row with a validity range, so a
fact stays attached to the value that held when it happened. Type three keeps
one previous value in a second column, which answers "before and after" and
nothing further back.

Only type two answers a question about the past, and it is the only one that
makes the dimension grow.
"""


def apply(kind, rows, change):
    """The dimension after a change, under the given policy."""
    if kind == "type 1":
        return [dict(row, **{key: value for key, value in change.items()
                             if key != "key"})
                if row["key"] == change["key"] else row for row in rows]
    if kind == "type 2":
        result = []
        for row in rows:
            if row["key"] == change["key"] and row.get("valid_to") is None:
                closed = dict(row)
                closed["valid_to"] = "now"
                result.append(closed)
            else:
                result.append(row)
        added = dict(change)
        added["valid_to"] = None
        result.append(added)
        return result
    if kind == "type 3":
        result = []
        for row in rows:
            if row["key"] != change["key"]:
                result.append(row)
                continue
            updated = dict(row)
            for key, value in change.items():
                if key == "key":
                    continue
                updated["previous_" + key] = row.get(key)
                updated[key] = value
            result.append(updated)
        return result
    raise ValueError("unknown policy: %s" % kind)


def answers_history(kind):
    """Whether the policy can answer a question about a past state."""
    answers = {"type 1": False, "type 2": True, "type 3": False}
    if kind not in answers:
        raise ValueError("unknown policy: %s" % kind)
    return answers[kind]


def growth(changes):
    """How many rows one key occupies after that many changes."""
    return {"type 1": 1, "type 2": changes + 1, "type 3": 1}
