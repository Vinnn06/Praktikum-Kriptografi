# Praktikum 4A (modifikasi): Demonstrasi konsep ECB leakage
# dengan "toy cipher" berbasis pergeseran huruf (Caesar) + pembalikan blok.
# Catatan: ini BUKAN enkripsi sungguhan, hanya untuk memperlihatkan prinsip ECB.

from collections import defaultdict

KUNCI_GESER = 3
UKURAN_BLOK = 4


def toy_block_encrypt(blok, kunci):
    """Geser setiap huruf sejauh `kunci`, lalu balik urutan blok."""
    hasil = ""
    for ch in blok:
        if ch.isalpha():
            hasil += chr((ord(ch.upper()) - 65 + kunci) % 26 + 65)
        else:
            hasil += ch
    return hasil[::-1]


def pecah_blok(pesan, ukuran):
    """Bagi pesan menjadi blok-blok dengan ukuran tetap (sisa diberi padding '_')."""
    blok = [pesan[i : i + ukuran] for i in range(0, len(pesan), ukuran)]
    blok[-1] = blok[-1].ljust(ukuran, "_")
    return blok


def ecb_toy_encrypt(pesan, ukuran, kunci):
    """Mode ECB: setiap blok dienkripsi sendiri-sendiri dengan kunci yang sama."""
    blok_plain = pecah_blok(pesan, ukuran)
    blok_cipher = [toy_block_encrypt(b, kunci) for b in blok_plain]
    return blok_plain, blok_cipher


def cari_pola(blok_cipher):
    """Kelompokkan nomor blok berdasarkan isi ciphertext yang sama."""
    posisi = defaultdict(list)
    for nomor, c in enumerate(blok_cipher, 1):
        posisi[c].append(nomor)
    return posisi


pesan = "UAJYUAJYINFOINFOUAJYUAJYINFOINFO"
plain, cipher = ecb_toy_encrypt(pesan, UKURAN_BLOK, KUNCI_GESER)

print("Pesan asli :", pesan)
print(f"Kunci geser: {KUNCI_GESER} | Ukuran blok: {UKURAN_BLOK}\n")

print(f"{'No':<4}{'Plaintext':<12}{'Ciphertext':<12}")
print("-" * 28)
for no, (p, c) in enumerate(zip(plain, cipher), 1):
    print(f"{no:<4}{p:<12}{c:<12}")

print("\n=== Analisis pola ciphertext ===")
for c, nomor in cari_pola(cipher).items():
    print(f"Blok '{c}' muncul {len(nomor)} kali di posisi {nomor}")

print(f"\nJumlah blok: {len(cipher)} | Blok unik: {len(set(cipher))}")
