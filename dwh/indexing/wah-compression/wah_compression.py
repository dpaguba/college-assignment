"""Word-aligned hybrid compression, as the fifth exercise sheet uses it.

A bitmap is cut into groups of one bit less than a word, and each group is
either stored literally or, when several consecutive groups are uniform,
replaced by a fill word that says how many groups of that value follow. The
alignment is the point: a compressed bitmap can be combined with another
without decompressing either, because the words line up.

The exercise's sequence is 1 zero, 20 ones, 3 zeros, 79 ones and 21 zeros,
124 bits in total, and the module encodes it, decodes it back and computes a
conjunction directly on the encoded form.
"""


def encode(bits, word=32):
    """The WAH words of a bit sequence.

    Each word carries one flag bit, so a literal holds word-1 bits and a fill
    counts groups of that size. A run shorter than a full group stays
    literal, which is why alternating bits compress to nothing.
    """
    payload = word - 1
    groups = [bits[index:index + payload]
              for index in range(0, len(bits), payload)]
    if groups and len(groups[-1]) < payload:
        groups[-1] = groups[-1] + [0] * (payload - len(groups[-1]))
    result = []
    index = 0
    while index < len(groups):
        group = groups[index]
        if all(bit == group[0] for bit in group):
            value = group[0]
            count = 0
            while index < len(groups) and all(bit == value
                                              for bit in groups[index]):
                count += 1
                index += 1
            result.append({"kind": "fill", "value": value, "groups": count})
            continue
        result.append({"kind": "literal", "bits": list(group)})
        index += 1
    return result


def decode(words, length, word=32):
    """The bit sequence a list of WAH words stands for."""
    payload = word - 1
    bits = []
    for item in words:
        if item["kind"] == "fill":
            bits.extend([item["value"]] * payload * item["groups"])
        else:
            bits.extend(item["bits"])
    return bits[:length]


def expand_groups(words, word=32):
    """The words as a list of groups, which is what an operation walks."""
    payload = word - 1
    groups = []
    for item in words:
        if item["kind"] == "fill":
            groups.extend([[item["value"]] * payload] * item["groups"])
        else:
            groups.append(list(item["bits"]))
    return groups


def conjunction(first, second, length, word=32):
    """The bitwise and of two encoded bitmaps, computed group by group.

    A fill of zeros meets anything and stays zero, a fill of ones passes the
    other side through, and only two literals need an actual bitwise
    operation. That is the saving the alignment buys, and it is what the
    exercise asks to demonstrate.
    """
    left = expand_groups(first, word)
    right = expand_groups(second, word)
    payload = word - 1
    combined = []
    for index in range(max(len(left), len(right))):
        a = left[index] if index < len(left) else [0] * payload
        b = right[index] if index < len(right) else [0] * payload
        combined.append([x & y for x, y in zip(a, b)])
    bits = [bit for group in combined for bit in group][:length]
    return encode(bits, word)


def compression_ratio(bits, word=32):
    """The size of the encoding against the raw bitmap."""
    words = encode(bits, word)
    return len(words) * word / max(1, len(bits))
