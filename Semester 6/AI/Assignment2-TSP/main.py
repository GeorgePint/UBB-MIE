import math
import random
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# ==========================================
# 1. DATASET: berlin52
# ==========================================
# Standard coordinates for the berlin52 TSP instance
BERLIN52 = [
    (565.0, 575.0), (25.0, 185.0), (345.0, 750.0), (945.0, 685.0), (845.0, 655.0),
    (880.0, 660.0), (25.0, 230.0), (525.0, 1000.0), (580.0, 1175.0), (650.0, 1130.0),
    (1605.0, 620.0), (1220.0, 580.0), (1465.0, 200.0), (1530.0, 5.0), (845.0, 680.0),
    (725.0, 370.0), (145.0, 665.0), (415.0, 635.0), (510.0, 875.0), (560.0, 365.0),
    (300.0, 465.0), (520.0, 585.0), (480.0, 415.0), (835.0, 625.0), (975.0, 580.0),
    (1215.0, 245.0), (1320.0, 315.0), (1250.0, 400.0), (660.0, 180.0), (410.0, 250.0),
    (420.0, 555.0), (575.0, 665.0), (1150.0, 1160.0), (700.0, 580.0), (685.0, 595.0),
    (685.0, 610.0), (770.0, 610.0), (795.0, 645.0), (720.0, 635.0), (760.0, 650.0),
    (475.0, 960.0), (95.0, 260.0), (875.0, 920.0), (700.0, 500.0), (555.0, 815.0),
    (830.0, 485.0), (1170.0, 65.0), (830.0, 610.0), (605.0, 625.0), (595.0, 360.0),
    (1340.0, 725.0), (1740.0, 245.0)
]
N_CITIES = len(BERLIN52)


# Helper: Calculate distance matrix
def get_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


DIST_MATRIX = [[get_distance(BERLIN52[i], BERLIN52[j]) for j in range(N_CITIES)] for i in range(N_CITIES)]


def calculate_total_distance(route):
    dist = 0
    for i in range(N_CITIES):
        dist += DIST_MATRIX[route[i]][route[(i + 1) % N_CITIES]]
    return dist


def get_random_route():
    route = list(range(N_CITIES))
    random.shuffle(route)
    return route


def two_opt_swap(route, i, j):
    new_route = route[:i] + route[i:j + 1][::-1] + route[j + 1:]
    return new_route


# ==========================================
# 2. SIMULATED ANNEALING
# ==========================================
def simulated_annealing(initial_temp=10000, cooling_rate=0.995, min_temp=1e-3):
    current_route = get_random_route()
    current_dist = calculate_total_distance(current_route)

    best_route = current_route
    best_dist = current_dist

    temp = initial_temp
    history = []

    while temp > min_temp:
        # Generate neighbor via 2-opt
        i, j = sorted(random.sample(range(N_CITIES), 2))
        neighbor = two_opt_swap(current_route, i, j)
        neighbor_dist = calculate_total_distance(neighbor)

        # Acceptance probability
        if neighbor_dist < current_dist:
            current_route, current_dist = neighbor, neighbor_dist
            if current_dist < best_dist:
                best_route, best_dist = current_route, current_dist
        else:
            prob = math.exp((current_dist - neighbor_dist) / temp)
            if random.random() < prob:
                current_route, current_dist = neighbor, neighbor_dist

        temp *= cooling_rate
        history.append(best_dist)

    return best_dist, best_route, history


