#include <iostream>
#include <vector>
#include <set>
#include <algorithm>

using namespace std;

// Define Matrix as a vector of vectors of integers
typedef vector<vector<int>> Matrix;

// Function to create an identity matrix of size n
Matrix identity(int n) {
    Matrix id(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) {
        id[i][i] = 1;
    }
    return id;
}

// Function to multiply two n x n matrices in Z2
Matrix multiply(const Matrix& a, const Matrix& b, int n) {
    Matrix result(n, vector<int>(n, 0));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            for (int k = 0; k < n; ++k) {
                result[i][j] = (result[i][j] + a[i][k] * b[k][j]) % 2;
            }
        }
    }
    return result;
}

// Function to compute the determinant of an n x n matrix in Z2 (recursive)
int determinant(const Matrix& m, int n) {
    if (n == 1) {
        return m[0][0];
    }
    else if (n == 2) {
        return (m[0][0] * m[1][1] - m[0][1] * m[1][0] + 2) % 2;
    }
    else {
        int det = 0;
        for (int p = 0; p < n; ++p) {
            Matrix subMatrix(n - 1, vector<int>(n - 1));
            for (int i = 1; i < n; ++i) {
                int sub_j = 0;
                for (int j = 0; j < n; ++j) {
                    if (j == p) continue;
                    subMatrix[i - 1][sub_j] = m[i][j];
                    sub_j++;
                }
            }
            det = (det + m[0][p] * determinant(subMatrix, n - 1) * ((p % 2 == 0) ? 1 : -1) + 2) % 2;
        }
        return (det + 2) % 2;  // Ensure the result is in Z2
    }
}

// Function to check if a matrix is invertible in Z2
bool isInvertible(const Matrix& m, int n) {
    return determinant(m, n) != 0;
}

// Function to compute the order of a matrix in the group
int order(const Matrix& m, int n) {
    Matrix current = identity(n);
    for (int i = 1; i <= 12; ++i) {  // Order is bounded by the least common multiple of 1 to n, but 12 is a safe upper limit for small n
        current = multiply(current, m, n);
        if (current == identity(n)) {
            return i;
        }
    }
    return -1;  // This should never happen
}

// Function to generate the group GLn(Z2)
vector<Matrix> generateGLn(int n) {
    vector<Matrix> elements;
    int num_matrices = 1 << (n * n);  // 2^(n^2) possible matrices
    for (int i = 0; i < num_matrices; ++i) {
        Matrix m(n, vector<int>(n, 0));
        for (int j = 0; j < n * n; ++j) {
            m[j / n][j % n] = (i & (1 << j)) ? 1 : 0;
        }
        if (isInvertible(m, n)) {
            elements.push_back(m);
        }
    }
    return elements;
}

bool areEqual(const Matrix& a, const Matrix& b) {
    return a == b;
}

bool contains(const vector<Matrix>& vec, const Matrix& m) {
    return find(vec.begin(), vec.end(), m) != vec.end();
}

vector<vector<Matrix>> generateSubgroups(const vector<Matrix>& group) {
    vector<vector<Matrix>> subgroups;
    int n = group.size();
    int maxSubgroups = 1 << n;  // 2^n possible subsets
    for (int i = 1; i < maxSubgroups; ++i) {  // Start from 1 to exclude the empty subset
        vector<Matrix> subgroup;
        for (int j = 0; j < n; ++j) {
            if (i & (1 << j)) {
                subgroup.push_back(group[j]);
            }
        }
        // Check if the subgroup is actually a group
        bool isGroup = true;
        for (const auto& a : subgroup) {
            for (const auto& b : subgroup) {
                Matrix product = multiply(a, b, subgroup[0].size());
                if (!contains(subgroup, product)) {
                    isGroup = false;
                    break;
                }
            }
            if (!isGroup) break;
        }
        if (isGroup) {
            subgroups.push_back(subgroup);
        }
    }
    return subgroups;
}

bool isNormalSubgroup(const vector<Matrix>& subgroup, const vector<Matrix>& group) {
    int n = subgroup[0].size();
    for (const auto& g : group) {
        for (const auto& h : subgroup) {
            Matrix gh = multiply(g, h, n);
            Matrix hg = multiply(h, g, n);
            if (!contains(subgroup, gh) || !contains(subgroup, hg)) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    int n;
    cout << "Enter the value of n (2 <= n <= 6): ";
    cin >> n;

    // Generate the group GLn(Z2)
    vector<Matrix> group = generateGLn(n);

    // Print the order of the group and its elements
    cout << "Order of the group GL" << n << "(Z2): " << group.size() << endl;
    cout << "Elements of the group:" << endl;
    for (const auto& elem : group) {
        for (const auto& row : elem) {
            for (int val : row) {
                cout << val << " ";
            }
            cout << endl;
        }
        cout << endl;
    }

    // Calculate and print the order of each element
    cout << "Orders of the elements:" << endl;
    for (const auto& elem : group) {
        cout << "Order: " << order(elem, n) << endl;
        for (const auto& row : elem) {
            for (int val : row) {
                cout << val << " ";
            }
            cout << endl;
        }
        cout << endl;
    }

    // Generate all subgroups
    vector<vector<Matrix>> subgroups = generateSubgroups(group);

    // Print all subgroups
    cout << "Subgroups of GL" << n << "(Z2):" << endl;
    for (const auto& subgroup : subgroups) {
        cout << "{ ";
        for (const auto& elem : subgroup) {
            cout << "{";
            for (const auto& row : elem) {
                for (int val : row) {
                    cout << val << " ";
                }
                cout << "; ";
            }
            cout << "}, ";
        }
        cout << "}" << endl;
    }


    // Identify and print the normal subgroups
    cout << "Normal subgroups of GL" << n << "(Z2):" << endl;
    for (const auto& subgroup : subgroups) {
        if (isNormalSubgroup(subgroup, group)) {
            cout << "{ ";
            for (const auto& elem : subgroup) {
                cout << "{";
                for (const auto& row : elem) {
                    for (int val : row) {
                        cout << val << " ";
                    }
                    cout << "; ";
                }
                cout << "}, ";
            }
            cout << "}" << endl;
        }
    }

    return 0;
}

