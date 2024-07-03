#include <iostream>
#include <fstream>

constexpr int MAX_GRID_SIZE = 20;

std::ofstream outputFile("output.txt");
int solutionCount = 0;
int gridSize;

int grid[MAX_GRID_SIZE][MAX_GRID_SIZE];
int lines[MAX_GRID_SIZE][MAX_GRID_SIZE], columns[MAX_GRID_SIZE][MAX_GRID_SIZE];

bool isValid(const int grid[][MAX_GRID_SIZE], int size) {
    bool associative = true;
    for (int i = 1; i <= size; ++i) {
        for (int j = 1; j <= size; ++j) {
            for (int k = 1; k <= size; ++k) {
                if (grid[grid[i][j]][k] != grid[i][grid[j][k]]) {
                    associative = false;
                    break;
                }
            }
        }
    }
    if (!associative) {
        return false;
    }
    bool identity = false;
    for (int k = 1; k <= size; ++k) {
        bool isIdentity = true;
        for (int i = 1; i <= size; ++i) {
            if (grid[k][i] != i || grid[i][k] != i) {
                isIdentity = false;
                break;
            }
        }
        if (isIdentity) {
            identity = true;
            break;
        }
    }
    if (!identity) {
        return false;
    }

    return true;
}

void printGrid(const int grid[][MAX_GRID_SIZE], int size) {
    outputFile << "Solution " << solutionCount + 1 << ":\n";
    for (int i = 1; i <= size; ++i) {
        outputFile << '\t';
        for (int j = 1; j <= size; ++j)
            outputFile << static_cast<char>(grid[i][j] + 'a' - 1) << ' ';
        outputFile << '\n';
    }
    outputFile << '\n';
}

void backtracking(int grid[][MAX_GRID_SIZE], int currentSquare, int size) {
    if (currentSquare == size * size + 1) {
        if (isValid(grid, size)) {
            printGrid(grid, size);
            ++solutionCount;
        }
        return;
    }

    int x = (currentSquare % size == 0 ? currentSquare / size - 1 : currentSquare / size) + 1;
    int y = currentSquare % size == 0 ? size : currentSquare % size;

    if (x > y) {
        grid[x][y] = grid[y][x];
        if (lines[x][grid[x][y]] != 0 || columns[y][grid[x][y]] != 0) {
            return;
        }
        lines[x][grid[x][y]] = 1;
        columns[y][grid[x][y]] = 1;
        backtracking(grid, currentSquare + 1, size);
        lines[x][grid[x][y]] = 0;
        columns[y][grid[x][y]] = 0;
    }
    else {
        for (int i = 1; i <= size; ++i) {
            grid[x][y] = i;
            if (lines[x][grid[x][y]] != 0 || columns[y][grid[x][y]] != 0) {
                continue;
            }
            lines[x][grid[x][y]] = 1;
            columns[y][grid[x][y]] = 1;
            backtracking(grid, currentSquare + 1, size);
            lines[x][grid[x][y]] = 0;
            columns[y][grid[x][y]] = 0;
        }
    }
}

int main() {
    std::cout << "Enter the grid size: ";
    std::cin >> gridSize;
    backtracking(grid, 1, gridSize);
    outputFile << "The total number of solutions is: " << solutionCount << std::endl;
    return 0;
}





