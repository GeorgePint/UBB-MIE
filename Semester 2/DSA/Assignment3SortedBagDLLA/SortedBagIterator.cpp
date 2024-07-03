#include "SortedBagIterator.h"
#include "SortedBag.h"
#include <exception>

SortedBagIterator::SortedBagIterator(const SortedBag& b) : bag(b) {
    this->current = this->bag.dlla->head;
    this->freq = (this->current != -1) ? this->bag.dlla->elems[current].frequency : 0;
    this->forward = true;;
}

TComp SortedBagIterator::getCurrent() {
    if (this->valid())
        return this->bag.dlla->elems[current].element;
    else
        throw std::exception();
}

bool SortedBagIterator::valid() const {
    return this->current != -1;
}

void SortedBagIterator::next() {
	if (this->valid()) {
		if (this->freq == 1) {
			if (this->forward) {
				this->current = (this->current != -1) ? this->bag.dlla->next[this->current] : -1;
			}
			else {
				this->current = (this->current != -1) ? this->bag.dlla->prev[this->current] : -1;
			}
			this->freq = (this->current != -1) ? this->bag.dlla->elems[this->current].frequency : 0;
		}
		else {
			this->freq--;
		}
	}
	else {
		throw std::exception();
	}
}

void SortedBagIterator::first() {
	this->current = this->bag.dlla->head;
	this->freq = (this->current != -1) ? this->bag.dlla->elems[current].frequency : 0;
	this->forward = true;
}
