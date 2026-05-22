import struct


def fast_inverse_square_root(number):
    """
    Computes 1/sqrt(number) using the Quake III algorithm.
    """
    if number < 0:
        raise ValueError("Cannot compute the square root of a negative number.")
    if number == 0:
        return float('inf')

    # Step 1: Get the bit representation of the 32-bit float
    # 'f' is for standard 32-bit float, 'i' is for 32-bit integer
    packed_float = struct.pack('f', number)
    i = struct.unpack('i', packed_float)[0]

    # Step 2: The magic bit-shift and subtraction
    # Bitshifting right by 1 divides the exponent by 2.
    # The magic number 0x5f3759df handles the IEEE 754 offset and scale.
    i = 0x5f3759df - (i >> 1)

    # Step 3: Reinterpret the bits back into a floating-point number
    packed_int = struct.pack('i', i)
    y = struct.unpack('f', packed_int)[0]

    # Step 4: One iteration of Newton's method to improve accuracy
    # f(y) = 1/y^2 - number = 0
    # y_{n+1} = y_n * (1.5 - (number/2) * y_n * y_n)
    x2 = number * 0.5
    y = y * (1.5 - (x2 * y * y))

    return y


# Example usage:
x = 0.15625
print(f"Standard 1/sqrt({x}): {1 / (x ** 0.5):.6f}")
print(f"Quake III 1/sqrt({x}): {fast_inverse_square_root(x):.6f}")


def newton_polynomial_root(P, dP, a, b, tol=1e-7, max_iter=1000):
    """
    Finds the root of a strictly increasing, convex polynomial P(x) in [a, b].
    P: Function representing the polynomial
    dP: Function representing the derivative of the polynomial
    """
    # Start at the right boundary. Because P is convex and increasing,
    # starting at 'b' guarantees monotonic convergence from the right.
    x_n = b

    for i in range(max_iter):
        fx = P(x_n)
        dfx = dP(x_n)

        if dfx == 0:
            raise ValueError("Derivative is zero. Newton's method fails.")

        x_next = x_n - fx / dfx

        # Check for convergence
        if abs(x_next - x_n) < tol:
            return x_next

        x_n = x_next

    raise Exception("Exceeded maximum iterations without convergence")


# Example: P(x) = x^3 + 2x - 5 on interval [1, 2]
# P'(x) = 3x^2 + 2 (Strictly positive, increasing)
# P''(x) = 6x (Strictly positive for x>0, convex)
P = lambda x: x ** 3 + 2 * x - 5
dP = lambda x: 3 * x ** 2 + 2

root = newton_polynomial_root(P, dP, 1, 2)
print(f"Root of the polynomial is approximately: {root:.7f}")


def nth_root_newton(x, n, tol=1e-7, max_iter=1000):
    """
    Finds the n-th root of a supraunitary real number x (x > 1).
    """
    if x <= 1:
        raise ValueError("x must be a supraunitary number (x > 1).")
    if n <= 0 or not isinstance(n, int):
        raise ValueError("n must be a positive integer.")
    if n == 1:
        return float(x)

    # Initial guess. Since x > 1, the root will be between 1 and x.
    # x is a safe upper-bound starting point.
    y_k = float(x)

    for i in range(max_iter):
        # Apply the simplified Newton's method formula for n-th roots
        y_next = ((n - 1) * y_k + x / (y_k ** (n - 1))) / n

        # Check for convergence
        if abs(y_next - y_k) < tol:
            return y_next

        y_k = y_next

    raise Exception("Exceeded maximum iterations without convergence")


# Example: 5th root of 3125 (which should be 5)
val = 3125
order = 5
result = nth_root_newton(val, order)
print(f"The {order}-th root of {val} is approximately: {result:.7f}")