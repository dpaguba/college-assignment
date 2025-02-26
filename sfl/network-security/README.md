# Network security

Five modules covering exercise 7 and the two network lectures: packet
filters, the certificate infrastructure, overload attacks, onion routing and
the attacks on an encrypted connection.

The two rule sets of exercise 7.1 are written out and executed against
packets rather than only tabulated, including the answer rule that needs
connection state.

Three results worth carrying:

- A browser trusts about 150 roots and every one may issue for every name, so
  the number an attacker must compromise is one.
- Onion routing is defeated by holding both ends of a circuit, or by watching
  both ends of the network without holding anything.
- None of the four transport attacks breaks a cipher. They read the
  negotiated version, the size, the answer or the timing, which is why the
  answer to all of them is authenticated encryption and identical error
  handling.
