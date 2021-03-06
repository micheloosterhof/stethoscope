from collections import Counter, defaultdict
import math
import random
from typing import Dict, List

from scipy.stats import poisson

import gematria

g = gematria.gematria

# There are 29 runes. Generally counted 0-28
MAX = 29


class colors:
    reset = "\033[0m"

    # Black
    fgBlack = "\033[30m"
    fgBrightBlack = "\033[30;1m"
    bgBlack = "\033[40m"
    bgBrightBlack = "\033[40;1m"

    # Red
    fgRed = "\033[31m"
    fgBrightRed = "\033[31;1m"
    bgRed = "\033[41m"
    bgBrightRed = "\033[41;1m"

    # Green
    fgGreen = "\033[32m"
    fgBrightGreen = "\033[32;1m"
    bgGreen = "\033[42m"
    bgBrightGreen = "\033[42;1m"

    # Yellow
    fgYellow = "\033[33m"
    fgBrightYellow = "\033[33;1m"
    bgYellow = "\033[43m"
    bgBrightYellow = "\033[43;1m"

    # Blue
    fgBlue = "\033[34m"
    fgBrightBlue = "\033[34;1m"
    bgBlue = "\033[44m"
    bgBrightBlue = "\033[44;1m"

    # Magenta
    fgMagenta = "\033[35m"
    fgBrightMagenta = "\033[35;1m"
    bgMagenta = "\033[45m"
    bgBrightMagenta = "\033[45;1m"

    # Cyan
    fgCyan = "\033[36m"
    fgBrightCyan = "\033[36;1m"
    bgCyan = "\033[46m"
    bgBrightCyan = "\033[46;1m"

    # White
    fgWhite = "\033[37m"
    fgBrightWhite = "\033[37;1m"
    bgWhite = "\033[47m"
    bgBrightWhite = "\033[47;1m"


def a2i(text: str) -> List[int]:
    """
    ASCII 2 INTEGER [A-Z] -> [0-25]
    """
    output: List[int] = []
    for c in text:
        output.append(ord(c) - ord("A"))
    return output


def i2a(text: List[int]) -> str:
    """
    INTEGER 2 ASCII [0-25] -> [A-Z]
    """
    output: str = ""
    for c in text:
        output += chr(ord("A") + c)
    return output


def shuffle(sequence: List[int]) -> List[int]:
    """
    Shuffle elements of a list
    """
    inp = list(sequence)
    output = []
    while len(inp):
        r = random.randrange(0, len(inp))
        output.append(inp[r])
        inp.remove(inp[r])
    return output


def shannon_entropy(ciphertext: List[int], base: int = 2) -> float:
    """
    shannon entropy. by default in bits.
    """
    f = Counter(ciphertext)
    N = len(ciphertext)
    H: float = 0.0
    for k in f.keys():
        H = H - f[k] / N * math.log(f[k] / N, base)
    print(f"Shannon Entropy = {H:.3f} bits (size={N})")
    return H


def shannon2_entropy(runes: List[int], base: int = 2, cut=0) -> float:
    """
    shannon entropy. by default in bits.
    """
    N = len(runes)
    if N < 3:
        return 0.0
    l: list = []
    if cut == 0:
        for i in range(0, N - 1):
            l.append(f"{runes[i]}-{runes[i+1]}")
    elif cut == 1 or cut == 2:
        for i in range(cut - 1, N - 1, 2):
            l.append(f"{runes[i]}-{runes[i+1]}")
    else:
        raise Exception
    f = Counter(l)
    H: float = 0.0
    for k in f.keys():
        H = H - f[k] / N * math.log(f[k] / N, base)
    print(f"S = {H:.3f} bits (size={N})")
    return H


def detect_gronsfeld(runes: List[int]) -> None:
    """
    compare frequency of the 4 most common runes with the 2 least common runes
    """
    freqs = Counter(runes)
    val = sorted(freqs.values())
    p: float = (val[-1] + val[-2] + val[-3] + val[-4]) / (val[0] + val[1])
    print(f"gronsfeld ratio: {p:.2f}")


def repeat_statistics(
    ciphertext: List[int], min: int = 4, max: int = 10, trace: bool = False
):  # -> Dict(List[int], int):
    """
    Find repeating sequences in the list, up to `max`. Max defaults to 10
    Returns dictionary with as key the sequence as a string, and as value the number of occurences
    The expected formula works best for length 4 or larger
    """
    for length in range(min, max + 1):
        l = []
        num = 0
        for index in range(0, len(ciphertext) - length + 1):
            k = "-".join([str(x) for x in ciphertext[index : index + length]])
            l.append(k)
        f = Counter(l)
        for k in f.keys():
            if f[k] > 1:
                num = num + 1

        mu: float = len(ciphertext) / pow(MAX, length)
        expected = pow(MAX, length) * poisson.pmf(2, mu)
        var = poisson.stats(mu, loc=0, moments="v") * pow(MAX, length)
        sigmage: float = abs(num - expected) / math.sqrt(var)
        # sigmage: float = abs(num - expected) / poisson.std(mu)
        print(
            f"repeats length {length}: observed={num:d} expected={expected:.3f} S={sigmage:.2f}??"
        )

        # second method
        expected = len(ciphertext) * (len(ciphertext) - 1) / (2 * pow(MAX, length))
        sigmage: float = abs(num - expected) / math.sqrt(var)
        print(
            f"repeats length {length}: observed={num:d} expected={expected:.3f} S={sigmage:.2f}??"
        )


