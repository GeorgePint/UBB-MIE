import heapq


def dijkstra(graph, start):
    # Initialize distances with infinity and the start node with 0
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0

    # Priority queue stores tuples of (distance, node)
    priority_queue = [(0, start)]

    # Dictionary to keep track of the shortest path tree
    previous_nodes = {node: None for node in graph}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        # If we find a longer path to a node we've already processed, skip it
        if current_distance > distances[current_node]:
            continue

        # Relax all adjacent edges
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            # If a shorter path is found, update the distance and queue
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, previous_nodes


# Example Usage:
graph = {
    'A': {'B': 4, 'C': 2},
    'B': {'C': 5, 'D': 10},
    'C': {'E': 3},
    'D': {'F': 11},
    'E': {'D': 4},
    'F': {}
}

distances, paths = dijkstra(graph, 'A')
print("Shortest distances from A:", distances)
print("")


def needleman_wunsch(seq1, seq2, match_score=1, mismatch_score=-1, gap_penalty=-1):
    n = len(seq1)
    m = len(seq2)

    # 1. Initialize the DP table with zeros
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    # 2. Base cases: Fill the first row and column with gap penalties
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + gap_penalty
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + gap_penalty

    # 3. Fill the DP matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Calculate scores for match/mismatch, deletion, and insertion
            is_match = seq1[i - 1] == seq2[j - 1]
            match = dp[i - 1][j - 1] + (match_score if is_match else mismatch_score)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty

            # The cell takes the maximum of the three possibilities
            dp[i][j] = max(match, delete, insert)

    # 4. Traceback to build the alignment
    align1 = ""
    align2 = ""
    i, j = n, m

    while i > 0 or j > 0:
        current_score = dp[i][j]

        # Check if the current score came from a diagonal step (match/mismatch)
        if i > 0 and j > 0:
            is_match = seq1[i - 1] == seq2[j - 1]
            diag_score = dp[i - 1][j - 1] + (match_score if is_match else mismatch_score)
            if current_score == diag_score:
                align1 += seq1[i - 1]
                align2 += seq2[j - 1]
                i -= 1
                j -= 1
                continue

        # Check if it came from a top step (gap in seq2)
        if i > 0 and current_score == dp[i - 1][j] + gap_penalty:
            align1 += seq1[i - 1]
            align2 += "-"
            i -= 1
            continue

        # If not diagonal or top, it must have come from a left step (gap in seq1)
        align1 += "-"
        align2 += seq2[j - 1]
        j -= 1

    # The traceback builds the strings backwards, so we reverse them
    return align1[::-1], align2[::-1], dp[n][m]


# Example Usage:
sequence_a = "GATTACA"
sequence_b = "GCATGCU"

aligned_a, aligned_b, final_score = needleman_wunsch(sequence_a, sequence_b)
print(f"Alignment Score: {final_score}")
print(f"Seq 1: {aligned_a}")
print(f"Seq 2: {aligned_b}")