"""Class to group information about alphabets.
"""

# There are 29 runes. Generally counted 0-28
# TODO: this parameter needs to be phased out
MAX = 29

LOWERCASE_ALPHABET = [chr(code) for code in range(ord("a"), ord("z") + 1)]
UPPERCASE_ALPHABET = [chr(code) for code in range(ord("A"), ord("Z") + 1)]
DIGITS_ALPHABET = [chr(code) for code in range(ord("0"), ord("9") + 1)]
BASE62_ALPHABET = LOWERCASE_ALPHABET + UPPERCASE_ALPHABET + DIGITS_ALPHABET
CICADA_ALPHABET = [
    "ᚠ",
    "ᚢ",
    "ᚦ",
    "ᚩ",
    "ᚱ",
    "ᚳ",
    "ᚷ",
    "ᚹ",
    "ᚻ",
    "ᚾ",
    "ᛁ",
    "ᛄ",
    "ᛇ",
    "ᛈ",
    "ᛉ",
    "ᛋ",
    "ᛏ",
    "ᛒ",
    "ᛖ",
    "ᛗ",
    "ᛚ",
    "ᛝ",
    "ᛟ",
    "ᛞ",
    "ᚪ",
    "ᚫ",
    "ᚣ",
    "ᛡ",
    "ᛠ",
]

CICADA_ENGLISH_ALPHABET = [
    "F",
    "U",
    "TH",
    "O",
    "R",
    "C",
    "G",
    "W",
    "H",
    "N",
    "I",
    "J",
    "EO",
    "P",
    "X",
    "S",
    "T",
    "B",
    "E",
    "M",
    "L",
    "NG",
    "OE",
    "D",
    "A",
    "AE",
    "Y",
    "IA",
    "EA",
]


class Alphabet:
    """
    Example:
        >>> abc = Alphabet(LOWERCASE_ALPHABET)
    """

    def __init__(self, alphabet: list[str] = UPPERCASE_ALPHABET) -> None:
        """ """
        self.alphabet = alphabet
        self.alphabetsize = len(self.alphabet)

        self.reversealphabet: dict[str, int] = {}
        for i, e in enumerate(self.alphabet):
            self.reversealphabet[e] = i

    def __len__(self) -> int:
        return self.alphabetsize

    def __str__(self) -> str:
        """ """
        return "Alphabet: " + "".join(self.alphabet)

    def a2i(self, a: str) -> int:
        i = self.reversealphabet[a]
        if i is not None:
            return self.reversealphabet[a]
        else:
            raise KeyError("Character not in alphabet")

    def i2a(self, i: int) -> str:
        try:
            return self.alphabet[i]
        except IndexError:
            raise KeyError("Character not in alphabet")


def a2i(text: str) -> list[int]:
    """
    ASCII 2 INTEGER [A-Z] -> [0-25]
    """
    output: list[int] = []
    for c in text:
        output.append(ord(c) - ord("A"))
    return output


def i2a(text: list[int]) -> str:
    """
    INTEGER 2 ASCII [0-25] -> [A-Z]
    """
    output: str = ""
    for c in text:
        output += chr(ord("A") + c)
    return output


def alphabet(text: list[int]) -> list[int]:
    """
    Find all unique values
    """
    return sorted(list(set(text)))


def keyword_to_alphabet(keyword: list[int] = range(0, MAX + 1)):
    """
    construct alphabet order based on keyword
    example:    keyword_to_alphabet(a2i("HYDRAULIC"))
    """
    alphabet = keyword
    return alphabet
