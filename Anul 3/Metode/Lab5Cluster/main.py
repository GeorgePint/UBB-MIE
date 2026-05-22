import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')


def load_from_file(filepath):
    entities = {}
    with open(filepath, 'r') as file:
        for line in file:
            if '->' not in line:
                continue

            # split the entity from the proprieties
            entity_part, props_part = line.split('->')
            entity = entity_part.strip()

            # split the proprieties by comma
            proprieties = {p.strip() for p in props_part.split(',')}
            entities[entity] = proprieties

    return entities


def calculate_distance_matrix(entities_dictionar):
    entity_names = list(entities_dictionar)
    n = len(entity_names)

    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            set1 = entities_dictionar[entity_names[i]]
            set2 = entities_dictionar[entity_names[j]]

            # calculate intersection and union
            intersection_size = len(set1.intersection(set2))
            union_size = len(set1.union(set2))

            # apply the formula
            if union_size == 0:
                distance = 1.0
            else:
                distance = 1.0 - (intersection_size / union_size)

            # Populate the matrix symmetrically
            dist_matrix[i][j] = distance
            dist_matrix[j][i] = distance
    return entity_names, dist_matrix


def perform_cluster_and_plot(entity_names, dist_matrix):
    # Convertim din 2d in 1d
    condensed_dist = squareform(dist_matrix)

    # perfrom hierarechal clustering
    Z = linkage(condensed_dist, method='average')

    n = len(entity_names)

    cluster_dict = {i: name for i, name in enumerate(entity_names)}

    print("Clustering trace:")
    for i, step in enumerate(Z):
        idx1, idx2, distance, count = step
        idx1, idx2 = int(idx1), int(idx2)

        # Get the names (or IDs) of the clusters being merged
        name1 = cluster_dict[idx1]
        name2 = cluster_dict[idx2]

        # The new cluster is assigned an ID of n + i
        new_cluster_id = n + i

        # We label the new cluster for future steps
        cluster_dict[new_cluster_id] = f"Cluster_{new_cluster_id}"

        print(f"Step {i + 1}:")
        print(f"  Merging : '{name1}' AND '{name2}'")
        print(f"  Distance: {distance:.4f}")
        print(f"  New ID  : {cluster_dict[new_cluster_id]} (Total entities: {int(count)})")
        print("-" * 30)
    print("\n")

    plt.figure(figsize=(10, 7))
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Entities")
    plt.ylabel("Distance")

    dendrogram(
        Z,
        labels=entity_names,
        leaf_rotation=90.,
        leaf_font_size=10,
    )

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # 1. Define the path to your data file
    # Make sure this matches the name of your text file!
    filepath = 'RelPropsLargerExample.txt'

    # 2. Load the data
    print(f"Loading data from {filepath}...")
    data = load_from_file(filepath)

    # 3. Calculate the distance matrix
    print("Calculating distances...")
    names, matrix = calculate_distance_matrix(data)

    # 4. Perform clustering and display the plot
    print("Starting clustering...")
    perform_cluster_and_plot(names, matrix)