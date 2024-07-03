#pragma once
//DO NOT INCLUDE SORTEDMAPITERATOR

//DO NOT CHANGE THIS PART
typedef int TKey;
typedef int TValue;
#include <utility>
#include <cmath>
typedef std::pair<TKey, TValue> TElem;
#define NULL_TVALUE -1
#define NULL_TPAIR pair<TKey, TValue>(-1, -1);
#define NULL_TELEM -1

typedef std::pair<TKey, TValue> TElem;

class SMIterator;
typedef bool(*Relation)(TKey, TKey);

class SortedMap {
	friend class SMIterator;
    private:
        struct Node {
            TElem elem;
            int next;
        };
        Node* elements;
        int* heads;
        int capacity;
        int numElements;
        int firstEmpty;
        Relation rel;
        int hash(TKey k) const;
        void resizeAndRehash();
    public:

        void changeFirstEmpty(); 
        //    m.firstEmpty = m.firstEmpty + 1;
        //    while (m.firstEmpty < m.numElements and m.elements[m.firstEmpty] != NULL_TVALUE) {
        //        m.firstEmpty = m.firstEmpty + 1;
        //    }
        //}

    // implicit constructor
        SortedMap(Relation r);

	// adds a pair (key,value) to the map
	//if the key already exists in the map, then the value associated to the key is replaced by the new value and the old value is returned
	//if the key SMes not exist, a new pair is added and the value null is returned
        TValue add(TKey k, TValue v);

	//searches for the key and returns the value associated with the key if the map contains the key or null: NULL_TVALUE otherwise
        TValue search(TKey k) const;


	//removes a key from the map and returns the value associated with the key if the key existed ot null: NULL_TVALUE otherwise
        TValue remove(TKey k);

	//returns the number of pairs (key,value) from the map
	int size() const;

	//checks whether the map is empty or not
	bool isEmpty() const;

    // return the iterator for the map
    // the iterator will return the keys following the order given by the relation
    SMIterator iterator() const;

    // destructor
    ~SortedMap();
};
