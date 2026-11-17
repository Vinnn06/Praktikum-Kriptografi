from math import gcd

ALPHABET_SIZE = 26


def cari_inverse_modulo(bilangan, modulus):
    if modulus <= 1:
        raise ValueError("Modulus harus lebih besar dari 1.")

    bilangan = bilangan % modulus

    if gcd(bilangan, modulus) != 1:
        return None

    for kandidat in range(1, modulus):
        if (bilangan * kandidat) % modulus == 1:
            return kandidat

    return None


def periksa_kunci(kunci):
    if gcd(kunci, ALPHABET_SIZE) != 1:
        raise ValueError(
            f"Kunci {kunci} tidak valid karena " f"gcd({kunci}, {ALPHABET_SIZE}) != 1."
        )


def multiplicative_encrypt(plaintext, kunci):
    periksa_kunci(kunci)
    hasil = []

    for karakter in plaintext:
        if karakter.isalpha():
            dasar = ord("A") if karakter.isupper() else ord("a")
            nilai_awal = ord(karakter) - dasar

            nilai_terenkripsi = (nilai_awal * kunci) % ALPHABET_SIZE

            hasil.append(chr(nilai_terenkripsi + dasar))
        else:
            hasil.append(karakter)

    return "".join(hasil)


def multiplicative_decrypt(ciphertext, kunci):
    inverse = cari_inverse_modulo(kunci, ALPHABET_SIZE)

    if inverse is None:
        raise ValueError(
            f"Kunci {kunci} tidak memiliki " f"inverse modulo {ALPHABET_SIZE}."
        )

    hasil = []

    for karakter in ciphertext:
        if karakter.isalpha():
            dasar = ord("A") if karakter.isupper() else ord("a")
            nilai_cipher = ord(karakter) - dasar

            nilai_asli = (nilai_cipher * inverse) % ALPHABET_SIZE

            hasil.append(chr(nilai_asli + dasar))
        else:
            hasil.append(karakter)

    return "".join(hasil)


plaintext = "HELLO WORLD"
kunci = 5

ciphertext = multiplicative_encrypt(plaintext, kunci)
hasil_dekripsi = multiplicative_decrypt(ciphertext, kunci)

print("Plaintext :", plaintext)
print("Kunci     :", kunci)
print("Ciphertext:", ciphertext)
print("Decrypted :", hasil_dekripsi)


try:
    multiplicative_encrypt(plaintext, 2)
except ValueError as error:
    print("Pengujian kunci 2:", error)
