# Huffman coding

Chapter six. Repeatedly join the two least frequent subtrees, and the result
is a prefix-free code of minimal weighted path length.

On 126 characters of German prose:

| | |
|---|---:|
| fixed eight bits per character | 1008 bits |
| Huffman code | 520 bits |
| saved | 48.4 percent |
| shortest code, for `e` | 3 bits |
| longest code | 7 bits |

The frequent characters get the short codes, which is the whole idea, and the
saving depends entirely on how uneven the frequencies are. A text where every
character occurs equally often gets no saving at all, and the code degenerates
into a fixed-width one.

## Prefix freedom is what makes decoding possible

No code is a prefix of another, so a decoder walking the tree from the root
is never in doubt about where one code ends and the next begins. That is why
the encoded bits need no separator, and it is a property of the construction:
codes sit at leaves, and a leaf has no descendants.

The property is checked directly rather than assumed, and so is the length: the
encoded output has to be exactly the sum over characters of frequency times
code length, computed from the tree rather than from the output. The two
disagree if the encoder and the tree ever fall out of step.

## The single-character case

A text of one distinct character produces a tree with one node, so the code
would be the empty string and the encoding would be nothing at all. The
convention here is a single zero per occurrence, which keeps the round trip
exact. Every construction of this kind has such a case, and it is where an
implementation that was never tested on it fails.

Verified by round trip on 60 random texts over alphabets of one to eight
characters, with the prefix property and the length identity checked each
time.
