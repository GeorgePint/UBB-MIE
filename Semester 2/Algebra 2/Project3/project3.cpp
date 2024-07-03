#include "subgroup.h"
#include <iostream>

subgroup::subgroup() : subgroupCount(0), groupSize(0), tupleLength(0) {}

void subgroup::findSubgroups(int m, int n) {
    if (n < 2 || n > 10 || m < 2 || m > 10) {
        std::cout << "Invalid input!";
        return;
    }

    std::ofstream outputFile("output.txt");

    coordinates.resize(std::max(m, n) + 1);
    groupTuples.resize(m * n + 1, std::vector<int>(2));

    backtrack(1, n, m, n, outputFile);
    backtrack(1, m, m, n, outputFile);

    tupleLength = 0;
    for (int i = 1; i <= m; i++) {
        for (int j = 1; j <= n; j++) {
            if (tupleLength < m * n) {
                groupTuples[tupleLength][0] = coordinates[i];
                groupTuples[tupleLength][1] = coordinates[j];
                tupleLength++;
            }
        }
    }

    groupSize = m * n;
    for (int i = 1; i <= m * n; i++) {
        tupleLength = i;
        backtracking2(1, m, n, outputFile);
    }

    outputFile << "\nThe number of subgroups of the abelian group is: " << subgroupCount;
    outputFile.close();
}

bool subgroup::checkCondition(int k, int m, int n) {
    for (int i = 1; i <= k; ++i) {
        for (int j = 1; j <= k; ++j) {
            if (!searchTuple((groupTuples[i][0] + groupTuples[j][0]) % m,
                (groupTuples[i][1] + groupTuples[j][1]) % n,
                k))
                return false;
        }
    }
    return true;
}

bool subgroup::searchTuple(int xCoord, int yCoord, int k) {
    for (int i = 1; i <= k; ++i) {
        if ((groupTuples[i][0] == xCoord) && (groupTuples[i][1] == yCoord))
            return true;
    }
    return false;
}

void subgroup::Print(int k, int m, int n, std::ofstream& outputFile) {
    if (checkCondition(k, m, n) && groupTuples[0][0] == 0 && groupTuples[0][1] == 0) {
        for (int i = 1; i <= k; ++i)
            outputFile << "(" << groupTuples[i][0] << ", " << groupTuples[i][1] << ") ";
        outputFile << std::endl;
        subgroupCount++;
    }
}

bool subgroup::isValid(int k) {
    for (int i = 1; i < k; ++i) {
        if (coordinates[k] <= coordinates[i])
            return false;
    }
    return true;
}

bool subgroup::isSolution(int k, int n) {
    return k == n;
}

void subgroup::backtracking2(int k, int m, int n, std::ofstream& outputFile) {
    if (k == tupleLength + 1) {
        Print(tupleLength, m, n, outputFile);
        return;
    }

    for (int i = 1; i <= groupSize - tupleLength + k; ++i) {
        groupTuples[k][0] = coordinates[i];
        groupTuples[k][1] = coordinates[i];
        backtracking2(k + 1, m, n, outputFile);
    }
}

char subgroup::backtrack(int k, int n, int m, int nn, std::ofstream& outputFile) {
    for (int i = 0; i < nn; ++i) {
        coordinates[k] = i;
        if (isValid(k)) {
            if (isSolution(k, n))
                return '\0';
            else
                return backtrack(k + 1, n, m, nn, outputFile);
        }
    }
    return '\0';
}
