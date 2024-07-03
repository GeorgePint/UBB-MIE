#include "Map.h"
#include "MapIterator.h"
#include <exception>
using namespace std;


MapIterator::MapIterator(const Map& d) : map(d)
{
	this->current = d.head;
//Overall complexity: Tetha(1)
}


void MapIterator::first() {
	current = map.head;
//Overall complexity: Tetha(1)
}


void MapIterator::next() {
	// Move the iterator to the next element in the map
	if (current == nullptr)
		throw exception("Iterator is not valid.");
	current = current->next;
//Overall complexity: Tetha(1)
}	


TElem MapIterator::getCurrent(){
	if (!valid())
		throw exception("Iterator is not valid.");
	return current->data;
//Overall complexity: Tetha(1)
}


bool MapIterator::valid() const {
	return current != nullptr;
//Overall complexity: Tetha(1)
}
