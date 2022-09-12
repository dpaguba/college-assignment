# Cross-site scripting

The page is parsed with the standard library's HTML parser and the executable
elements are collected, so the check is what a reader of the page finds
rather than what a pattern happens to match.

Rendering `<script>steal(document.cookie)</script>` without escaping gives a
page containing a script element. Escaping it gives a page with no executable
element, and the text is still visible.

## The context decides the escaping

| context | what has to be escaped |
|---|---|
| element content | `<` `>` `&` |
| attribute value | the quotes as well |
| url | the scheme, `javascript:` is a scheme |
| script | no foreign text belongs there at all |
| style | nor there |

The attribute case is the one that gets missed: escaping only the angle
brackets leaves `" onerror="steal()` free to close the attribute and open a
new one.

## The three kinds

Stored: the text was saved and is shown to everyone. Reflected: the text
comes back from the request that carried it. DOM based: the page builds the
markup in the browser from a value the server never sees, so no server-side
filter can help.

A content security policy is the second line, and one that permits
`'unsafe-inline'` has given up the protection it was added for.
