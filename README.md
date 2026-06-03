# Komputasi-Numerik-Praktikum-2-3

## PPT-5

## Soal
<img width="882" height="666" alt="image" src="https://github.com/user-attachments/assets/76d83437-97c6-4c7f-8d6a-98f26dac068f" />

## Langkah-Langkah potongan kode

### 1.Mengimpor Library & Inisialisasi Kelas Utama

```py
import math

class NewtonGregoryInterpolator:
    def __init__(self):
        self.x_data = []
        self.y_data = []
        self.n = 0
        self.diff_table = []
        self.h = 0
```
*Langkah pertama adalah mengimpor library matematika bawaan Python dan mendefinisikan kelas NewtonGregoryInterpolator. Fungsi __init__ bertugas menyiapkan wadah memori dasar saat objek dibuat, seperti list kosong untuk titik koordinat (X, Y), variabel jumlah data (n), jarak interval (h), dan matriks tabel selisih.*



