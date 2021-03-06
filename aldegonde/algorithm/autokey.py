"""
ciphertext autokey variations
we can do 3 operations, 2 subtractions and 1 addition, addition=vigenere, subtraction=beaufort, minuend
C=P+K C=P-K, C=K-P
"""

from ..structures.sequence import Sequence


def ciphertext_autokey_vigenere_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Vigenere primitive without any console output, C=P+K
    """
    assert primer.alphabet == plaintext.alphabet
    key: Sequence = primer.copy()
    output = Sequence(alphabet=plaintext.alphabet)
    MAX = len(plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (plaintext[j] + key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_vigenere_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Vigenere primitive without any console output, P=C-K
    """
    assert primer.alphabet == ciphertext.alphabet
    MAX = len(ciphertext.alphabet)
    key = primer + ciphertext
    output = Sequence(alphabet=ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        output.append((ciphertext[j] - key[j]) % MAX)
    return output


def ciphertext_autokey_beaufort_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Minuend primitive without any console output, C=K-P
    """
    assert primer.alphabet == plaintext.alphabet
    key: Sequence = primer.copy()
    MAX = len(plaintext.alphabet)
    output = Sequence(alphabet=plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (key[j] - plaintext[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Minuend primitive without any console output, P=K-C
    """
    assert primer.alphabet == ciphertext.alphabet
    key: Sequence = primer + ciphertext
    output = Sequence(alphabet=ciphertext.alphabet)
    MAX = len(ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        output.append((key[j] - ciphertext[j]) % MAX)
    return output


def ciphertext_autokey_variant_beaufort_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Beafort primitive without any console output, C=P-K
    """
    assert primer.alphabet == plaintext.alphabet
    key: Sequence = primer.copy()
    output = Sequence(alphabet=plaintext.alphabet)
    MAX = len(plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (plaintext[j] - key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def ciphertext_autokey_variant_beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Beafort primitive without any console output, P=C+K
    """
    assert primer.alphabet == ciphertext.alphabet
    key: Sequence = primer + ciphertext
    output = Sequence(alphabet=ciphertext.alphabet)
    MAX = len(ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        output.append((ciphertext[j] + key[j]) % MAX)
    return output


"""
Combo autokey combines both the plaintext and ciphertext algorithms
"""


def combo_autokey_vigenere_encrypt(
    plaintext: Sequence, primer: Sequence, mode: int = 1
) -> Sequence:
    """
    Vigenere primitive without any console output, C=P+K
    """
    assert primer.alphabet == plaintext.alphabet
    plain_key: Sequence = primer + plaintext
    cipher_key: Sequence = primer
    output = Sequence(alphabet=plaintext.alphabet)
    MAX = len(plaintext.alphabet)
    for j in range(0, len(plaintext)):
        if mode == 1:
            c = (plaintext[j] + plain_key[j] + cipher_key[j]) % MAX
        elif mode == 2:
            c = (plaintext[j] + plain_key[j] - cipher_key[j]) % MAX
        elif mode == 3:
            c = (plaintext[j] - plain_key[j] + cipher_key[j]) % MAX
        elif mode == 4:
            c = (plaintext[j] - plain_key[j] - cipher_key[j]) % MAX
        elif mode == 5:
            c = (-plaintext[j] + plain_key[j] + cipher_key[j]) % MAX
        elif mode == 6:
            c = (-plaintext[j] + plain_key[j] - cipher_key[j]) % MAX
        elif mode == 7:
            c = (-plaintext[j] - plain_key[j] + cipher_key[j]) % MAX
        elif mode == 8:
            c = (-plaintext[j] - plain_key[j] - cipher_key[j]) % MAX
        else:
            raise Exception
        cipher_key.append(c)
        output.append(c)
    return output


def combo_autokey_vigenere_decrypt(
    ciphertext: Sequence, primer: Sequence, mode: int = 1
) -> Sequence:
    """
    Vigenere primitive without any console output, C=P+K
    """
    assert primer.alphabet == ciphertext.alphabet
    plain_key: Sequence = primer
    cipher_key: Sequence = primer + ciphertext
    output = Sequence(alphabet=ciphertext.alphabet)
    MAX = len(ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        # TODO encrypt and decrypt modes don't match
        if mode == 1:
            p = (ciphertext[j] + plain_key[j] + cipher_key[j]) % MAX
        elif mode == 2:
            p = (ciphertext[j] + plain_key[j] - cipher_key[j]) % MAX
        elif mode == 3:
            p = (ciphertext[j] - plain_key[j] + cipher_key[j]) % MAX
        elif mode == 4:
            p = (ciphertext[j] - plain_key[j] - cipher_key[j]) % MAX
        elif mode == 5:
            p = (-ciphertext[j] + plain_key[j] + cipher_key[j]) % MAX
        elif mode == 6:
            p = (-ciphertext[j] + plain_key[j] - cipher_key[j]) % MAX
        elif mode == 7:
            p = (-ciphertext[j] - plain_key[j] + cipher_key[j]) % MAX
        elif mode == 8:
            p = (-ciphertext[j] - plain_key[j] - cipher_key[j]) % MAX
        else:
            raise Exception
        plain_key.append(p)
        output.append(p)
    return output


# plaintext autokey variations
# we can do 3 operations, 2 subtractions and 1 addition, addition=vigenere, subtraction=beaufort, minuend
# C=P+K C=P-K, C=K-P


def plaintext_autokey_vigenere_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Vigenere primitive without any console output, C=P+K
    """
    assert primer.alphabet == plaintext.alphabet
    key = primer + plaintext
    MAX = len(plaintext.alphabet)
    output = Sequence(alphabet=plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (plaintext[j] + key[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_vigenere_encrypt_with_alphabet(
    plaintext: Sequence,
    primer: Sequence,
    alphabet: list[int],
    trace: bool = False,
) -> Sequence:
    """
    Plain Vigenere C=P+K
    """
    assert primer.alphabet == plaintext.alphabet
    key = primer + plaintext
    MAX = len(plaintext.alphabet)
    output: Sequence = Sequence()

    if not alphabet:
        alphabet = list(range(0, MAX + 1))
    tr: list[list[int]] = construct_tabula_recta(alphabet)
    abc = list(alphabet)

    for i in range(0, len(plaintext)):
        row_index = abc.index(key[i])
        row = tr[row_index]
        column_index = abc.index(plaintext[i])
        output.append(tr[row_index][column_index])

    return output


def plaintext_autokey_vigenere_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Vigenere primitive without any console output, P=C-K
    """
    assert primer.alphabet == ciphertext.alphabet
    key: Sequence = primer.copy()
    MAX = len(ciphertext.alphabet)
    output = Sequence(alphabet=ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        c = (ciphertext[j] - key[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def plaintext_autokey_beaufort_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Minuend primitive without any console output, C=K-P
    """
    assert primer.alphabet == plaintext.alphabet
    key: Sequence = primer + plaintext
    output = Sequence(alphabet=plaintext.alphabet)
    MAX = len(plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (key[j] - plaintext[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Minuend primitive without any console output, P=K-C
    """
    assert primer.alphabet == ciphertext.alphabet
    key: Sequence = primer.copy()
    output = Sequence(alphabet=ciphertext.alphabet)
    MAX = len(ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        c = (key[j] - ciphertext[j]) % MAX
        output.append(c)
        key.append(c)
    return output


def plaintext_autokey_variant_beaufort_encrypt(
    plaintext: Sequence, primer: Sequence
) -> Sequence:
    """
    Beafort primitive without any console output, C=P-K
    """
    assert primer.alphabet == plaintext.alphabet
    key: Sequence = primer + plaintext
    output = Sequence(alphabet=plaintext.alphabet)
    MAX = len(plaintext.alphabet)
    for j in range(0, len(plaintext)):
        c = (plaintext[j] - key[j]) % MAX
        output.append(c)
    return output


def plaintext_autokey_variant_beaufort_decrypt(
    ciphertext: Sequence, primer: Sequence
) -> Sequence:
    """
    Beafort primitive without any console output, P=C+K
    """
    assert primer.alphabet == ciphertext.alphabet
    key: Sequence = primer.copy()
    output = Sequence(alphabet=ciphertext.alphabet)
    MAX = len(ciphertext.alphabet)
    for j in range(0, len(ciphertext)):
        p = (key[j] + ciphertext[j]) % MAX
        output.append(p)
        key.append(p)
    return output


# Vigenere Autokey with custom alphabet


def plaintext_autokey_vigenere_encrypt_with_alphabet(
    plaintext: Sequence,
    primer: Sequence,
    # alphabet: list[int] = range(0, MAX + 1),
    trace: bool = False,
) -> Sequence:
    """
    Plain Vigenere C=P+K
    """
    assert primer.alphabet == plaintext.alphabet
    output = Sequence(alphabet=plaintext.alphabet)
    tr: list[list[int]] = construct_tabula_recta(alphabet)

    key: list[int] = primer.copy()
    output: list[int] = []
    for j in range(0, len(plaintext)):
        row_index = alphabet.index(primer[i % len(primer)])
        row = tr[row_index]
        column_index = alphabet.index(plaintext[i])
        c = tr[row_index][column_index]
        output.append(c)
        key.append(c)

    return output


def detect_plaintext_autokey(
    ciphertext: list[int],
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
    ciphertext: list[int],
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

        alphabet: dict[int, list[int]] = {}
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
