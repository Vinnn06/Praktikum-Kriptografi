def tampilkan_modulo(bilangan, pembagi):
    if pembagi <= 0:
        raise ValueError("Pembagi harus lebih besar dari 0.")

    hasil_bagi, sisa = divmod(bilangan, pembagi)

    print(
        f"{bilangan} mod {pembagi} = {sisa} "
        f"karena {bilangan} = {hasil_bagi} x {pembagi} + {sisa}"
    )


contoh_perhitungan = [
    (29, 7),
    (100, 12),
    (17, 5),
    (45, 6)
]

for bilangan, pembagi in contoh_perhitungan:
    tampilkan_modulo(bilangan, pembagi)
