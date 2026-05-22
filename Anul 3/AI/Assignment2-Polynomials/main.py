import cmath
import time
import random
import matplotlib

matplotlib.use('TkAgg')  # Prevents PyCharm SciView backend crashes
import matplotlib.pyplot as plt


# ==========================================
# 1. BRUTE FORCE POLYNOMIAL MULTIPLICATION
# ==========================================
def brute_force_multiply(A, B):
    """
    Multiplies two polynomials represented as lists of coefficients.
    A = [a0, a1, ..., an] represents a0 + a1*x + ... + an*x^n
    """
    n = len(A)
    m = len(B)
    # Resulting polynomial will have a degree of (n - 1) + (m - 1)
    result = [0] * (n + m - 1)

    for i in range(n):
        for j in range(m):
            result[i + j] += A[i] * B[j]

    return result


# ==========================================
# 2. FFT (FAST FOURIER TRANSFORM) APPROACH
# ==========================================
def fft(a, invert=False):
    """
    Recursive Cooley-Tukey FFT algorithm.
    a: list of coefficients (length must be a power of 2)
    invert: True for Inverse FFT, False for Forward FFT
    """
    n = len(a)
    if n == 1:
        return a

    # Divide step: Split into even and odd indices
    a_even = a[0::2]
    a_odd = a[1::2]

    # Conquer step: Recursive calls
    y_even = fft(a_even, invert)
    y_odd = fft(a_odd, invert)

    # Combine step using primitive roots of unity
    y = [0] * n
    angle = 2 * cmath.pi / n * (-1 if invert else 1)
    w = 1
    wn = cmath.exp(complex(0, angle))

    for i in range(n // 2):
        # Geometrical butterfly operations
        match_transform = w * y_odd[i]
        y[i] = y_even[i] + match_transform
        y[i + n // 2] = y_even[i] - match_transform

        if invert:
            y[i] /= 2
            y[i + n // 2] /= 2

        w *= wn

    return y


def fft_multiply(A, B):
    """
    Multiplies two polynomials using FFT by evaluating, 
    multiplying pointwise, and interpolating back.
    """
    # Find the next power of 2 size that can hold the result polynomial
    target_size = 1
    while target_size < len(A) + len(B) - 1:
        target_size *= 2

    # Pad polynomials with zeros up to the target power of 2
    A_padded = A + [0] * (target_size - len(A))
    B_padded = B + [0] * (target_size - len(B))

    # Step 1: Evaluate polynomials at roots of unity (Coefficient -> Value representation)
    A_val = fft(A_padded, invert=False)
    B_val = fft(B_padded, invert=False)

    # Step 2: Pointwise multiplication in Value space
    C_val = [A_val[i] * B_val[i] for i in range(target_size)]

    # Step 3: Interpolate back to coefficients (Value -> Coefficient representation)
    C_padded = fft(C_val, invert=True)

    # Round real parts to integers/floats and trim trailing zeroes to match expected size
    result_size = len(A) + len(B) - 1
    return [round(c.real, 5) for c in C_padded[:result_size]]


# ==========================================
# TIMING AND PLOTTING
# ==========================================
def run_benchmarks():
    # Use smaller sizes for visualization so Brute Force doesn't lock up execution
    degrees = [4, 16, 64, 128, 256, 512, 1024, 2048]
    bf_times = []
    fft_times = []

    for d in degrees:
        # Generate random polynomial coefficients
        A = [random.randint(-10, 10) for _ in range(d)]
        B = [random.randint(-10, 10) for _ in range(d)]

        # Benchmark Brute Force
        start = time.time()
        brute_force_multiply(A, B)
        bf_times.append(time.time() - start)

        # Benchmark FFT
        start = time.time()
        fft_multiply(A, B)
        fft_times.append(time.time() - start)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(degrees, bf_times, label=r'Brute Force $O(n^2)$', color='crimson', marker='o')
    plt.plot(degrees, fft_times, label=r'FFT Multiplication $O(n \log n)$', color='teal', marker='s')
    plt.xlabel('Polynomial Degree ($n$)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Polynomial Multiplication Complexity Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Validation test
    poly1 = [1, 2, 3]  # 1 + 2x + 3x^2
    poly2 = [4, 5, 6]  # 4 + 5x + 6x^2
    print("Brute Force Result:", brute_force_multiply(poly1, poly2))
    print("FFT Result:        ", [int(x) for x in fft_multiply(poly1, poly2)])

    print("\nRunning performance benchmarks...")
    run_benchmarks()