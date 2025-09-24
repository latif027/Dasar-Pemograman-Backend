import penambahan
import pengurangan
import perkalian
import pembagian

# Input dari user
a = float(input("Masukkan angka pertama : "))
b = float(input("Masukkan angka kedua  : "))

# Proses dengan modul
print("Penambahan  dari", a, "dan", b, "adalah", penambahan.tambah(a, b))
print("Pengurangan dari", a, "dan", b, "adalah", pengurangan.kurang(a, b))
print("Perkalian   dari", a, "dan", b, "adalah", perkalian.kali(a, b))
print("Pembagian   dari", a, "dan", b, "adalah", pembagian.bagi(a, b))
