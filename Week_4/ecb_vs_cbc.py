# Praktikum 4C (modifikasi): Perbandingan ECB dan CBC
# Plaintext berpola (A-A-B-A) dienkripsi dengan ECB dan CBC, lalu
# dibandingkan jumlah blok unik pada masing-masing ciphertext.
# CBC dijalankan dua kali dengan IV acak berbeda untuk melihat pengaruh IV.

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

UKURAN_BLOK = AES.block_size
key = b"KunciRahasia2026"
plaintext = b"PRAKTIKUM KRIPTO" * 2 + b"MINGGU KE EMPAT!" + b"PRAKTIKUM KRIPTO"


def pecah_blok(data, ukuran=UKURAN_BLOK):
    return [data[i : i + ukuran] for i in range(0, len(data), ukuran)]


def enkripsi(mode, iv=None):
    if mode == AES.MODE_ECB:
        c = AES.new(key, AES.MODE_ECB)
    else:
        c = AES.new(key, AES.MODE_CBC, iv)
    return c.encrypt(pad(plaintext, UKURAN_BLOK))


def tampilkan(judul, ct):
    blok = pecah_blok(ct)
    print(f"=== {judul} ===")
    for no, b in enumerate(blok, 1):
        print(f"  Blok {no}: {b.hex()}")
    print(f"  -> Blok unik: {len(set(blok))} dari {len(blok)} blok\n")


# ECB
ecb_ct = enkripsi(AES.MODE_ECB)
tampilkan("AES-ECB", ecb_ct)

# CBC dengan dua IV acak yang berbeda
iv1 = get_random_bytes(UKURAN_BLOK)
iv2 = get_random_bytes(UKURAN_BLOK)
cbc_ct1 = enkripsi(AES.MODE_CBC, iv1)
cbc_ct2 = enkripsi(AES.MODE_CBC, iv2)

print("IV-1:", iv1.hex())
tampilkan("AES-CBC (IV-1)", cbc_ct1)
print("IV-2:", iv2.hex())
tampilkan("AES-CBC (IV-2)", cbc_ct2)

# Ringkasan perbandingan
print("=== Ringkasan ===")
print("Ciphertext CBC IV-1 == CBC IV-2 ?", cbc_ct1 == cbc_ct2)
dek = unpad(AES.new(key, AES.MODE_CBC, iv1).decrypt(cbc_ct1), UKURAN_BLOK)
print("Dekripsi CBC (IV-1) sesuai plaintext?", dek == plaintext)
