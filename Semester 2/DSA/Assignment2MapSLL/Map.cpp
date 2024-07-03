#include "Map.h"
#include "MapIterator.h"

Map::Map() {
	this->head = nullptr;
}

Map::~Map() {
	Node* current = head;
	while (current != nullptr) {
		Node* next = current->next;
		delete current;
		current = next;
	}
}

TValue Map::add(TKey c, TValue v){
	Node* current = head;
	while (current != nullptr) {
		if (current->data.first == c) {
			TValue oldValue = current->data.second;
			current->data.second = v;
			return oldValue;
		}
		current = current->next;
	}
	// If the key doesn't exist, create a new node and add it to the list
	Node* newNode = new Node(std::make_pair(c, v));
	newNode->next = head;
	head = newNode;
	return NULL_TVALUE;
/*
Best case: Tetha(1) - When the key already exists at the beginning of the list.
Worst case: Tetha(n) - When the key doesn't exist and the new node needs to be added at the beginning of the list.
Overall complexity: O(n) (since insertion at the beginning of a linked list takes linear time).
*/
}

TValue Map::search(TKey c) const{
	Node* current = head;
	while (current != nullptr) {
		if (current->data.first == c)
			return current->data.second;
		current = current->next;
	}
	return NULL_TVALUE; // Key not found
/*
Best case: Tetha(1) - When the key being searched is at the beginning of the list.
Worst case: Tetha(n) - When the key being searched is not found or located at the end of the list.
Final complexity: O(n) (since searching involves traversing the linked list, which takes linear time in the worst case).
*/
}

TValue Map::remove(TKey c){
	Node* current = head;
	Node* prev = nullptr;
	while (current != nullptr) {
		if (current->data.first == c) {
			// Found the key
			if (prev != nullptr)
				prev->next = current->next;
			else
				head = current->next;
			TValue value = current->data.second;
			delete current;
			return value;
		}
		prev = current;
		current = current->next;
	}
	return NULL_TVALUE; // Key not found
/*
Best case: Tetha(1) - When the node to be removed is at the beginning of the list.
Worst case: Tetha(n) - When the node to be removed is not found or located at the end of the list.
Final complexity: O(n) (since removal involves traversing the linked list to find the node to remove, which takes linear time in the worst case).
*/
}


int Map::size() const {
	// Returns the number of pairs (key, value) in the map
	int count = 0;
	Node* current = head;
	while (current != nullptr) {
		count++;
		current = current->next;
	}
	return count;
/*
Best case: Tetha(n) - When the list is empty.
Worst case: Tetha(n) - When traversing the entire list to count the number of elements.
Final complexity: O(n) (since it always traverses the entire linked list once).
*/
}

bool Map::isEmpty() const{
	return head == nullptr;
//Overall complexity: Tetha(1)
}

MapIterator Map::iterator() const {
	return MapIterator(*this);
//Overall complexity: Tetha(1)
}