# ==========================================
# 3. TABU SEARCH
# ==========================================
def tabu_search(iterations=1000, tabu_tenure=20, neighborhood_size=50):
    current_route = get_random_route()
    current_dist = calculate_total_distance(current_route)

    best_route = current_route
    best_dist = current_dist

    tabu_list = {}
    history = []

    for it in range(iterations):
        best_neighbor = None
        best_neighbor_dist = float('inf')
        best_move = None

        # Explore neighborhood
        for _ in range(neighborhood_size):
            i, j = sorted(random.sample(range(N_CITIES), 2))
            neighbor = two_opt_swap(current_route, i, j)
            neighbor_dist = calculate_total_distance(neighbor)

            # Check if move is Tabu (Aspiration criterion: accept if it's the global best)
            is_tabu = (i, j) in tabu_list and tabu_list[(i, j)] >= it
            if not is_tabu or neighbor_dist < best_dist:
                if neighbor_dist < best_neighbor_dist:
                    best_neighbor_dist = neighbor_dist
                    best_neighbor = neighbor
                    best_move = (i, j)

        if best_neighbor:
            current_route = best_neighbor
            current_dist = best_neighbor_dist
            tabu_list[best_move] = it + tabu_tenure  # Update Tabu List

            if current_dist < best_dist:
                best_route = current_route
                best_dist = current_dist

        history.append(best_dist)

    return best_dist, best_route, history


# ==========================================
# 4. GENETIC ALGORITHM
# ==========================================
def genetic_algorithm(pop_size=100, generations=500, mutation_rate=0.1):
    population = [get_random_route() for _ in range(pop_size)]
    best_dist = float('inf')
    best_route = None
    history = []

    for _ in range(generations):
        # Evaluate fitness (inverse distance)
        fitnesses = [1.0 / calculate_total_distance(ind) for ind in population]

        # Track best
        current_best_idx = fitnesses.index(max(fitnesses))
        current_best_dist = 1.0 / fitnesses[current_best_idx]
        if current_best_dist < best_dist:
            best_dist = current_best_dist
            best_route = population[current_best_idx]

        history.append(best_dist)

        # Selection (Tournament)
        new_population = []
        for _ in range(pop_size):
            t1, t2 = random.sample(range(pop_size), 2)
            parent1 = population[t1] if fitnesses[t1] > fitnesses[t2] else population[t2]
            t1, t2 = random.sample(range(pop_size), 2)
            parent2 = population[t1] if fitnesses[t1] > fitnesses[t2] else population[t2]

            # Crossover (Order Crossover - OX1)
            start, end = sorted(random.sample(range(N_CITIES), 2))
            child = [-1] * N_CITIES
            child[start:end] = parent1[start:end]
            p2_idx = end
            for i in range(N_CITIES):
                if parent2[(end + i) % N_CITIES] not in child:
                    child[p2_idx % N_CITIES] = parent2[(end + i) % N_CITIES]
                    p2_idx += 1

            # Mutation (Swap)
            if random.random() < mutation_rate:
                i, j = random.sample(range(N_CITIES), 2)
                child[i], child[j] = child[j], child[i]

            new_population.append(child)
        population = new_population

    return best_dist, best_route, history


# ==========================================
# 5. BENCHMARKING & VISUALIZATION
# ==========================================
if __name__ == "__main__":
    print("Benchmarking Algorithms on berlin52...")

    start = time.time()
    sa_dist, sa_route, sa_hist = simulated_annealing()
    print(f"Simulated Annealing: {sa_dist:.2f} (Time: {time.time() - start:.2f}s)")

    start = time.time()
    ts_dist, ts_route, ts_hist = tabu_search()
    print(f"Tabu Search:         {ts_dist:.2f} (Time: {time.time() - start:.2f}s)")

    start = time.time()
    ga_dist, ga_route, ga_hist = genetic_algorithm()
    print(f"Genetic Algorithm:   {ga_dist:.2f} (Time: {time.time() - start:.2f}s)")

    # Plot convergence
    plt.figure(figsize=(10, 6))
    plt.plot(sa_hist, label='Simulated Annealing')
    plt.plot(ts_hist, label='Tabu Search')
    plt.plot(ga_hist, label='Genetic Algorithm')
    plt.title('Algorithm Convergence Comparison (berlin52)')
    plt.xlabel('Iterations / Generations')
    plt.ylabel('Best Total Distance')
    plt.legend()
    plt.grid()
    plt.show()