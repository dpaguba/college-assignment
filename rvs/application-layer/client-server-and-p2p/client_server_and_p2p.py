"""Client-server against peer-to-peer, as a distribution time.

Sending a file to `n` clients from one server takes at least `n` times the file
size divided by the server's upload rate, because every copy leaves the server.
That is linear in the number of clients and is the whole scalability problem.

In a peer-to-peer distribution every peer uploads what it has received, so the
total upload capacity grows with the number of peers. The time is bounded below
by three things instead of one: the server's upload, the slowest peer's
download, and the total capacity divided by the total demand.
"""

from __future__ import annotations


def client_server_time(peers, size, server_rate, peer_rate):
    """Distribution time with one server sending every copy.

    The maximum of two bounds: the server must push `n` copies, and the slowest
    client must pull one. The first grows with `n` and the second does not,
    which is why the server bound wins for any interesting number of clients.
    """
    return max(peers * size / server_rate, size / peer_rate)


def peer_to_peer_time(peers, size, server_rate, peer_rate, peer_upload=None):
    """Distribution time when peers upload to each other.

    Three bounds: the server must send at least one copy, the slowest peer must
    receive one, and the total upload capacity must carry `n` copies. The third
    grows with `n` in both numerator and denominator, which is why the time
    approaches a constant instead of growing.
    """
    peer_upload = peer_upload if peer_upload is not None else peer_rate
    total_upload = server_rate + peers * peer_upload

    return max(size / server_rate,
               size / peer_rate,
               peers * size / total_upload)


def crossover(size, server_rate, peer_rate):
    """The number of peers at which peer-to-peer starts to win.

    Below it the server is not the bottleneck and the extra complexity buys
    nothing, which is why small deployments are all client-server and why the
    architecture is a function of scale rather than of taste.
    """
    peers = 1
    while peers < 10 ** 6:
        if peer_to_peer_time(peers, size, server_rate, peer_rate) \
                < client_server_time(peers, size, server_rate, peer_rate):
            return peers
        peers += 1
    return None


def server_load(peers, requests_per_peer):
    """Requests a server must handle, which is what a client-server design pays."""
    return peers * requests_per_peer