def monoalphabetic_substitution_encrypt(
    sequence: List[int], key: List[int]
) -> List[int]:
    """
    Monalphabetic substitution
    """
    output = []
    for e in sequence:
        output.append(key[e])
    return output


def reverse_key(key: List[int]) -> List[int]:
    """
    Takes an array containing all elements and reverses the index and the value
    Returns output if the input contains valid values, else raises ValueError
    """
    output = [-1] * len(key)
    for i in key:
        try:
            output[key[i]] = i
        except IndexError:
            raise ValueError
    for i in output:
        if i == -1:
            raise ValueError
    return output


def monoalphabetic_substitution_decrypt(
    sequence: List[int], key: List[int]
) -> List[int]:
    """
    Monalphabetic substitution
    NOTE: key input is the same as for encryption, this function will reverse the key
    """
    reversed_key = reverse_key(key)
    # print(f"revkey: {reversed_key}")
    output = []
    for e in sequence:
        output.append(reversed_key[e])
    return output


def repeat(
    ciphertext: List[int], min: int = 2, max: int = 10
):  # -> Dict(List[int], int):
    """
    Find repeating sequences in the list, up to `max`. Max defaults to 10
    Returns dictionary with as key the sequence as a string, and as value the number of occurences
    """
    sequences = {}
    for length in range(min, max + 1):
        l = []
        for index in range(0, len(ciphertext) - length + 1):
            k = "-".join([str(x) for x in ciphertext[index : index + length]])
            l.append(k)
        f = Counter(l)
        for k in f.keys():
            if f[k] > 1:
                sequences[k] = f[k]

    return sequences


def repeat_statistics(
    ciphertext: List[int], min: int = 2, max: int = 10, trace: bool = False
):  # -> Dict(List[int], int):
    """
    Find repeating sequences in the list, up to `max`. Max defaults to 10
    Returns dictionary with as key the sequence as a string, and as value the number of occurences
    """
    for length in range(min, max + 1):
        l = []
        num = 0
        for index in range(0, len(ciphertext) - length + 1):
            k = "-".join([str(x) for x in ciphertext[index : index + length]])
            l.append(k)
        f = Counter(l)
        for k in f.keys():
            if f[k] > 1:
                num = num + 1

        mu: float = len(ciphertext) / pow(MAX, length)
        expected = pow(MAX, length) * poisson.pmf(2, mu)
        var = poisson.stats(mu, loc=0, moments="v") * pow(MAX, length)
        sigmage: float = abs(num - expected) / math.sqrt(var)
        print(
            f"repeats length {length}: observed={num:.2f} expected={expected:.7f} S={sigmage:.2f}??"
        )


def repeat2(
    ciphertext: List[int], min: int = 2, max: int = 10
):  # -> Dict(List[int], int):
    """
    Find repeating sequences in the list, up to `max`. Max defaults to 10
    Returns dictionary with as key the sequence as a string, and as value the list of starting positions of that substring
    """
    sequences = {}
    for length in range(min, max + 1):
        l: Dict[str, List[int]] = {}
        for index in range(0, len(ciphertext) - length + 1):
            k = "-".join([str(x) for x in ciphertext[index : index + length]])
            if k in l.keys():
                l[k].append(index)
            else:
                l[k] = [index]

        for k in l.keys():
            if len(l[k]) > 1:
                sequences[k] = l[k].copy()

    return sequences


def alphabet(text: List[int]) -> List[int]:
    """
    Find all unique values
    """
    return sorted(list(set(text)))


def randomrunes(l: int, max: int = MAX) -> List[int]:
    """
    Random list of runes of lenth len
    """
    rl = []
    for i in range(0, l):
        rl.append(random.randrange(0, max))
    return rl


def numberToBase(n: int, b: int) -> List[int]:
    """
    converts from base10 to any other base. outputs as list of int
    """
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


def base29(input: int, padding: int = -1) -> List[int]:
    """
    input `int` and output in Base29 as list of integers
    """
    l = numberToBase(input, MAX)
    if padding == -1:
        return l
    else:
        pad_value = 0
        pad_size = padding - len(l)
        final_list = [*[pad_value] * pad_size, *l]
        return final_list


class RuneIterator:
    """
    iterates over runes length L, [0,0,0], [0,0,1], [0,0,2], ..., [0,0,MAX], [0,1,0], ...
    """

    i: int
    maximum: int
    length: int

    def __init__(self, length: int):
        self.length = length
        self.maximum = MAX**length

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= self.maximum:
            raise StopIteration
        else:
            x = self.i
            self.i += 1
            return base29(x, padding=self.length)


def rot(inp: List[int], shift: int) -> List[int]:
    """
    shift contents of list by `shift` mod MAX
    e.g. rot13
    """
    output = []
    for i in inp:
        output.append((i + shift + MAX) % MAX)
    return output


def diffstream(runes: List[int]) -> List[int]:
    """
    diffstream mod MAX
    DIFF = C_K+1 - C_K % MAX
    """
    diff = []
    for i in range(0, len(runes) - 1):
        diff.append((runes[i + 1] - runes[i]) % MAX)
    return diff


def diffstream1(runes: List[int]) -> List[int]:
    """
    diffstream mod MAX
    DIFF = C_K - C_K+1 % MAX
    """
    diff = []
    for i in range(0, len(runes) - 1):
        diff.append((runes[i] - runes[i + 1]) % MAX)
    return diff


def addstream(runes: List[int]) -> List[int]:
    """
    diffstream mod MAX
    DIFF = C_K + C_K+1 % MAX
    """
    diff = []
    for i in range(0, len(runes) - 1):
        diff.append((runes[i + 1] + runes[i]) % MAX)
    return diff


