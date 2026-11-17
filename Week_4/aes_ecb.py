# Praktikum 4B (modifikasi): Pengujian ECB leakage menggunakan AES-ECB
# Plaintext disusun dari blok 16 byte dengan pola A-A-B-A, lalu ciphertext
# dianalisis untuk mencari blok yang berulang. Hasil juga diverifikasi
# dengan proses dekripsi.

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

UKURAN_BLOK = AES.block_size
key = b"KunciRahasia2026"

blok_a = b"PRAKTIKUM KRIPTO"
blok_b = b"MINGGU KE EMPAT!"
plaintext = blok_a + blok_a + blok_b + blok_a


def pecah_blok(data, ukuran=UKURAN_BLOK):
    return [data[i : i + ukuran] for i in range(0, len(data), ukuran)]


def cari_blok_kembar(blok):
    """Kembalikan dict {hex_blok: [nomor_blok,...]} untuk blok yang muncul > 1 kali."""
    posisi = {}
    for nomor, b in enumerate(blok, 1):
        posisi.setdefault(b.hex(), []).append(nomor)
    return {h: n for h, n in posisi.items() if len(n) > 1}


# --- Enkripsi ---
cipher = AES.new(key, AES.MODE_ECB)
ciphertext = cipher.encrypt(pad(plaintext, UKURAN_BLOK))

print("Panjang plaintext :", len(plaintext), "byte")
print("Panjang ciphertext:", len(ciphertext), "byte\n")

print("=== Plaintext vs Ciphertext per blok ===")
blok_plain = pecah_blok(pad(plaintext, UKURAN_BLOK))
blok_cipher = pecah_blok(ciphertext)
for no, (p, c) in enumerate(zip(blok_plain, blok_cipher), 1):
    teks = "<padding>" if no > len(plaintext) // UKURAN_BLOK else p.decode()
    print(f"Blok {no}: {teks:<18} -> {c.hex()}")

# --- Analisis kebocoran pola ---
print("\n=== Deteksi blok ciphertext yang berulang ===")
kembar = cari_blok_kembar(blok_cipher)
if kembar:
    for h, nomor in kembar.items():
        print(f"{h[:16]}... muncul di blok {nomor}")
else:
    print("Tidak ada blok yang berulang.")

# --- Verifikasi dekripsi ---
hasil_dekripsi = unpad(AES.new(key, AES.MODE_ECB).decrypt(ciphertext), UKURAN_BLOK)
print("\nDekripsi sesuai plaintext asli?", hasil_dekripsi == plaintext)
