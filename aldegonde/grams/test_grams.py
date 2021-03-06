"""
test grams
"""

from ..structures import alphabet, sequence
from .grams import trigrams, tetragrams

nils = sequence.Sequence(data=[0] * 30, alphabet=alphabet.UPPERCASE_ALPHABET)
ones = sequence.Sequence(data=[1] * 30, alphabet=alphabet.UPPERCASE_ALPHABET)
uniq = sequence.Sequence(data=list(range(0, 6)), alphabet=alphabet.UPPERCASE_ALPHABET)
short = sequence.Sequence(data=[0] * 2, alphabet=alphabet.UPPERCASE_ALPHABET)


def test_trigrams():
    """ """
    assert trigrams(short) == []
    assert trigrams(uniq, cut=0) == ["0-1-2", "1-2-3", "2-3-4", "3-4-5"]
    assert trigrams(uniq, cut=1) == ["0-1-2", "3-4-5"]
    assert trigrams(uniq, cut=2) == ["1-2-3"]
    assert trigrams(uniq, cut=3) == ["2-3-4"]


def test_tetragrams():
    """ """
    assert tetragrams(short) == []
    assert tetragrams(uniq, cut=0) == ["0-1-2-3", "1-2-3-4", "2-3-4-5"]
    assert tetragrams(uniq, cut=1) == ["0-1-2-3"]
    assert tetragrams(uniq, cut=2) == ["1-2-3-4"]
    assert tetragrams(uniq, cut=3) == ["2-3-4-5"]
