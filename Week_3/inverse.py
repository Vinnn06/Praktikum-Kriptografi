from math import gcd


def cari_inverse(bilangan, modulus):
    if modulus <= 1:
        raise ValueError("Modulus harus lebih besar dari 1.")

    bilangan = bilangan % modulus

    if gcd(bilangan, modulus) != 1:
        return None

    for kandidat in range(1, modulus):
        if (bilangan * kandidat) % modulus == 1:
            return kandidat

    return None


angka_uji = [3, 5, 7, 2, 11]
modulus = 26

for angka in angka_uji:
    hasil = cari_inverse(angka, modulus)

    if hasil is None:
        print(f"{angka} tidak memiliki inverse modulo {modulus}")
    else:
        print(f"Inverse {angka} modulo {modulus} = {hasil}")
