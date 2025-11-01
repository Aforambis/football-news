import sys

NAMA = "Rusydan"
NPM = "2406421081"


def determinant_cofactor(matrix, row=0):
    """
    Menghitung determinan matriks secara rekursif menggunakan ekspansi kofaktor pada baris tertentu.
    """
    n = len(matrix)

    if n == 1:
        return matrix[0][0]

    if n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    det = 0

    for col in range(n):
        # Membuat submatriks (minor) dengan menghapus baris `row` dan kolom `col`
        sub_matrix = []
        for i in range(n):
            if i == row:
                continue
            new_row = []
            for j in range(n):
                if j == col:
                    continue
                new_row.append(matrix[i][j])
            sub_matrix.append(new_row)
        
        # Menghitung kofaktor dan menambahkannya ke determinan total
        sign = (-1) ** (row + col)
        det += sign * matrix[row][col] * determinant_cofactor(sub_matrix)

    return det


def generate_permutations(elements):
    """
    Menghasilkan semua permutasi dari daftar elemen.
    """
    if len(elements) == 0:
        return [[]]

    permutations = []

    for i in range(len(elements)):
        rest = elements[:i] + elements[i + 1:]
        for perm in generate_permutations(rest):
            permutations.append([elements[i]] + perm)

    return permutations


def count_inversions(perm):
    """
    Menghitung jumlah inversi dalam suatu permutasi.
    """
    inversions = 0
    n = len(perm)

    for i in range(n):
        for j in range(i + 1, n):
            if perm[i] > perm[j]:
                inversions += 1

    return inversions


def determinant_combinatorics(matrix):
    """
    Menghitung determinan matriks menggunakan metode permutasi (metode Leibniz).
    """
    n = len(matrix)
    det = 0

    indices = list(range(n))
    permutations = generate_permutations(indices)

    for perm in permutations:
        # Hitung tanda (sign) dari permutasi
        sign = (-1) ** count_inversions(perm)
        
        # Hitung produk elemen matriks sesuai permutasi
        term = 1
        for i in range(n):
            term *= matrix[i][perm[i]]
            
        det += sign * term

    return det


def cramer_rule(A, b, determinant_method):
    """
    Menyelesaikan Sistem Persamaan Linear (SPL) Ax = b menggunakan Aturan Cramer.
    """
    det_A = determinant_method(A)

    if det_A == 0:
        return None

    n = len(A)
    solutions = []

    for i in range(n):
        # Buat matriks A_i dengan mengganti kolom ke-i dengan vektor b
        A_i = [row[:] for row in A] # Salin matriks A
        for j in range(n):
            A_i[j][i] = b[j]
            
        # Hitung determinan A_i dan cari solusi x_i
        det_Ai = determinant_method(A_i)
        solutions.append(det_Ai / det_A)

    return solutions


def invers_matrix(matrix):
    """
    Menghitung invers dari matriks persegi menggunakan adjoin matriks.
    """
    det_A = determinant_cofactor(matrix)

    if det_A == 0:
        return None

    n = len(matrix)
    
    # 1. Buat matriks kofaktor
    cofactor_matrix = []
    for r in range(n):
        cofactor_row = []
        for c in range(n):
            # Buat submatriks (minor)
            sub_matrix = []
            for i in range(n):
                if i == r:
                    continue
                new_row = []
                for j in range(n):
                    if j == c:
                        continue
                    new_row.append(matrix[i][j])
                sub_matrix.append(new_row)
            
            # Hitung kofaktor
            sign = (-1) ** (r + c)
            cofactor_row.append(sign * determinant_cofactor(sub_matrix))
        cofactor_matrix.append(cofactor_row)

    # 2. Transpos matriks kofaktor untuk mendapatkan adjoin
    adjoint_matrix = []
    for c in range(n):
        adjoint_row = []
        for r in range(n):
            adjoint_row.append(cofactor_matrix[r][c])
        adjoint_matrix.append(adjoint_row)
        
    # 3. Hitung invers: (1/detA) * adj(A)
    inverse_matrix = []
    for r in range(n):
        inverse_row = []
        for c in range(n):
            inverse_row.append(adjoint_matrix[r][c] / det_A)
        inverse_matrix.append(inverse_row)
        
    return inverse_matrix


def multiply_matrix_vector(matrix, vector):
    """
    Mengalikan matriks persegi dengan vektor.
    """
    n = len(matrix)
    result = [0] * n
    
    for i in range(n):
        for j in range(n):
            result[i] += matrix[i][j] * vector[j]

    return result


while True:
    print("\n=== Sistem Persamaan Linear ===")
    try:
        n = int(input("Masukkan ordo matriks persegi (n): "))
        if n <= 0:
            print("Ordo harus bilangan bulat positif.")
            continue

        A = []
        for i in range(n):
            row = list(map(float, input(f"Masukkan baris {i + 1} dari matriks koefisien A (dipisah spasi): ").split()))
            if len(row) != n:
                print(f"Error: Baris harus berisi {n} elemen.")
                raise ValueError
            A.append(row)

        b = list(map(float, input("Masukkan vektor hasil b (dipisah spasi): ").split()))
        if len(b) != n:
            print(f"Error: Vektor b harus berisi {n} elemen.")
            raise ValueError

    except ValueError:
        print("Input tidak valid. Pastikan semua masukan adalah angka dan sesuai format.")
        continue

    while True:
        print("\nPilih metode penyelesaian:")
        print("1. Menggunakan Determinan (Cramer)")
        print("2. Menggunakan Invers Matriks")
        print("3. Masukkan SPL baru")
        print("4. Keluar")
        metode = input("Pilihan: ")

        if metode == "1":
            print("\nPilih metode perhitungan determinan:")
            print("1. Metode Kofaktor (rekursif)")
            print("2. Metode Kombinatorik (permutasi)")
            metode_det = input("Pilihan: ")

            solutions = None
            if metode_det == "1":
                solutions = cramer_rule(A, b, determinant_cofactor)
            elif metode_det == "2":
                solutions = cramer_rule(A, b, determinant_combinatorics)
            else:
                print("Pilihan tidak valid.")
                continue

            if solutions is None:
                print("Sistem tidak memiliki solusi unik karena determinan = 0.")
            else:
                print("\nHasil solusi SPL menggunakan Aturan Cramer:")
                for i, sol in enumerate(solutions):
                    print(f"  x{i + 1} = {sol:.2f}")

        elif metode == "2":
            A_inv = invers_matrix(A)
            if A_inv is None:
                print("Sistem tidak memiliki solusi unik karena determinan = 0.")
            else:
                solutions = multiply_matrix_vector(A_inv, b)
                print("\nHasil solusi SPL menggunakan Invers Matriks:")
                for i, sol in enumerate(solutions):
                    print(f"  x{i + 1} = {sol:.2f}")

        elif metode == "3":
            break

        elif metode == "4":
            print("Program selesai.")
            sys.exit()

        else:
            print("Pilihan tidak valid.")