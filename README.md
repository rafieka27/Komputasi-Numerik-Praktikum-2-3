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

### 2.Mengumpulkan dan Memvalidasi Data (input_data & _check_equidistant)
```py
    def input_data(self):
        # ... (kode pengumpulan input dengan try-except) ...
        
        if not self._check_equidistant():
            print("\n[PERINGATAN] Jarak antar titik X tidak sama (ekuivalen).")
            print("Metode Newton-Gregory idealnya digunakan pada data dengan interval X yang konstan.")
            self.h = (self.x_data[-1] - self.x_data[0]) / (self.n - 1)
        else:
            self.h = self.x_data[1] - self.x_data[0]

        self._build_difference_table()

    def _check_equidistant(self):
        if self.n < 2: return False
        expected_h = self.x_data[1] - self.x_data[0]
        for i in range(1, self.n - 1):
            if not math.isclose(self.x_data[i+1] - self.x_data[i], expected_h, rel_tol=1e-5):
                return False
        return True
```
*Fungsi ini menangani interaksi dengan pengguna untuk menerima sekumpulan titik (X, Y). Sistem juga dilengkapi dengan fungsi validasi _check_equidistant untuk memastikan bahwa jarak antar titik X bernilai konstan. Jika input jaraknya berantakan, program akan memberikan peringatan namun tetap mencari nilai rata-rata h sebagai fail-safe agar program tidak crash.*

### 3.Membangun Tabel Selisih Dasar (_build_difference_table)
```py    
def _build_difference_table(self):
        self.diff_table = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        for i in range(self.n):
            self.diff_table[i][0] = self.y_data[i]
            
        for j in range(1, self.n):
            for i in range(self.n - j):
                self.diff_table[i][j] = self.diff_table[i + 1][j - 1] - self.diff_table[i][j - 1]
```
*Karena metode Newton-Gregory membutuhkan tabel diferensiasi, fungsi ini membangun matriks 2D berukuran $N \times N$. Program menggunakan perulangan bersarang (nested loop) untuk menghitung selisih dari data Y. Nilai pada sel tertentu didapatkan dengan mengurangkan sel di bawahnya dengan sel di posisinya pada kolom sebelumnya.*

### 4.Sistem Router Otomatis (interpolate)
```py
def interpolate(self, target_x):
        mid_point = (self.x_data[0] + self.x_data[-1]) / 2
        
        if target_x <= mid_point:
            method_used = "Newton-Gregory FORWARD"
            result = self._forward_interpolation(target_x)
        else:
            method_used = "Newton-Gregory BACKWARD"
            result = self._backward_interpolation(target_x)
            
        return result, method_used
```
*Fungsi ini bertindak sebagai penentu rute algoritma yang cerdas. Dengan menghitung nilai tengah (mid-point) dari rentang data masukan, program secara otomatis memutuskan: gunakan interpolasi maju (Forward) jika nilai target berada di paruh awal data, atau interpolasi mundur (Backward) jika berada di paruh akhir, guna menekan persentase galat.*

### 5.Algoritma Kalkulasi Newton-Gregory Forward & Backward
```Py
def _forward_interpolation(self, target_x):
        s = (target_x - self.x_data[0]) / self.h
        result = self.diff_table[0][0]
        
        for i in range(1, self.n):
            s_term = self._calculate_s_term_forward(s, i)
            result += (s_term * self.diff_table[0][i]) / math.factorial(i)
            
        return result

    def _backward_interpolation(self, target_x):
        s = (target_x - self.x_data[-1]) / self.h
        result = self.diff_table[self.n - 1][0]
        
        for i in range(1, self.n):
            s_term = self._calculate_s_term_backward(s, i)
            result += (s_term * self.diff_table[self.n - 1 - i][i]) / math.factorial(i)
            
        return result
```
*Di sinilah rumus polinomial inti dieksekusi. Masing-masing fungsi menghitung parameter jarak s sesuai rutenya. Selanjutnya, perulangan dilakukan untuk mengakumulasikan nilai dari setiap orde suku, di mana faktor berantai s dikalikan dengan elemen baris paling atas (untuk Forward) atau elemen diagonal paling bawah (untuk Backward) dari matriks tabel selisih, lalu dibagi dengan faktorial.*

### 6.Antarmuka Utama Program (main)
```Py
def main():
    print("==================================================")
    print(" PROGRAM INTERPOLASI NEWTON-GREGORY (AUTO-SELECT) ")
    print("==================================================")
    
    interpolator = NewtonGregoryInterpolator()
    interpolator.input_data()
    interpolator.print_difference_table()
    
    while True:
        # ... (blok try-except penerimaan target X) ...
        
        if target_x_str.lower() == 'q':
            break
            
        result, method = interpolator.interpolate(target_x)
        print(f"Nilai Fungsi f({target_x}) = {result:.6f}")

if __name__ == "__main__":
    main()
```
*Fungsi main bertindak sebagai jembatan interaksi (CLI) yang merangkai objek dan pemanggilan metodanya. Program sengaja dibungkus dalam perulangan tak terbatas (while True) supaya pengguna bisa terus mencari berbagai nilai X berulang kali tanpa perlu memasukkan ulang data set awal, hingga pengguna memutuskannya dengan mengetik 'q'.*


