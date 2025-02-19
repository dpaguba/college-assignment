# UNIX file permissions

Three permissions, read, write and execute, at three levels, owner, group and
others. The mode string is parsed rather than read by eye, and converted to
the octal form so both notations can be compared.

## The parliament listing of exercise 1.2

| file | mode | octal | who can read it |
|---|---|---|---|
| `coalition.pptx` | `-rw-rw-r--` | 664 | everyone |
| `g8-topics` | `drwx------` | 700 | the owner only, and it is a directory |
| `ffp2-invoice.pdf` | `-rw-r-----` | 640 | the owner and the group |
| `omicron.sh` | `-rwsr-xr-x` | 4755 | everyone, and it runs as root |

The last line is the one that matters. The `s` in the owner's execute
position is the set-user-id bit: anyone with execute permission may run the
program, and it runs with the rights of its owner, here root. A flaw in that
script is not a flaw with the caller's rights but with root's.

On a directory the three permissions mean something else: read lists the
names, write creates and deletes entries, and execute is what allows passing
through to the files inside. A directory with execute but without read lets
someone open a file whose name they already know while hiding the listing.

The umask takes rights away from the default and never grants any, which the
implementation follows.
