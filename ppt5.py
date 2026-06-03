import math

class NewtonGregoryInterpolator:
    def __init__(self):
        self.x_data = []
        self.y_data = []
        self.n = 0
        self.diff_table = []
        self.h = 0

    def input_data(self):
        print("\n--- Input Data Pasangan (X, Y) ---")
        while True:
            try:
                self.n = int(input("Masukkan jumlah titik data (minimal 2): "))
                if self.n >= 2:
                    break
                print("Jumlah data minimal adalah 2. Silakan ulangi.")
            except ValueError:
                print("Input tidak valid. Masukkan angka bulat.")

        self.x_data = []
        self.y_data = []
        
        print("\nMasukkan nilai X dan Y secara berurutan:")
        for i in range(self.n):
            while True:
                try:
                    x_val = float(input(f"X[{i}]: "))
                    y_val = float(input(f"Y[{i}]: "))
                    self.x_data.append(x_val)
                    self.y_data.append(y_val)
                    break
                except ValueError:
                    print("Input harus berupa angka. Silakan ulangi untuk titik ini.")

        if not self._check_equidistant():
            print("\n[PERINGATAN] Jarak antar titik X tidak sama (ekuivalen).")
            print("Metode Newton-Gregory idealnya digunakan pada data dengan interval X yang konstan.")
            # Program tetap dilanjutkan, menggunakan rata-rata h sebagai fallback
            self.h = (self.x_data[-1] - self.x_data[0]) / (self.n - 1)
        else:
            self.h = self.x_data[1] - self.x_data[0]

        self._build_difference_table()

    def _check_equidistant(self):
        """Memeriksa apakah jarak antar titik x konstan."""
        if self.n < 2: return False
        expected_h = self.x_data[1] - self.x_data[0]
        for i in range(1, self.n - 1):
            if not math.isclose(self.x_data[i+1] - self.x_data[i], expected_h, rel_tol=1e-5):
                return False
        return True

    def _build_difference_table(self):
        """Membangun tabel selisih (difference table)."""
        self.diff_table = [[0.0 for _ in range(self.n)] for __ in range(self.n)]
        
        # Kolom pertama adalah nilai Y
        for i in range(self.n):
            self.diff_table[i][0] = self.y_data[i]
            
        # Menghitung selisih maju
        for j in range(1, self.n):
            for i in range(self.n - j):
                self.diff_table[i][j] = self.diff_table[i + 1][j - 1] - self.diff_table[i][j - 1]

    def print_difference_table(self):
        """Menampilkan tabel selisih ke layar dengan rapi."""
        print("\n--- Tabel Selisih (Difference Table) ---")
        header = "X\t\tY"
        for i in range(1, self.n):
            header += f"\t\tΔ^{i}"
        print(header)
        print("-" * (16 + 16 * self.n))
        
        for i in range(self.n):
            row_str = f"{self.x_data[i]:.4f}\t{self.diff_table[i][0]:.4f}"
            for j in range(1, self.n - i):
                row_str += f"\t{self.diff_table[i][j]:.4f}"
            print(row_str)
        print("-" * (16 + 16 * self.n))

    def _calculate_s_term_forward(self, s, i):
        term = 1
        for j in range(i):
            term *= (s - j)
        return term

    def _calculate_s_term_backward(self, s, i):
        term = 1
        for j in range(i):
            term *= (s + j)
        return term

    def interpolate(self, target_x):
        # Fitur Fleksibilitas: Penentuan Otomatis Forward atau Backward
        mid_point = (self.x_data[0] + self.x_data[-1]) / 2
        
        if target_x <= mid_point:
            method_used = "Newton-Gregory FORWARD"
            result = self._forward_interpolation(target_x)
        else:
            method_used = "Newton-Gregory BACKWARD"
            result = self._backward_interpolation(target_x)
            
        return result, method_used

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

def main():
    print("==================================================")
    print(" PROGRAM INTERPOLASI NEWTON-GREGORY (AUTO-SELECT) ")
    print("==================================================")
    
    interpolator = NewtonGregoryInterpolator()
    interpolator.input_data()
    interpolator.print_difference_table()
    
    while True:
        print("\n--- Hitung Nilai Fungsi ---")
        try:
            target_x_str = input("Masukkan nilai X yang ingin dicari (atau ketik 'q' untuk keluar): ")
            if target_x_str.lower() == 'q':
                print("Program selesai. Terima kasih!")
                break
                
            target_x = float(target_x_str)
            result, method = interpolator.interpolate(target_x)
            
            print(f"\n[HASIL]")
            print(f"Nilai X yang dicari : {target_x}")
            print(f"Metode Terpilih     : {method} (Dipilih otomatis berdasarkan posisi X)")
            print(f"Nilai Fungsi f({target_x}) = {result:.6f}")
            
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")

if __name__ == "__main__":
    main()