def trigrams(runes: List[int]):
    """
    get the trigrams
    """
    return repeat(runes, min=3, max=3)


def quadgrams(runes: List[int]):
    """
    get the quadgrams
    """
    return repeat(runes, min=4, max=4)


def find(sequence: List[int], runes: List[int]) -> List[int]:
    """
    find `sequence` inside the list of `runes`, return array with indexes
    """
    N = len(runes)
    results = []
    for index in range(0, N - len(sequence) + 1):
        if sequence == runes[index : index + len(sequence)]:
            results.append(index)
    return results


def triplets(runes: List[int]) -> int:
    """
    find number of triplet. triplet is X followed by XX for any X
    """
    N = len(runes)
    triplets: int = 0
    for index in range(0, N - 2):
        if runes[index] == runes[index + 1] and runes[index] == runes[index + 2]:
            triplets += 1
    print(f"triplets = {triplets}")
    expected = N / MAX / MAX
    print(f"expected = {expected:.2f}")
    return triplets


def doublets(runes: List[int], skip: int = 1, trace: bool = False) -> List[int]:
    """
    find number of doublets. doublet is X followed by X for any X
    """
    N = len(runes)
    doublets: List[int] = []
    for index in range(0, N - skip - 1):
        if runes[index] == runes[index + skip]:
            doublets.append(index)
            if trace:
                print(
                    f"doublet at {index}: {runes[index-1]}-{runes[index]}-{runes[index+1]}-{runes[index+2]}"
                )
                print(
                    f" factors N-1: {prime_factors(index-1)}; N: {prime_factors(index)};  N+1: {prime_factors(index+1)} N+2 {prime_factors(index+2)}"
                )
    l: int = len(doublets)

    mu = N / MAX
    mean, var = poisson.stats(mu, loc=0, moments="mv")
    sigmage: float = abs(l - mean) / math.sqrt(var)
    print(f"doublets={l} expected={mean:.2f} S={sigmage:.2f}??")
    return doublets


def dist(runes: List[int]) -> None:
    """
    print frequency distribution
    """
    N = len(runes)
    freqs = Counter(runes)
    print("frequency distribution")
    for rune in range(0, MAX):
        print(f"{rune}: {freqs[rune]/N*100}")


def ioc(runes: List[int]) -> float:
    """
    Monographic Index of Coincidence: ??IC

    Input is a list of integers, from 0 to MAX-1
    Output is the Index of Coincidence formatted as a float

    This output is not normalized to alphabet size
    """
    N = len(runes)
    if N < 2:
        return 0.0
    freqs = Counter(runes)
    freqsum = 0.0
    for rune in range(0, N):
        freqsum += freqs[rune] * (freqs[rune] - 1)
    IC = freqsum / (N * (N - 1))
    return IC


def normalized_ioc(runes: List[int], alphabetsize: int = 0) -> float:
    """
    Like ioc() but normalized by alphabet size.
    """
    if alphabetsize == 0:
        A = len(alphabet(runes))
    else:
        A = alphabet
    return ioc(runes) * A


def ioc2(runes: List[int], cut: int = 0) -> float:
    """
    Digraphic Index of Coincidence: ??IC

    Input is a list of integers, with values from 0 to MAX-1
    Output is the Index of Coincidence formatted as a float

    Specify `cut=0` and it operates on sliding blocks of 2 runes: AB, BC, CD, DE
    Specify `cut=1` and it operates on non-overlapping blocks of 2 runes: AB, CD, EF
    Specify `cut=2` and it operates on non-overlapping blocks of 2 runes: BC, DE, FG
    """
    N = len(runes)
    if N < 3:
        return 0.0
    l: list = []
    if cut == 0:
        for i in range(0, N - 1):
            l.append(f"{runes[i]}-{runes[i+1]}")
    elif cut == 1 or cut == 2:
        for i in range(cut - 1, N - 1, 2):
            l.append(f"{runes[i]}-{runes[i+1]}")
    else:
        raise Exception
    freqs = Counter(l)
    freqsum = 0.0
    for r in freqs.keys():
        freqsum += freqs[r] * (freqs[r] - 1)
    try:
        IC = freqsum / (len(l) * (len(l) - 1))
    except ZeroDivisionError:
        IC = 0.0
    return IC


def normalized_ioc2(runes: List[int], cut: int = 0, alphabetsize: int = 0) -> float:
    """
    Like ioc2() but normalized by alphabet size.
    """
    if alphabetsize == 0:
        A = len(alphabet(runes))
    else:
        A = alphabet
    return ioc2(runes) * pow(A, 2)


def ioc3(runes: List[int], cut: int = 0) -> float:
    """
    Trigraphic Index of Coincidence: ??IC

    Input is a list of integers, with values from 0 to MAX-1
    Output is the Index of Coincidence formatted as a float, normalized to to alphabet size

    Specify `cut=0` and it operates on sliding blocks of 2 runes: ABC, BCD, CDE, ...
    Specify `cut=1` and it operates on non-overlapping blocks of 3 runes: ABC, DEF, ...
    Specify `cut=2` and it operates on non-overlapping blocks of 3 runes: BCD, EFG, ...
    Specify `cut=3` and it operates on non-overlapping blocks of 3 runes: CDE, FGH, ...
    """
    N = len(runes)
    if N < 4:
        return 0.0
    l: list = []
    if cut == 0:
        for i in range(0, N - 2):
            l.append(f"{runes[i]}-{runes[i+1]}-{runes[i+2]}")
    elif cut == 1 or cut == 2 or cut == 3:
        for i in range(cut - 1, N - 2, 3):
            l.append(f"{runes[i]}-{runes[i+1]}-{runes[i+2]}")
    else:
        raise Exception
    freqs = Counter(l)
    freqsum = 0.0
    for r in freqs.keys():
        freqsum += freqs[r] * (freqs[r] - 1)
    try:
        IC = freqsum / (len(l) * (len(l) - 1))
    except ZeroDivisionError:
        IC = 0.0
    return IC


