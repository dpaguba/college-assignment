# Authentication and authorization

Who is asking, and what may they do. Password storage, the choice between a
session and a token, the structure of a signed token and its two known
forgeries, Shiro's permission syntax, and the three models of access control.

The signature check is verified against an independently computed HMAC, and
the permission rules against the documented table, including the asymmetric
case where a narrower permission does not imply a wider one.
