# Permissions

Shiro's wildcard syntax: `resource:action:instance`, with `*` for any value
and commas for several. A missing level on the held side means any value; a
missing level on the wanted side does not.

Checked against the documented table:

| held | wanted | answer |
|---|---|---|
| `printer:print:lp7` | `printer:print:lp7` | yes |
| `printer:print` | `printer:print:lp7` | yes |
| `printer:*` | `printer:print:lp7` | yes |
| `printer:*:lp7` | `printer:print:lp7` | yes |
| `printer` | `printer:print:lp7` | yes |
| `printer:print:lp7` | `printer:print` | **no** |
| `printer:query` | `printer:print` | no |
| `printer:print,query` | `printer:query:lp7` | yes |
| `printer:print:lp7,lp8` | `printer:print:lp8` | yes |
| `*` | anything | yes |

The sixth row is the asymmetry. Holding the right to print on one particular
printer does not grant the right to print in general; the wanted permission
being shorter makes it broader, not narrower.

## Why not check roles

Checking a role couples the code to the organisation: split the role or
rename it and the code changes. Checking a permission asks what is to be
done and survives a reorganisation. Roles hold permissions; the code asks
about permissions.
