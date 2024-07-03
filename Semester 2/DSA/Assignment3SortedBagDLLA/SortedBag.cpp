#include "SortedBag.h"
#include "SortedBagIterator.h"

SortedBag::SortedBag(Relation r) {
    this->rel = r;
    this->length = 0;
    this->dlla = new DLLA;
    this->dlla->capacity = 1;
    this->dlla->elems = new Pair[1];
    this->dlla->prev = new int[1];
    this->dlla->next = new int[1];
    this->dlla->prev[0] = -1;
    this->dlla->next[0] = -1;
    this->dlla->head = -1;
    this->dlla->tail = -1;
    this->dlla->first_empty = 0;
//Theta(1)
}

void SortedBag::resize() {
    Pair* new_elems = new Pair[2 * this->dlla->capacity];
    int* new_prev = new int[2 * this->dlla->capacity];
    int* new_next = new int[2 * this->dlla->capacity];

    for (int i = 0; i < this->dlla->capacity; i++) {
        new_elems[i] = this->dlla->elems[i];
        new_prev[i] = this->dlla->prev[i];
        new_next[i] = this->dlla->next[i];
    }
    for (int i = this->dlla->capacity; i < this->dlla->capacity * 2 - 1; i++) {
        new_prev[i] = i - 1;
        new_next[i] = i + 1;
    }
    new_prev[this->dlla->capacity * 2 - 1] = this->dlla->capacity * 2 - 2;
    new_next[this->dlla->capacity * 2 - 1] = -1;

    delete[] this->dlla->elems;
    delete[] this->dlla->prev;
    delete[] this->dlla->next;

    this->dlla->elems = new_elems;
    this->dlla->prev = new_prev;
    this->dlla->next = new_next;
    this->dlla->first_empty = this->dlla->capacity;
    this->dlla->capacity = this->dlla->capacity * 2;
    //BC=WC=TOTAL=Theta(capacity)
}



void SortedBag::add(TComp e) {
    Pair new_elem{};
    new_elem.frequency = 1;
    new_elem.element = e;

    int current = this->dlla->head;
    int prev = -1;

    while (current != -1 && this->rel(this->dlla->elems[current].element, e)) {
        prev = current;
        current = this->dlla->next[current];
    }


    if (current != -1 && this->dlla->elems[current].element == e) {
        //if the element already exists
        this->dlla->elems[current].frequency++;
        this->length++;
        return;
    }

    if (this->dlla->first_empty == -1)
        this->resize();

    int new_position = this->dlla->first_empty;
    this->dlla->elems[new_position] = new_elem;
    this->dlla->first_empty = this->dlla->next[this->dlla->first_empty];

    if (prev == -1) {
        //element is inserted into the first position
        this->dlla->prev[new_position] = -1;
        this->dlla->next[new_position] = this->dlla->head;
        if (this->dlla->head != -1)
            this->dlla->prev[this->dlla->head] = new_position;
        this->dlla->head = new_position;
    }
    else {
        //element is inserted in the middle 
        this->dlla->prev[new_position] = prev;
        this->dlla->next[new_position] = this->dlla->next[prev];
        if (this->dlla->next[prev] != -1)
            this->dlla->prev[this->dlla->next[prev]] = new_position;

        else
        {
            this->dlla->tail = new_position;
        }
        this->dlla->next[prev] = new_position;
    }

    this->length++;
//Best case: Theta(1) if the element is added at the beginning or the end of the sorted bag.
//Worst case: Theta(capacity) if the bag needs to be resized before adding the element.
//Overall average : Theta(capacity).
}


bool SortedBag::remove(TComp e) {
    int current_node = this->dlla->head;

    while (current_node != -1 && this->dlla->elems[current_node].element != e)
        current_node = this->dlla->next[current_node];

    if (current_node != -1) {
        if (this->dlla->elems[current_node].frequency > 1)
            this->dlla->elems[current_node].frequency--;
        else {
            if (this->dlla->prev[current_node] == -1)
                this->dlla->head = this->dlla->next[current_node];
            else
                this->dlla->next[this->dlla->prev[current_node]] = this->dlla->next[current_node];

            if (this->dlla->next[current_node] != -1)
                this->dlla->prev[this->dlla->next[current_node]] = this->dlla->prev[current_node];
            else
                this->dlla->tail = this->dlla->prev[current_node];

            this->dlla->next[current_node] = this->dlla->first_empty;
            this->dlla->first_empty = current_node;
        }
        this->length--;
        return true;
    }
    return false;


//Best case: Theta(1) if the element is at the beginning or the end of the sorted bag and its frequency becomes 0.
//Worst case: Theta(nrNodes) if the element needs to be searched through the entire bag.
//Overall average : Theta(nrNodes).
}

bool SortedBag::search(TComp elem) const {
    int current = this->dlla->head;
    while (current != -1 && this->dlla->elems[current].element != elem)
        current = this->dlla->next[current];
    return current != -1;
//Best case: Theta(1) if the element is at the beginning of the sorted bag.
//Worst case: Theta(nrNodes) if the element is at the end of the bag or not present.
//Overall average : Theta(nrNodes).
}



int SortedBag::nrOccurrences(TComp elem) const {
    int current = this->dlla->head;
    while (current != -1 && this->dlla->elems[current].element != elem)
        current = this->dlla->next[current];

    int occurrences = 0;
    while (current != -1 && this->dlla->elems[current].element == elem) {
        occurrences += this->dlla->elems[current].frequency;
        current = this->dlla->next[current];
    }

    return occurrences;
//Best case: Theta(1) if the element is at the beginning of the sorted bag.
//Worst case: Theta(nrNodes) if the element is at the end of the bag or not present.
//Overall average : Theta(nrNodes).
}



int SortedBag::size() const {
    return this->length;

//Theta(1)
}


bool SortedBag::isEmpty() const {
    return this->length == 0;

//Theta(1)
}


SortedBagIterator SortedBag::iterator() const {
	return SortedBagIterator(*this);

//Theta(1)
}


SortedBag::~SortedBag() {
    delete[] this->dlla->elems;
    delete[] this->dlla->prev;
    delete[] this->dlla->next;

//Theta(nrNodes)
}
