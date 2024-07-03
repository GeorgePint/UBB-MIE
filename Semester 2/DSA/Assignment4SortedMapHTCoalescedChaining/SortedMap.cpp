#include "SMIterator.h"
#include "SortedMap.h"
#include <exception>
#include <iostream>
using namespace std;

SortedMap::SortedMap(Relation r) : rel(r), numElements(0), capacity(10), firstEmpty(0) {
    elements = new Node[capacity];
    heads = new int[capacity];
    for (int i = 0; i < capacity; i++) {
        heads[i] = -1;
        elements[i].next = (i < capacity - 1) ? i + 1 : -1;
    }
//Worst case: Theta(capacity)
//Best case: Theta(capacity)
//Overall case: O(capacity)
}

int SortedMap::hash(TKey k) const {
	return abs(k) % capacity;
//Worst case: Theta(1)
//Best case: Theta(1)
//Overall case: O(1)

}

void SortedMap::changeFirstEmpty() {
    this->firstEmpty = this->firstEmpty + 1;
    while (this->firstEmpty < this->capacity and this->elements[this->firstEmpty].next!=-1)
        this->firstEmpty = this->firstEmpty + 1;
}

void SortedMap::resizeAndRehash() {
    int oldCapacity = capacity;
    capacity *= 2; // Double the size of the array
    Node* newElements = new Node[capacity];
    int* newHeads = new int[capacity];

    // Initialize newHeads and set all newElements.next to -1 (none should initially point to another)
    for (int i = 0; i < capacity; i++) {
        newHeads[i] = -1;
        newElements[i].next = -1;
    }

    // Rehash elements to new table
    for (int i = 0; i < oldCapacity; i++) {
        int current = heads[i];
        while (current != -1) {
            int newIndex = abs(elements[current].elem.first) % capacity; // Get new index
            int next = elements[current].next;

            // Rehash to new index
            // Insert at the beginning of the new index's list
            newElements[current].elem = elements[current].elem;
            newElements[current].next = newHeads[newIndex];
            newHeads[newIndex] = current;

            current = next;
        }
    }

    // Set up the firstEmpty to point to the first unused node in the new array
    firstEmpty = oldCapacity;
    if (oldCapacity < capacity) {
        // Link all new positions together as a free list starting from the old capacity.
        for (int i = oldCapacity; i < capacity - 1; i++) {
            newElements[i].next = i + 1;
        }
        newElements[capacity - 1].next = -1; // Last element in the array should terminate the free list
    }

    delete[] elements;
    delete[] heads;

    elements = newElements;
    heads = newHeads;
//Worst case: Theta(n)
//Best case: Theta(n)
//Overall case: O(n)
}



TValue SortedMap::add(TKey k, TValue v) {

    if (numElements == capacity) resizeAndRehash();


    int idx = hash(k);
    int prev = -1;
    int current = heads[idx];

    // Search for the key in the chain; if found, update the value.
    while (current != -1 && elements[current].elem.first != k) {
        prev = current;
        current = elements[current].next;
    }

    if (current != -1) {// Key found, replace value.
        TValue oldVal = elements[current].elem.second;
        elements[current].elem.second = v;
        return oldVal;
    }
    else {// Key not found, insert new element in the chain.
        int newIdx = firstEmpty;
        firstEmpty = elements[firstEmpty].next;


        elements[newIdx] = { TElem(k, v), heads[idx] };// Insert at the head of the chain.
        heads[idx] = newIdx;
        numElements++;

        while (firstEmpty < capacity && elements[firstEmpty].elem.first != NULL_TVALUE) {
            firstEmpty++;
        }


        return NULL_TVALUE;
    }

//Worst case: Theta(n) triggering a resizing 
//Best case: Theta(1) the key directly maps to an empty slot or replaces an existing key without the need for rehashing
//Overall case: O(n)
}

TValue SortedMap::search(TKey k) const {
    int idx = hash(k);
    for (int current = heads[idx]; current != -1; current = elements[current].next) {
        // Check if the current node in the chain has the key we are looking for.
        if (elements[current].elem.first == k) {
            return elements[current].elem.second; // Key found
        }
    }
    return NULL_TVALUE;
//Worst case: Theta(n) the key is at the end of a long chain, or doesnt exist
//Best case: Theta(1) the key is at the first position of its chain or there are no collisions
//Overall case: O(n)
}

TValue SortedMap::remove(TKey k) {
    int idx = hash(k);
    int current = heads[idx];
    int prev = -1;
    while (current != -1 && elements[current].elem.first != k) {
        prev = current;
        current = elements[current].next;
    }
    if (current == -1) {
        return NULL_TVALUE;  // Key not found
    }
    TValue removedValue = elements[current].elem.second;// Store value to return.

    // Remove the element by updating links and possibly shifting elements to maintain integrity.
    int nextNode = elements[current].next;
    while (nextNode != -1) {
        elements[current].elem = elements[nextNode].elem;// Shift element forward.
        prev = current;
        current = nextNode;
        nextNode = elements[current].next;
    }

    // Update the link from previous node or the head if necessary.
    if (prev == -1) {
        heads[idx] = -1;
    }
    else {
        elements[prev].next = -1;
    }
    elements[current].next = firstEmpty;
    firstEmpty = current;
    numElements--;
    return removedValue;

//Worst case: Theta(n) the elements is first in the chain, then you must move multiple elements 
//Best case: Theta(1)
//Overall case: O(n)
}

int SortedMap::size() const {
	return this->numElements;
}

bool SortedMap::isEmpty() const {
	return this->numElements == 0;
}

SMIterator SortedMap::iterator() const {
	return SMIterator(*this);
}

SortedMap::~SortedMap() {
    delete[] elements;
    delete[] heads;
}
