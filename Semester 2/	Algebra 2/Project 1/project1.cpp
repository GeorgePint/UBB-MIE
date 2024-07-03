#define _CRT_SECURE_NO_WARNINGS

#include <stdlib.h>
#include <stdio.h>

void printTable(FILE* outputFile, int number, char table[4][4]);
bool isAssoc(int number, char table[4][4]);
void getBinarOp(FILE* outputFile, int number, char set[], int size, char table[4][4], int ind, int* counter);

void printTable(FILE* outputFile, int number, char table[4][4]) {
    // function to print the operation table 
    // input: the size of the set(number), the operation table
    // output: the function prints the operation table to the output file
    for (int i = 0; i < number; i++) {
        for (int j = 0; j < number; j++) {
            fprintf(outputFile, "%c ", table[i][j]);
        }
        fprintf(outputFile, "\n");
    }
}

bool isAssoc(int number, char table[4][4]) {
    // function to check if an operation is associative
    // input: the number of elements in the set(number), and the operation table
    // output: true/false
    for (int i = 0; i < number; i++) {
        for (int j = 0; j < number; j++) {
            for (int k = 0; k < number; k++) {
                // Associativity check
                if (table[table[i][j] - 'a'][k] != table[i][table[j][k] - 'a']) {
                    return false;
                }
            }
        }
    }
    return true;
}

// Function to generate all possible binary operations
void getBinarOp(FILE* outputFile, int number, char set[], int size, char table[4][4], int ind, int* counter) {
    // recursive function to generate all the binary operations
    // input: the number of elements(number), the actual elements array(set[]), the size of the array(size),
    // the operation table(table[][]), the index of the current element(ind), and the counter(counter)
    // output: recursively writes all the operation tables to the output file
    if (ind == number * number) {
        // the base case
        if (isAssoc(number, table)) {
            fprintf(outputFile, "\nAssociative operation table %d:\n", (*counter)++);
            printTable(outputFile, number, table);
        }
        return;
    }

    for (int i = 0; i < size; i++) {
        table[ind / number][ind % number] = set[i];
        getBinarOp(outputFile, number, set, size, table, ind + 1, counter);
    }
}

int main() {
    FILE* outputFile;
    outputFile = fopen("output.txt", "w");
    if (outputFile == NULL) {
        printf("Error opening output.txt file.\n");
        return 1;
    }

    int number = 5;
    while (number < 1 || number > 4) {
        printf("Enter the number of elements (1, 2, 3 or 4): ");
        scanf("%d", &number);
        if (number < 1 || number > 4) {
            fprintf(outputFile, "Invalid input, please try again.\n");
        }
    }

    char A[4];
    printf("Enter the %d elements separated by space (a, b, c, d): ", number);
    for (int i = 0; i < number; i++) {
        scanf(" %c", &A[i]);
    }

    char table[4][4];
    int counter = 0;

    getBinarOp(outputFile, number, A, number, table, 0, &counter);

    fprintf(outputFile, "\nNumber of associative operations on set A: %d\n", counter);

    fclose(outputFile);
    return 0;
}