def normalized_ioc3(runes: List[int], cut: int = 0, alphabetsize: int = 0) -> float:
    """
    Like ioc3() but normalized by alphabet size.
    """
    if alphabetsize == 0:
        A = len(alphabet(runes))
    else:
        A = alphabet
    return ioc3(runes) * pow(A, 3)


def ioc4(runes: List[int], cut: int = 0) -> float:
    """
    Tetragraphic Index of Coincidence: ??IC

    Input is a list of integers, with values from 0 to MAX-1
    Output is the Index of Coincidence formatted as a float, normalized to to alphabet size

    Specify `cut=0` and it operates on sliding blocks of 2 runes: ABCD, BCDE, CDEF, ...
    Specify `cut=1` and it operates on non-overlapping blocks of 4 runes: ABCD, EFGH, ...
    Specify `cut=2` and it operates on non-overlapping blocks of 4 runes: BCDE, FGHI, ...
    Specify `cut=3` and it operates on non-overlapping blocks of 4 runes: CDEF, GHIJ, ...
    Specify `cut=4` and it operates on non-overlapping blocks of 4 runes: DEFG, HIJK, ...
    """
    N = len(runes)
    if N < 6:
        return 0.0
    l: list = []
    if cut == 0:
        for i in range(0, N - 3):
            l.append(f"{runes[i]}-{runes[i+1]}-{runes[i+2]}-{runes[i+3]}")
    elif cut == 1 or cut == 2 or cut == 3 or cut == 4:
        for i in range(cut - 1, N - 3, 4):
            l.append(f"{runes[i]}-{runes[i+1]}-{runes[i+2]}-{runes[i+3]}")
    else:
        raise Exception
    freqs = Counter(l)
    freqsum = 0.0
    for r in freqs.keys():
        freqsum += freqs[r] * (freqs[r] - 1)
    IC = freqsum / (len(l) * (len(l) - 1))
    return IC


def normalized_ioc4(runes: List[int], cut: int = 0, alphabetsize: int = 0) -> float:
    """
    Like ioc4() but normalized by alphabet size.
    """
    if alphabetsize == 0:
        A = len(alphabet(runes))
    else:
        A = alphabet
    return ioc4(runes) * pow(A, 4)


def hamming_distance(s1: List[int], s2: List[int]) -> int:
    """
    The Hamming distance between two equal-length strings of symbols
    is the number of positions at which the corresponding symbols
    are different
    """
    if len(s1) != len(s2):
        raise ValueError("Undefined for sequences of unequal length.")
    return sum(el1 != el2 for el1, el2 in zip(s1, s2))


def chi(text1: List[int], text2: List[int]) -> float:
    """
    Calculate chi test of 2 texts

    It's calculated by multiplying the frequency count of one letter
    in the first string by the frequency count of the same letter
    in the second string, and then doing the same for all the other
    letters, and summing the result. This is divided by the product
    of the total number of letters in each string.
    """
    N1 = len(text1)
    N2 = len(text2)
    freqs1 = Counter(text1)
    freqs2 = Counter(text2)
    sum: float = 0.0
    for rune in range(0, MAX):
        sum += freqs1[rune] * freqs2[rune] / (N1 * N2)
    return sum


def kappa(
    ciphertext: List[int],
    min: int = 1,
    max: int = 51,
    threshold: float = 1.3,
    trace: bool = False,
) -> None:
    """
    kappa test
    overlay text with itself and count the number of duplicate letters
    """
    if max == 0:
        max = int(len(ciphertext) / 2)
    for a in range(min, max):
        counter = 0
        dups = 0
        for i in range(0, len(ciphertext) - a):
            counter = counter + 1
            if ciphertext[i] == ciphertext[i + a]:
                dups = dups + 1
        if (dups / counter * MAX) > threshold or trace is True:
            print(f"offset={a:02d}, dups={dups:02d}, ioc={dups/counter*MAX:.3f} ")
    print()


def bigram_diagram(runes: List[int]) -> None:
    """
    Input is a list of integers, from 0 to MAX-1
    Output is the bigram frequency diagram printed to stdout
    """
    count = Counter(runes)
    ioc: float = 0.0
    res = Counter(
        "{:02d}-{:02d}".format(runes[idx], runes[idx + 1])
        for idx in range(len(runes) - 1)
    )

    bigram = defaultdict(dict)
    for k in res.keys():
        x, y = k.split("-")
        bigram[int(x)][int(y)] = res[k]

    print("   | ", end="")
    for i in range(0, MAX):
        print(f"{i:02d} ", end="")
    print("| IOC")
    print("---+-", end="")
    for i in range(0, MAX):
        print(f"---", end="")
    print("+------")

    # for i in sorted(bigram.keys()):
    for i in range(0, MAX):
        print(f"{i:02} | ", end="")
        for j in range(0, MAX):
            # for j in sorted(bigram[i]):
            try:
                v = bigram[i][j]
            except:
                v = 0
            if v == 0:
                print(colors.bgRed, end="")
            elif v < 5:
                print(colors.bgYellow, end="")
            elif v < 10:
                print(colors.bgGreen, end="")
            elif v > 25:
                print(colors.bgBlue, end="")
            print(f"{v:02}", end="")
            print(colors.reset, end=" ")

        # partial IOC (one rune), and total IOC
        pioc = (
            (count[int(i)] * (count[int(i)] - 1))
            / (len(runes) * (len(runes) - 1))
            * MAX
        )
        ioc += pioc
        print("| {0:.3f}".format(pioc))

    print("---+-", end="")
    for i in range(0, MAX):
        print(f"---", end="")
    print("+------")

    print("   | ", end="")
    for i in range(0, MAX):
        print(f"   ", end="")
    print(f"| {ioc:0.3f}")


