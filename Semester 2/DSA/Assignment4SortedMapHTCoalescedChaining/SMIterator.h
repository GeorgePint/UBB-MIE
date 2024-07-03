#pragma once
#include "SortedMap.h"

//DO NOT CHANGE THIS PART
class SMIterator {
    friend class SortedMap;
private:
    const SortedMap& map;
    TElem* sortedElements;
    int current;
    int totalElements;

public:
    SMIterator(const SortedMap& map);
    void first();
    void next();
    bool valid() const;
    TElem getCurrent() const;
    void sortElements();
    ~SMIterator();
};
