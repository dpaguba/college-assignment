"""HTTP: request, response, and where the time goes.

The protocol is text and trivially parseable, which is most of why it won. What
matters for performance is not the parsing but the connection handling, because
every new TCP connection costs a round trip before any data moves.

| scheme | cost for `n` objects |
|---|---|
| non-persistent | `2n` round trips: handshake plus request per object |
| persistent | `1 + n` round trips: one handshake, then one per object |
| persistent and pipelined | `1 + 1` round trips: requests sent back to back |

That table is the entire history of HTTP versions in three rows.
"""

from __future__ import annotations


def parse_request(text):
    """Parse a request into method, target, version and headers."""
    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    method, target, version = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        name, _, value = line.partition(":")
        headers[name.strip()] = value.strip()

    return {"method": method, "target": target, "version": version,
            "headers": headers, "body": body}


def parse_response(text):
    """Parse a response into status, reason and headers."""
    head, _, body = text.partition("\r\n\r\n")
    lines = head.split("\r\n")
    version, status, *reason = lines[0].split()

    headers = {}
    for line in lines[1:]:
        if not line:
            continue
        name, _, value = line.partition(":")
        headers[name.strip()] = value.strip()

    return {"version": version, "status": int(status), "reason": " ".join(reason),
            "headers": headers, "body": body}


def transfer_time(objects, rtt, persistent=True, pipelined=False):
    """Round-trip time to fetch a number of objects, ignoring bandwidth.

    Latency-bound rather than bandwidth-bound, which is the case that matters
    for a page of small objects and the reason persistent connections were
    worth a protocol revision.
    """
    if not persistent:
        return objects * 2 * rtt
    if pipelined:
        return rtt + rtt
    return rtt + objects * rtt


def cache_result(modified):
    """What a conditional request returns.

    `304 Not Modified` carries no body, so a cache revalidation costs one round
    trip and a few bytes rather than the object. That is why caching is
    described as a protocol feature and not as an optimisation.
    """
    if modified:
        return {"status": 200, "body": True}
    return {"status": 304, "body": False}


def status_class(status):
    """The meaning of a status code's first digit."""
    return {1: "informational", 2: "success", 3: "redirect",
            4: "client error", 5: "server error"}[status // 100]


def is_idempotent(method):
    """Whether repeating a request is guaranteed to change nothing more.

    `GET`, `HEAD`, `PUT` and `DELETE` are, `POST` is not. The distinction is
    what lets a proxy retry a request after a timeout, and it is why a browser
    warns before resubmitting a form.
    """
    return method in ("GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE")