def bigram_diagram_skip(runes: List[int], skip: int = 1) -> None:
    """
    Input is a list of integers, from 0 to MAX-1
    Output is the bigram frequency diagram printed to stdout
    """
    count = Counter(runes)
    ioc = 0.0
    res = Counter(
        "{:02d}-{:02d}".format(runes[idx], runes[idx + skip])
        for idx in range(len(runes) - skip)
    )
    bigram = defaultdict(dict)

    for k in res.keys():
        x, y = k.split("-")
        bigram[int(x)][int(y)] = res[k]

    print(
        "   | 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 | IOC"
    )
    print(
        "---+----------------------------------------------------------------------------------------+----"
    )

    i: int
    for i in range(0, MAX):
        print(f"{i:02} | ", end="")
        j: int
        for j in range(0, MAX):
            # for j in sorted(bigram[i]):
            try:
                v = bigram[i][j]
            except:
                v = 0
            if v == 0:
                print(colors.bgRed, end="")
            elif v < 5:
                print(colors.bgBlue, end="")
            print(f"{v:02}", end="")
            print(colors.reset, end=" ")

        # partial IOC (one rune), and total IOC
        pioc = (
            (count[int(i)] * (count[int(i)] - 1))
            / (len(runes) * (len(runes) - 1))
            * MAX
        )
        ioc += pioc
        print("| {0:.3f}".format(pioc))

    print(
        "--------------------------------------------------------------------------------------------+----"
    )
    print(
        "                                                                                            | {0:.3f}".format(
            ioc
        )
    )
    print("\n")


# split_by functions offers various methods to split a larger text into smaller text


def split_by_slice(inp: List[int], size: int) -> Dict[int, List[int]]:
    """
    Create slices of the input, with a certain slice size
    This will return every N'th element
    For size 3, it will return a dictionary of lists with elements:
       [0, 3, 6, 9] [1, 4, 7, 10] [2, 5, 8]
    """
    outp = {}
    for i in range(0, size):
        outp[i] = inp[slice(i, len(inp), size)].copy()
    return outp


def split_by_character(inp: List[int]) -> Dict[int, List[int]]:
    """
    by previous character
    """
    outp: Dict[int, List[int]] = {}
    for i in range(0, MAX):
        outp[i] = []
    for i in range(0, len(inp) - 1):
        outp[inp[i]].append(inp[i + 1])
    return outp


def split_by_doublet(ciphertext: List[int]) -> List[List[int]]:
    """
    split in simple chunks separated by a doublet
    """
    output: List[List[int]] = []
    current: List[int] = []
    for i in range(0, len(ciphertext)):
        if ciphertext[i] == ciphertext[i - 1]:
            output.append(current)
            current = [ciphertext[i]]
        else:
            current.append(ciphertext[i])
    output.append(current)
    return output


