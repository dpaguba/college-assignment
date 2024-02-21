"""Shingling: turning a document into a set so that sets can be compared.

A shingle is a window of consecutive characters or words, so a document
becomes the set of its windows. The length decides how much order survives:
single characters keep almost none, and long shingles keep so much that two
documents share nothing unless they are nearly identical.

Word shingles of length two or three are the usual choice for text, and they
are what the seventh sheet uses, because they survive small edits and still
notice a reordering.
"""


def shingles(text, size):
    """The set of character windows of the given length."""
    if size > len(text):
        return set()
    return {text[index:index + size] for index in range(len(text) - size + 1)}


def word_shingles(text, size):
    """The set of word windows of the given length."""
    words = text.split()
    if size > len(words):
        return set()
    return {" ".join(words[index:index + size])
            for index in range(len(words) - size + 1)}


def sample_text():
    """A varied paragraph, so the shingle counts mean something.

    Repeating one sentence produces the same shingles over and over, which is
    the trap in measuring a corpus by its length: the number of distinct
    shingles depends on the variety and not on the size.
    """
    words = ("the quick brown fox jumps over a lazy dog while nine sailors "
             "watch from a stone bridge and count every passing barge").split()
    sentences = []
    for offset in range(40):
        rotated = words[offset % len(words):] + words[:offset % len(words)]
        sentences.append(" ".join(rotated[:8]))
    return " ".join(sentences)


def hashed(text, size, buckets=2 ** 20):
    """The shingles reduced to bucket numbers, which is what is stored.

    Storing the strings costs more than the document. Hashing them into four
    byte numbers keeps the comparison and drops the text, at the price of a
    collision rate that the bucket count controls.
    """
    return {hash(shingle) % buckets for shingle in word_shingles(text, size)}
