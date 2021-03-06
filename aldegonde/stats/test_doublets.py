"""tests for doublets.py"""

from ..structures import sequence, alphabet
from .doublets import doublets, triplets

uniq = sequence.Sequence("ABCDEFGH", alphabet=alphabet.UPPERCASE_ALPHABET)
dobl = sequence.Sequence("AABBCCDDEEFFGGHH", alphabet=alphabet.UPPERCASE_ALPHABET)
trpl = sequence.Sequence(
    "AAABBBCCCDDDEEEFFFGGGHHH", alphabet=alphabet.UPPERCASE_ALPHABET
)


def test_doublets():
    assert doublets(dobl) == [0, 2, 4, 6, 8, 10, 12, 14]
    assert doublets(uniq) == []
    assert doublets(trpl) == [0, 1, 3, 4, 6, 7, 9, 10, 12, 13, 15, 16, 18, 19, 21, 22]


def test_triplets():
    assert triplets(dobl) == 0
    assert triplets(uniq) == 0
    assert triplets(trpl) == 8
