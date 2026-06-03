import sympy as sp


def integrasi_romberg(func_str, a, b, steps):
    x = sp.symbols('x')
    try:
        expr = sp.sympify(func_str)
        f = sp.lambdify(x, expr, 'numpy')
    except Exception as e:
        return f"Error format fungsi: {e}"

    R = [[0.0] * (steps + 1) for _ in range(steps + 1)]
    h = b-a
    try:
        R[0][0] = 0.5 * h * (f(a) + f(b))
    except Exception as e:
        return f"Error saat menghitung fungsi pada batas a atau b: {e}"
    for i in range(1, steps + 1):
        h /= 2
        try:
            sum_new_points = sum(f(a + (2 * k - 1) * h) for k in range(1, 2 ** (i - 1) + 1))
        except Exception as e:
            return f"Error perhitungan nilai fungsi di dalam interval: {e}"

        R[i][0] = 0.5 * R[i - 1][0] + h * sum_new_points
        for j in range(1, i + 1):
            R[i][j] = R[i][j - 1] + (R[i][j - 1] - R[i - 1][j - 1]) / (4 ** j - 1)
    return R

def main():
    func_input = input("Masukkan f(x): ")
    try:
        a = float(input("Masukkan a   : "))
        b = float(input("Masukkan b   : "))
    except ValueError:
        print("\n[Error] Batas interval harus berupa angka!")
        return
    if a >= b:
        print("\n[Error] Interval tidak valid! (a) < (b).")
        return
    try:
        iterations = int(input("Masukkan jumlah iterasi: "))
        if iterations < 1:
            print("\n[Error] Jumlah iterasi harus minimal 1!")
            return
    except ValueError:
        print("\n[Error] Jumlah iterasi harus berupa bilangan bulat!")
        return

    result_matrix = integrasi_romberg(func_input, a, b, iterations)

    if isinstance(result_matrix, str):
        print(f"\n{result_matrix}")
    else:
        for i in range(len(result_matrix)):
            row_str = "  ".join(f"{val:.8f}" for j, val in enumerate(result_matrix[i]) if j <= i)
            print(f"R[{i}]: {row_str}")
        print(f"Hasil Estimasi: {result_matrix[iterations][iterations]:.10f}")

if __name__ == "__main__":
    main()