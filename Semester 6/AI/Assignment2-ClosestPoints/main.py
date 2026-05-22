import matplotlib.pyplot as plt
import math
import random
import time
import matplotlib
matplotlib.use('TkAgg')


# Representation of a Point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


# Euclidean distance between two points
def dist(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


# ==========================================
# 1. BRUTE FORCE APPROACH
# ==========================================
def brute_force(points):
    min_d = float('inf')
    n = len(points)
    pair = (None, None)
    for i in range(n):
        for j in range(i + 1, n):
            d = dist(points[i], points[j])
            if d < min_d:
                min_d = d
                pair = (points[i], points[j])
    return min_d, pair


# ==========================================
# 2. DIVIDE AND CONQUER APPROACH
# ==========================================
def closest_pair_dc(points):
    # Sort points according to X coordinate
    points_x = sorted(points, key=lambda p: p.x)
    # Sort points according to Y coordinate
    points_y = sorted(points, key=lambda p: p.y)

    return _closest_pair_rec(points_x, points_y)


def _closest_pair_rec(points_x, points_y):
    n = len(points_x)

    # Base case: Use brute force if points are 3 or fewer
    if n <= 3:
        return brute_force(points_x)

    # Find the middle point
    mid = n // 2
    mid_point = points_x[mid]

    # Divide points in Y sorted array into left and right halves
    # maintaining the sorted order by Y coordinate
    points_y_left = []
    points_y_right = []
    for p in points_y:
        if p.x <= mid_point.x and len(points_y_left) < mid:
            points_y_left.append(p)
        else:
            points_y_right.append(p)

    # Recursive calls for left and right halves
    dl, pair_l = _closest_pair_rec(points_x[:mid], points_y_left)
    dr, pair_r = _closest_pair_rec(points_x[mid:], points_y_right)

    # Find the smaller of two distances
    if dl < dr:
        d = dl
        min_pair = pair_l
    else:
        d = dr
        min_pair = pair_r

    # Geometrical Observation: Find points close to the dividing line
    strip = [p for p in points_y if abs(p.x - mid_point.x) < d]

    # Check the strip for closer pairs
    strip_d, strip_pair = _closest_strip(strip, d)

    if strip_d < d:
        return strip_d, strip_pair
    return d, min_pair


def _closest_strip(strip, d):
    min_d = d
    pair = (None, None)
    size = len(strip)

    # This inner loop runs at most 7 times for each point due to geometric constraints
    for i in range(size):
        for j in range(i + 1, size):
            if (strip[j].y - strip[i].y) >= min_d:
                break
            distance = dist(strip[i], strip[j])
            if distance < min_d:
                min_d = distance
                pair = (strip[i], strip[j])

    return min_d, pair


# ==========================================
# TIMING AND PLOTTING
# ==========================================
def run_benchmarks():
    sizes = [10, 50, 100, 200, 500, 800, 1000, 1500, 2000]
    bf_times = []
    dc_times = []

    for size in sizes:
        # Generate random coordinates between -100,000 and 100,000 (matching Infoarena limits)
        points = [Point(random.uniform(-100000, 100000), random.uniform(-100000, 100000)) for _ in range(size)]

        # Benchmark Brute Force
        start = time.time()
        brute_force(points)
        bf_times.append(time.time() - start)

        # Benchmark Divide and Conquer
        start = time.time()
        closest_pair_dc(points)
        dc_times.append(time.time() - start)

    # Plotting the results
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, bf_times, label='Brute Force $O(N^2)$', color='red', marker='o')
    plt.plot(sizes, dc_times, label='Divide & Conquer $O(N \log N)$', color='blue', marker='s')
    plt.xlabel('Number of Points ($N$)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Closest Pair of Points: Brute Force vs Divide & Conquer')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Example validation run
    test_points = [Point(2, 3), Point(12, 30), Point(40, 50), Point(5, 1), Point(12, 10), Point(3, 4)]
    min_distance, pairs = closest_pair_dc(test_points)
    print(f"Validation Run Minimum Distance: {min_distance:.4f} between {pairs[0]} and {pairs[1]}")

    print("\nRunning performance benchmarks and generating plot...")
    run_benchmarks()