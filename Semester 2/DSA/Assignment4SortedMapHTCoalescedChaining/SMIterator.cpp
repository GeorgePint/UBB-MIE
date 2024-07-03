#include "SMIterator.h"
#include "SortedMap.h"
#include <exception>

using namespace std;

SMIterator::SMIterator(const SortedMap& m) : map(m), current(0), totalElements(0) {
    sortedElements = new TElem[m.numElements];  // numElements gives total number of elements
    int idx = 0;
    for (int i = 0; i < map.capacity; i++) {
        int head = map.heads[i];
        while (head != -1) {
            sortedElements[idx++] = map.elements[head].elem;
            head = map.elements[head].next;
        }
    }
    totalElements = idx;
    sortElements();

//Worst case: Theta(n^2) the sorting dominates the complexity here
//Best case: Theta(n^2)
//Overall case: O(n^2)
}

void SMIterator::sortElements() {
    for (int i = 1; i < totalElements; i++) {
        TElem key = sortedElements[i];
        int j = i - 1;
        while (j >= 0 && map.rel(key.first, sortedElements[j].first)) {
            sortedElements[j + 1] = sortedElements[j];
            j--;
        }
        sortedElements[j + 1] = key;
    }
//Worst case: Theta(n^2)
//Best case: Theta(n^2)
//Overall case: O(n^2)
}

void SMIterator::first() {
    current = 0;
}

void SMIterator::next() {
    if (!valid())
        throw std::exception("Iterator out of bounds");
    current++;
}

bool SMIterator::valid() const {
    return current < totalElements;
}

TElem SMIterator::getCurrent() const {
    if (!valid())
        throw std::exception("Invalid access");
    return sortedElements[current];
}

SMIterator::~SMIterator() {
    delete[] sortedElements;

//Worst case: Theta(n)
//Best case: Theta(n)
//Overall case: O(n)
}