def variant_beaufort_encrypt(
    plaintext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Variant Beaufort C=P-K
    Note: this is the same as vigenere_decrypt() !!
    """
    output: List[int] = []
    for i in range(0, len(plaintext)):
        output.append((plaintext[i] - primer[i % len(primer)]) % MAX)
    return output


def variant_beaufort_decrypt(
    ciphertext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Plain Beaufort P=C+K
    Note: this is the same as vigenere_encrypt() !!
    """
    output: List[int] = []
    for i in range(0, len(ciphertext)):
        output.append((ciphertext[i] + primer[i % len(primer)]) % MAX)
    return output


def beaufort_encrypt(
    plaintext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Plain Beaufort C=K-P
    Note: this is the same as beaufort_decrypt() !!
    """
    output: List[int] = []
    for i in range(0, len(plaintext)):
        output.append((primer[i % len(primer)] - plaintext[i]) % MAX)
    return output


def beaufort_decrypt(
    ciphertext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Plain Beaufort P=K-P
    Note: this is the same as beaufort_encrypt() !!
    """
    output: List[int] = []
    for i in range(0, len(ciphertext)):
        output.append((primer[i % len(primer)] - ciphertext[i]) % MAX)
    return output


def vigenere_decrypt(
    ciphertext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Plain Vigenere P=C-K
    """
    output: List[int] = []
    for i in range(0, len(ciphertext)):
        output.append((ciphertext[i] - primer[i % len(primer)]) % MAX)
    return output


def vigenere_encrypt(
    plaintext: List[int], primer: List[int] = [0], trace: bool = False
):
    """
    Plain Vigenere C=P+K
    """
    output: List[int] = []
    for i in range(0, len(plaintext)):
        output.append((plaintext[i] + primer[i % len(primer)]) % MAX)
    return output


def construct_tabula_recta(
    alphabet: List[int] = list(range(0, MAX)), trace: bool = True
):
    """
    construct a tabula recta based on custom alphabet.
    output is a MAX*MAX matrix
    """
    output: List[List[int]] = []
    for shift in range(0, MAX):
        output.append(alphabet[shift:] + alphabet[:shift])
    if trace:
        print(repr(output))
    return output


def vigenere_encrypt_with_alphabet(
    plaintext: List[int],
    primer: List[int] = [0],
    alphabet: List[int] = range(0, MAX + 1),
    trace: bool = False,
):
    """
    Plain Vigenere C=P+K
    """
    output: List[int] = []
    tr: List[List[int]] = construct_tabula_recta(alphabet)

    for i in range(0, len(plaintext)):
        row_index = alphabet.index(primer[i % len(primer)])
        row = tr[row_index]
        column_index = alphabet.index(plaintext[i])
        output.append(tr[row_index][column_index])

    return output


def vigenere_decrypt_with_alphabet(
    ciphertext: List[int],
    primer: List[int] = [0],
    alphabet: List[int] = range(0, MAX + 1),
    trace: bool = False,
):
    """
    Plain Vigenere C=P+K
    """
    output: List[int] = []
    tr: List[List[int]] = construct_tabula_recta(alphabet)

    for i in range(0, len(ciphertext)):
        row_index = alphabet.index(primer[i % len(primer)])
        print(f"row index={row_index}")
        row = tr[row_index]
        print(f"row={row}")
        column_index = row.index(ciphertext[i])
        print(f"column index={column_index}")
        # output.append( tr[row_index][column_index] )
        output.append(alphabet[column_index])

    return output


def keyword_to_alphabet(keyword: List[int] = range(0, MAX + 1)):
    """
    construct alphabet order based on keyword
    example:    keyword_to_alphabet(a2i("HYDRAULIC"))
    """
    alphabet = keyword
    return alphabet


# ciphertext autokey variations
# we can do 3 operations, 2 subtractions and 1 addition, addition=vigenere, subtraction=beaufort, minuend
# C=P+K C=P-K, C=K-P


def ciphertext_autokey_vigenere_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Vigenere primitive without any console output, C=P+K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (plaintext[j] + key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_vigenere_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Vigenere primitive without any console output, P=C-K
    """
    key: List[int] = primer + ciphertext
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        output.append((ciphertext[j] - key[j]) % MAX)
    return output


def ciphertext_autokey_minuend_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Minuend primitive without any console output, C=K-P
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (key[j] - plaintext[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_minuend_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Minuend primitive without any console output, P=K-C
    """
    key: List[int] = primer + ciphertext
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        output.append((key[j] - ciphertext[j]) % MAX)
    return output


def ciphertext_autokey_beaufort_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Beafort primitive without any console output, C=P-K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (plaintext[j] - key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_beaufort_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Beafort primitive without any console output, P=C+K
    """
    key: List[int] = primer + ciphertext
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        output.append((ciphertext[j] + key[j]) % MAX)
    return output


# plaintext autokey variations
# we can do 3 operations, 2 subtractions and 1 addition, addition=vigenere, subtraction=beaufort, minuend
# C=P+K C=P-K, C=K-P


def plaintext_autokey_vigenere_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Vigenere primitive without any console output, C=P+K
    """
    key: List[int] = primer + plaintext
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (plaintext[j] + key[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_vigenere_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Vigenere primitive without any console output, P=C-K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        c = (ciphertext[j] - key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def plaintext_autokey_minuend_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Minuend primitive without any console output, C=K-P
    """
    key: List[int] = primer + plaintext
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (key[j] - plaintext[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_minuend_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Minuend primitive without any console output, P=K-C
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        c = (key[j] - ciphertext[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def plaintext_autokey_beaufort_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Beafort primitive without any console output, C=P-K
    """
    key: List[int] = primer + plaintext
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (plaintext[j] - key[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_beaufort_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    Beafort primitive without any console output, P=C+K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        p = (key[j] + ciphertext[j]) % MAX
        output.append(p)
        key.append(p)
    return output


def detect_plaintext_autokey(
    ciphertext: List[int],
    minkeysize: int = 1,
    maxkeysize: int = 20,
    trace: bool = False,
) -> None:
    """
    the way Caesar generalizes to Vigenere,
    a single-letter autokey generalizes to a multi-letter autokey
    to solve it, split it into multiple slices.
    """
    if trace is True:
        print(f"test for plaintext autokey, samplesize={len(ciphertext)}")
        print("#######################################################\n")

    for keysize in range(minkeysize, maxkeysize + 1):
        slices = {}
        vigiocs: float = 0
        miniocs: float = 0
        beaiocs: float = 0
        for start in range(0, keysize):
            slices[start] = ciphertext[start::keysize]
            if trace is True:
                print(f"\nslice={start}: ", end="")
            # Bruteforce Vigenere introductory key at this position
            for key in range(0, MAX):
                plain = plaintext_autokey_vigenere_decrypt(slices[start], [key])
                vigiocs += normalized_ioc(plain)
                if normalized_ioc(plain) > 1.3:
                    if trace is True:
                        print(f"vigenere ioc={normalized_ioc(plain):.2f} ", end="")
            # Bruteforce Beaufort introductory key at this position
            for key in range(0, MAX):
                plain = plaintext_autokey_beaufort_decrypt(slices[start], [key])
                beaiocs += normalized_ioc(plain)
                if normalized_ioc(plain) > 1.3:
                    if trace is True:
                        print(f"beaufort ioc={normalized_ioc(plain):.2f} ", end="")
            # Bruteforce Minuend introductory key at this position
            for key in range(0, MAX):
                plain = plaintext_autokey_beaufort_decrypt(slices[start], [key])
                miniocs += normalized_ioc(plain)
                if normalized_ioc(plain) > 1.3:
                    if trace is True:
                        print(f"minuend ioc={normalized_ioc(plain):.2f} ", end="")
        vigiocavg = vigiocs / MAX / keysize
        miniocavg = miniocs / MAX / keysize
        beaiocavg = beaiocs / MAX / keysize
        if trace is True:
            print(f"\nvigenere keysize={keysize} avgioc = {vigiocavg:0.3f}")
            print(f"\nbeaufort keysize={keysize} avgioc = {beaiocavg:0.3f}")
            print(f"\nminuend  keysize={keysize} avgioc = {miniocavg:0.3f}")
        if vigiocavg > 1.2 or miniocavg > 1.2 or beaiocavg > 1.2:
            print("Attempting bruteforce...")
            if keysize < 4:
                bruteforce_autokey(
                    ciphertext,
                    minkeylength=keysize,
                    maxkeylength=keysize,
                    iocthreshold=1.3,
                )


def detect_ciphertext_autokey_vigenere(
    ciphertext: List[int],
    minkeysize: int = 1,
    maxkeysize: int = 10,
    trace: bool = False,
):
    """
    the way Caesar generalizes to Vigenere,
    a single-letter autokey generalizes to a multi-letter autokey
    to solve it, split it into multiple segments

    split by previous letter and create MAX alphabets. run bigram/ioc on these
    """
    if trace is True:
        print(f"test for ciphertext autokey, samplesize={len(ciphertext)}")
        print("#######################################################\n")

    # length of autokey introductory key
    for a in range(minkeysize, maxkeysize + 1):
        if trace is True:
            print(f"Checking key size {a}")

        alphabet: Dict[int, List[int]] = {}
        for i in range(0, MAX):
            alphabet[i] = []

        for i in range(0, len(ciphertext) - a - 1):
            alphabet[ciphertext[i]].append(ciphertext[i + a])

        tot = 0.0
        for i in alphabet.keys():
            tot += normalized_ioc(alphabet[i])
            if trace is True:
                print(f"IOC: key={i} {normalized_ioc(alphabet[i]):.3f}")
            # dist(alphabet[i])
            # bigram_diagram(alphabet[i])
        print(f"key={a} avgioc={tot/MAX:.3f}")


# assume fixed length key. find period
def detect_vigenere(
    ciphertext: List[int],
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


# assume 1 letter cipher autokey
# split by next letter and create MAX alphabets. run bigram on these
def run_test2a(ciphertext):

    for a in range(1, 20):
        alphabet = {}
        for i in range(0, MAX):
            alphabet[i] = []

        for i in range(0 + a, len(ciphertext)):
            alphabet[ciphertext[i]].append(ciphertext[i - a])

        tot = 0
        for i in alphabet.keys():
            tot += normalized_ioc(alphabet[i])
            # bigram_diagram(alphabet[i])
            # print("key={}: ioc of runes before {} = {}".format(a, i, ioc(alphabet[i])))
        print(f"key={a} avgioc={tot/MAX:.3f}")


# assume fixed length key. find period
def run_test3(ciphertext: List[int], trace: bool = False):
    print("testing for fixed size periodicity")
    for period in range(1, 30):
        group: Dict[int, List[int]] = {}
        for i in range(period):
            group[i] = []

        for i in range(0, len(ciphertext)):
            group[i % period].append(ciphertext[i])

        iocsum = 0.0
        for k in group.keys():
            iocsum += float(normalized_ioc(group[k]))
            # print("ioc of runes {}/{} = {}".format(k, period, ioc(group[k])))

        if trace is True or iocsum / period > 1.0:
            print(f"avgioc period {period} = {iocsum/period:.2f}")


# test cipher autokey
def offset():
    # offset is the main variable, how much we are overlaying the data
    print("OFFSET: 1\n")

    output = []
    for j in range(0, len(gl)):
        transform = (gl[j] - gl[(j + 1) % len(gl)]) % MAX

        output.append((gl[j] - gl[(j + 1) % len(gl)]) % MAX)

    # print sample
    samplesize = 10
    print("CIPHER: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(gl[i]), end="")
    print()
    print("OFFSET: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(gl[(1 + i) % len(gl)]), end="")
    print()
    print("OUTPUT: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(output[i]), end="")

    # print("\nOUTPUT: ", end="")
    # for i in range(0,samplesize*3):
    #    print("{:2} ".format(g.position_to_latin_forward_dict[output[i]]), end="")

    print("IOC: " + normalized_ioc(output))
    bigram_diagram(output)


# test cipher autokey
def offset_reverse():
    # offset is the main variable, how much we are overlaying the data
    offset = 5
    print(f"OFFSET: {offset}\n")

    output = []
    for j in range(0, len(gl)):
        transform = (gl[j - 1] - gl[(j) % len(gl)]) % MAX

        output.append((gl[j] + offset - gl[(j - 1) % len(gl)]) % MAX)

    # print sample
    samplesize = 10
    print("CIPHER: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(gl[i]), end="")
    print()
    print("OFFSET: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(gl[(offset + i) % len(gl)]), end="")
    print()
    print("OUTPUT: ", end="")
    for i in range(0, samplesize):
        print("{:2} ".format(output[i]), end="")

    # print("\nOUTPUT: ", end="")
    # for i in range(0,samplesize*3):
    #    print("{:2} ".format(g.position_to_latin_forward_dict[output[i]]), end="")

    print("IOC: " + normalized_ioc(output))
    bigram_diagram(output)


# test cipher autokey
def run_test4():
    print("\n\n\nLP\n")
    print("IOC: " + normalized_ioc(gl))
    bigram_diagram(gl)

    # now overlay list with itself
    # offset is the main variable, how much we are overlaying the data
    for offset in range(0, MAX):

        print(f"\n\n\nOFFSET: {offset}\n")

        output = []
        for j in range(0, len(gl)):
            output.append((gl[j] + offset - gl[(j - 1) % len(gl)]) % MAX)

        # print sample
        samplesize = 10
        print("CIPHER: ", end="")
        for i in range(0, samplesize):
            print("{:2} ".format(gl[i]), end="")
        print()
        print("OFFSET: ", end="")
        for i in range(0, samplesize):
            print("{:2} ".format(gl[(1 + i) % len(gl)]), end="")
        print()
        print("OUTPUT: ", end="")
        for i in range(0, samplesize):
            print("{:2} ".format(output[i]), end="")

        print("\nOUTPUT: ", end="")
        for i in range(0, samplesize * 3):
            print("{:2} ".format(g.position_to_latin_forward_dict[output[i]]), end="")

        print()

        print("IOC: " + normalized_ioc(output))
        bigram_diagram(output)


def ignore():
    for offset in range(1, 20):
        print(f"OFFSET: {offset}")
        x = autokey_vigenere(gl, offset=offset)
        print("number of dups: " + str(len(repeat(x).keys())))
        y = split_by_character(x)
        for k in y.keys():
            print(normalized_ioc(y[k]), end=" ")
        print()


def prime_factors(n: int) -> List[int]:
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors


def primes(n):
    out = list()
    sieve = [True] * (n + 1)
    for p in range(2, n + 1):
        if sieve[p]:
            out.append(p)
            for i in range(p, n + 1, p):
                sieve[i] = False
    return out


"""
2vig are vigenere variants that look 2 characters back rather than one
"""


def ciphertext_autokey_vig2_encrypt(
    plaintext: List[int], primer: List[int] = [0, 0]
) -> List[int]:
    """
    2Vig primitive without any console output, C=P+K1+K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(plaintext)):
        c = (plaintext[j] - key[j + 1] + key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_vig2_decrypt(
    ciphertext: List[int], primer: List[int] = [0, 0]
) -> List[int]:
    """
    2Vig primitive without any console output, P=C-K
    """
    key: List[int] = primer + ciphertext
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        output.append((ciphertext[j] + key[j + 1] - key[j]) % MAX)
    return output


def ciphertext_autokey_oddvig_encrypt(
    plaintext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    2Vig primitive without any console output, C=P+K1+K
    """
    key: List[int] = primer.copy()
    output: List[int] = []
    for j in range(0, len(plaintext)):
        if j % 2 == 0:
            c = (plaintext[j] + key[j]) % MAX
        else:
            c = (plaintext[j] - key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_oddvig_decrypt(
    ciphertext: List[int], primer: List[int] = [0]
) -> List[int]:
    """
    2Vig primitive without any console output, P=C-K
    """
    key: List[int] = primer + ciphertext
    output: List[int] = []
    for j in range(0, len(ciphertext)):
        if j % 2 == 0:
            p = (ciphertext[j] - key[j]) % MAX
        else:
            p = (ciphertext[j] + key[j]) % MAX
        output.append(p)
    return output


def english_output(runes: List[int], limit=0) -> None:
    """
    prints rune output translated back to english letters
    """
    if limit == 0 or limit > len(runes):
        limit = len(runes)

    print("--: ", end="")
    for i in range(0, limit):
        print("{:2} ".format(runes[i]), end="")
    print()

    print("--: ", end="")
    for i in range(0, limit):
        print("{:2} ".format(g.position_to_latin_forward_dict[runes[i]]), end="")
    print()


def bruteforce_autokey(
    ciphertext: List[int],
    minkeylength: int = 1,
    maxkeylength: int = 1,
    iocthreshold: float = 1.2,
    trace: bool = False,
) -> None:
    """
    bruteforce vigenere autokey and variants
    """
    algs = {
        "ciphertext_vigenere": ciphertext_autokey_vigenere_decrypt,
        "ciphertext_beaufort": ciphertext_autokey_beaufort_decrypt,
        "ciphertext_minuend": ciphertext_autokey_minuend_decrypt,
        "plaintext_vigenere": plaintext_autokey_vigenere_decrypt,
        "plaintext_beaufort": plaintext_autokey_beaufort_decrypt,
        "plaintext_minuend": plaintext_autokey_minuend_decrypt,
    }
    for keylength in range(minkeylength, maxkeylength + 1):
        for key in RuneIterator(keylength):
            for a in algs.keys():
                p = algs[a](ciphertext, key)
                ic = normalized_ioc(p)
                if ic > iocthreshold or trace:
                    print(f"key {key}: {ic}: ")
                    english_output(p, limit=30)

    return


def gcd(p, q):
    # Create the gcd of two positive integers.
    while q != 0:
        p, q = q, p % q
    return p


def is_coprime(x, y):
    return gcd(x, y) == 1


def phi_func(x):
    """
    euler phi // totient
    """
    if x == 1:
        return 1
    else:
        n = [y for y in range(1, x) if is_coprime(x, y)]
        return len(n)


def isomorph(ciphertext: List[int]) -> str:
    """
    Input is a piece of ciphertext as a list of int
    Output is this normalized as an isomorph, it's output as a string for easy comparison in alphabet A-Z
    Example ATTACK and EFFECT both normalize to ABBACD
    """
    output = ""
    letter = "A"
    mapping: Dict[int, str] = {}
    for r in ciphertext:
        if r not in mapping:
            mapping[r] = letter
            letter = chr(ord(letter) + 1)
        output = output + mapping[r]
    return output
