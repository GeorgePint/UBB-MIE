import pandas as pd
import numpy as np
from math import log2
from sklearn.datasets import load_iris


# ==========================================
# PART 1: Categorical Decision Tree (ID3)
# ==========================================

def calculate_entropy(data, target_col):
    """Calculates the entropy of a dataset."""
    counts = data[target_col].value_counts()
    probabilities = counts / len(data)

    # Filter out any 0 probabilities to avoid the log2(0)
    probabilities = probabilities[probabilities > 0]

    entropy = -sum(probabilities * np.log2(probabilities))
    return entropy


def calculate_information_gain(data, feature, target_col):
    """Calculates Information Gain for a specific feature."""
    total_entropy = calculate_entropy(data, target_col)

    # Calculate weighted entropy of the feature
    values = data[feature].value_counts(normalize=True)
    weighted_entropy = 0
    for value, prob in values.items():
        subset = data[data[feature] == value]
        weighted_entropy += prob * calculate_entropy(subset, target_col)

    information_gain = total_entropy - weighted_entropy
    return information_gain


def build_tree(data, original_data, features, target_col, parent_node_class=None):
    """Recursively builds the decision tree using the Divide and Conquer strategy."""
    # Base Case 1: If all target values are the same, return that value
    if len(np.unique(data[target_col])) <= 1:
        return np.unique(data[target_col])[0]

    # Base Case 2: If dataset is empty, return the mode target feature value in the original dataset
    elif len(data) == 0:
        return np.unique(original_data[target_col])[
            np.argmax(np.unique(original_data[target_col], return_counts=True)[1])]

    # Base Case 3: If feature space is empty, return the mode target feature value of the current dataset
    elif len(features) == 0:
        return parent_node_class

    # Recursive Step: Divide and Conquer
    else:
        parent_node_class = np.unique(data[target_col])[np.argmax(np.unique(data[target_col], return_counts=True)[1])]

        # Find the feature with the highest information gain
        item_values = [calculate_information_gain(data, feature, target_col) for feature in features]
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]

        # Create the tree structure
        tree = {best_feature: {}}
        features = [i for i in features if i != best_feature]

        # Grow a branch under the root node for each possible value of the root node feature
        for value in np.unique(data[best_feature]):
            subset = data.where(data[best_feature] == value).dropna()
            subtree = build_tree(subset, original_data, features, target_col, parent_node_class)
            tree[best_feature][value] = subtree

        return tree


# --- PlayTennis Categorical Dataset ---
play_tennis_data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rainy', 'Rainy', 'Rainy', 'Overcast', 'Sunny', 'Sunny', 'Rainy', 'Sunny',
                'Overcast', 'Overcast', 'Rainy'],
    'Temperature': ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot',
                    'Mild'],
    'Humidity': ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal',
                 'High', 'Normal', 'High'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong',
             'Weak', 'Strong'],
    'Play': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
}
df_tennis = pd.DataFrame(play_tennis_data)

print("--- PART 1: Standard ID3 Decision Tree (Categorical) ---")
features = list(df_tennis.columns[:-1])
tree = build_tree(df_tennis, df_tennis, features, 'Play')
import pprint

pprint.pprint(tree)
print("\n")


# ==========================================
# PART 2: Fuzzy Decision Tree Implementation
# ==========================================

def fuzzify_continuous_series(series):
    """
    Converts continuous data into fuzzy categories (Low, Medium, High).
    In a true fuzzy system, values have 'degrees of membership' to multiple sets.
    For standard tree compatibility, we evaluate membership and pick the dominant fuzzy set.
    """
    min_val, max_val = series.min(), series.max()
    range_val = max_val - min_val

    # Define simple triangular fuzzy membership boundaries
    low_bound = min_val + (range_val * 0.33)
    high_bound = min_val + (range_val * 0.66)

    fuzzy_categories = []
    for val in series:
        # Calculating simple membership degrees (simplified for demonstration)
        # Degree of "Low"
        deg_low = 1.0 if val <= low_bound else (high_bound - val) / (
                    high_bound - low_bound) if val < high_bound else 0.0
        # Degree of "High"
        deg_high = 1.0 if val >= high_bound else (val - low_bound) / (
                    high_bound - low_bound) if val > low_bound else 0.0
        # Degree of "Medium" (1 - extreme degrees)
        deg_med = 1.0 - max(deg_low, deg_high) if (val > low_bound and val < high_bound) else 0.0

        # Determine the dominant fuzzy category for standard ID3 processing
        degrees = {'Fuzzy_Low': deg_low, 'Fuzzy_Medium': deg_med, 'Fuzzy_High': deg_high}
        dominant_set = max(degrees, key=degrees.get)
        fuzzy_categories.append(dominant_set)

    return fuzzy_categories


# --- Iris Dataset (Continuous Data) ---
print("--- PART 2: Fuzzy Decision Tree (Continuous Data) ---")
iris = load_iris()
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris['Species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

print("Original Continuous Data (First 3 rows):")
print(df_iris.head(3))
print("-" * 30)

# Fuzzify the continuous dataset
df_fuzzy_iris = df_iris.copy()
for col in iris.feature_names:
    df_fuzzy_iris[col] = fuzzify_continuous_series(df_iris[col])

print("Fuzzified Data (First 3 rows):")
print(df_fuzzy_iris.head(3))
print("-" * 30)

# Build the tree using the fuzzified continuous data using the same entropy/info gain logic
fuzzy_features = list(df_fuzzy_iris.columns[:-1])
fuzzy_tree = build_tree(df_fuzzy_iris, df_fuzzy_iris, fuzzy_features, 'Species')

print("Fuzzy Decision Tree Structure:")
pprint.pprint(fuzzy_tree)