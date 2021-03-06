from ..structures.alphabet import Alphabet
from ..structures.sequence import Sequence


def variant_beaufort_encrypt(
    plaintext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    output: Sequence = Sequence(alphabet=plaintext.alphabet)
    for i in range(0, len(plaintext)):
        output.append(
            variant_beaufort_encrypt_module(
                plaintext[i], primer[i % len(primer)], len(output.alphabet)
            )
        )
    return output


def variant_beaufort_encrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    """
    Variant Beaufort C=P-K
    Note: this is the same as vigenere_decrypt() !!
    """
    return (char - modifier) % alphabetlen


def variant_beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    output: Sequence = Sequence(alphabet=ciphertext.alphabet)
    for i in range(0, len(ciphertext)):
        output.append((ciphertext[i] + primer[i % len(primer)]) % len(output.alphabet))
    return output


def variant_beaufort_decrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    """
    Plain Beaufort P=C+K
    Note: this is the same as vigenere_encrypt() !!
    """
    return (char + modifier) % alphabetlen


def beaufort_encrypt(
    plaintext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    """
    Plain Beaufort C=K-P
    Note: this is the same as beaufort_decrypt() !!
    """
    output: Sequence = Sequence(alphabet=plaintext.alphabet)
    for i in range(0, len(plaintext)):
        # output.append((primer[i % len(primer)] - plaintext[i]) % len(output.alphabet))
        output.append(
            beaufort_encrypt_module(
                plaintext[i], primer[i % len(primer)], len(output.alphabet)
            )
        )
    return output


def beaufort_encrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    return (modifier - char) % alphabetlen


def beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    """
    Plain Beaufort P=K-P
    Note: this is the same as beaufort_encrypt() !!
    """
    output: Sequence = Sequence(alphabet=ciphertext.alphabet)
    for i in range(0, len(ciphertext)):
        # output.append((primer[i % len(primer)] - ciphertext[i]) % len(output.alphabet))
        output.append(
            beaufort_decrypt_module(
                ciphertext[i], primer[i % len(primer)], len(output.alphabet)
            )
        )
    return output


def beaufort_decrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    return (modifier - char) % alphabetlen


def vigenere_encrypt(
    plaintext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    output: Sequence = Sequence(alphabet=plaintext.alphabet)
    print(output)
    print(repr(output))
    for i in range(0, len(plaintext)):
        output.append((plaintext[i] + primer[i % len(primer)]) % len(output.alphabet))
    return output


def vigenere_encrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    """
    Plain Vigenere C=P+K
    """
    return (char + modifier) % alphabetlen


def vigenere_decrypt(
    ciphertext: Sequence, primer: Sequence, trace: bool = False
) -> Sequence:
    output: Sequence = Sequence(alphabet=ciphertext.alphabet)
    for i in range(0, len(ciphertext)):
        output.append((ciphertext[i] - primer[i % len(primer)]) % len(output.alphabet))
    return output


def vigenere_encrypt_module(char: int, modifier: int, alphabetlen: int) -> int:
    """
    Plain Vigenere P=C-K
    """
    return (char - modifier) % alphabetlen


def construct_tabula_recta(alphabet: Alphabet, trace: bool = True):
    """
    construct a tabula recta based on custom alphabet.
    output is a MAX*MAX matrix
    """
    output: list[list[str]] = []
    for shift in range(0, len(alphabet)):
        output.append(alphabet[shift:] + alphabet[:shift])
    if trace:
        print(repr(output))
    return output


"""
The Quagmire group of periodic ciphers are similar to the Vigen??re cipher but use one or more mixed alphabets. There are four variations; I, II, III and IV. The simplest of these, the Quagmire I cipher, is constructed from a keyed plaintext alphabet created from the keyword with repeated letters being omitted and followed by the unused letters of the alphabet in alphabetic order. For example the keyword PAULBRANDT is reduced to PAULBRNDT when repeated letters are removed. Appending unused alphabet letters produces the following keyed alphabet:

PAULBRNDTCEFGHIJKMOQSVWXYZ

The Quagmires 2, 3 and 4 are constructed in a similar way except:

Quagmire 2 uses a straight (A-Z) alphabet for the plaintext and a keyed alphabet for the ciphertext,

Quagmire 3 uses a keyed alphabet for the plaintext and the same keyed alphabet for the ciphertext,

Quagmire 4 uses a keyed alphabet for the plaintext and a different keyed alphabet for the ciphertext.
"""


def vigenere_encrypt_with_alphabet(
    plaintext: Sequence,
    primer: Sequence,
    alphabet: list[int],
    trace: bool = False,
) -> Sequence:
    """
    Vigenere with custom alphabet. Also known as the Quagmire I
    """
    output: Sequence = Sequence()
    if not alphabet:
        alphabet = list(range(0, len(plaintext.alphabet) + 1))
    tr: list[list[int]] = construct_tabula_recta(alphabet)
    abc = list(alphabet)

    for i in range(0, len(plaintext)):
        row_index = abc.index(primer[i % len(primer)])
        row = tr[row_index]
        column_index = abc.index(plaintext[i])
        output.append(tr[row_index][column_index])

    return output


def vigenere_decrypt_with_alphabet(
    ciphertext: Sequence,
    primer: Sequence,
    alphabet: list[int],
    trace: bool = False,
) -> Sequence:
    """
    Plain Vigenere C=P+K
    """
    output: Sequence = Sequence()
    if not alphabet:
        alphabet = list(range(0, len(ciphertext.alphabet) + 1))
    tr: list[list[int]] = construct_tabula_recta(alphabet)

    for i in range(0, len(ciphertext)):
        row_index = alphabet.index(primer[i % len(primer)])
        row = tr[row_index]
        column_index = row.index(ciphertext[i])
        output.append(alphabet[column_index])

    return output


# assume fixed length key. find period
def detect_vigenere(
    ciphertext: list[int],
    minkeysize: int = 1,
    maxkeysize: int = 20,
    trace: bool = False,
):
    print("testing for periodicity using friedman test")
    for period in range(minkeysize, maxkeysize):
        slices = split_by_slice(ciphertext, period)

        iocsum: float = 0.0
        for k in slices.keys():
            ic = normalized_ioc(slices[k])
            iocsum += ic
            if trace is True:
                print(f"ioc of runes {k}/{period} = {ic:.3f}")
        if trace is True:
            print(f"avgioc period {period} = {iocsum/period:.2f}")
