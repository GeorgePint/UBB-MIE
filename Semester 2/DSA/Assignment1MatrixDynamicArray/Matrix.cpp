#include "Matrix.h"
#include <exception>
using namespace std;


Matrix::Matrix(int nrLines, int nrCols) {
	this->numberOfLines = nrLines;
	this->numberOfColumns = nrCols;
	this->capacity = 1;
	this->numberOfElements = 0;
	this->linesArray = new TElem[capacity];
	this->columnsArray = new TElem[capacity];
	this->elementsArray = new TElem[capacity];
//Complexity Tetha(1)
}

int Matrix::nrLines() const {
	return this->numberOfLines;
//Complexity Tetha(1)
}

int Matrix::nrColumns() const {
	return this->numberOfColumns;
//Complexity Tetha(1)
}

TElem Matrix::element(int i, int j) const {
	if (i < 0 || i >= this->numberOfLines || j < 0 || j >= this->numberOfColumns)
	{
		throw exception();
	}
	int index;
	for (index = 0; index < this->numberOfElements; index++)
	{
		if (this->linesArray[index] == i && this->columnsArray[index] == j)
		{
			return this->elementsArray[index];
		}
	}
	return NULL_TELEM;
/*
Complexity:
Best case: Tetha(1)
Worst case: Tetha(numberofElements)
Total complexity: O(numberofElements)
*/
}

TElem Matrix::modify(int i, int j, TElem newValue) {
	if (i < 0 || i >= this->numberOfLines || j < 0 || j >= this->numberOfColumns)
	{
		throw exception();
	}

	bool existsElement = false;
	int savedIndex;
	TElem previousElement = NULL_TELEM;
	for (int index = 0; index < this->numberOfElements; index++)
	{
		if (this->linesArray[index] == i && this->columnsArray[index] == j)
		{
			existsElement = true;
			savedIndex = index;
			previousElement = this->elementsArray[index];
		}
	}
	if (existsElement) {
		if (newValue == NULL_TELEM) {
			for (int k = savedIndex; k < this->numberOfElements; k++) {
				this->linesArray[k] = this->linesArray[k + 1];
				this->columnsArray[k] = this->columnsArray[k + 1];
				this->elementsArray[k] = this->elementsArray[k + 1];
			}
			numberOfElements--;
			return previousElement;
		}
		else {
			this->elementsArray[savedIndex] = newValue;
			return previousElement;
		}
	}
	else if (!existsElement) {
		if (newValue == NULL_TELEM) {
			return NULL_TELEM;
		}
		if (this->numberOfElements == this->capacity) {
			resize();
		}
		this->linesArray[this->numberOfElements] = i;
		this->columnsArray[this->numberOfElements] = j;
		this->elementsArray[this->numberOfElements] = newValue;
		this->numberOfElements = this->numberOfElements + 1;
		return NULL_TELEM;

	}
	{
		if (this->numberOfElements == this->capacity)
		{
			resize();
		}
		this->linesArray[this->numberOfElements] = i;
		this->columnsArray[this->numberOfElements] = j;
		this->elementsArray[this->numberOfElements] = newValue;
		this->numberOfElements = this->numberOfElements + 1;
		return NULL_TELEM;
	}
/*
Complexity:
Best case: Tetha(1)
Worst case: Tetha(numberofElements)
Total complexity: O(numberofElements)
*/
}

void Matrix::resize() {
	TElem* newLinesArray = new TElem[2 * this->capacity];
	TElem* newColumnsArray = new TElem[2 * this->capacity];
	TElem* newElementsArray = new TElem[2 * this->capacity];
	for (int i = 0; i < this->numberOfElements; i++)
	{
		newLinesArray[i] = this->linesArray[i];
		newColumnsArray[i] = this->columnsArray[i];
		newElementsArray[i] = this->elementsArray[i];
	}
	this->capacity = 2 * this->capacity;
	delete[] this->linesArray;
	delete[] this->columnsArray;
	delete[] this->elementsArray;
	this->linesArray = newLinesArray;
	this->columnsArray = newColumnsArray;
	this->elementsArray = newElementsArray;
//Complexity Tetha(numberofElements)
}

Matrix::~Matrix() {
	delete[] this->elementsArray;
	delete[] this->linesArray;
	delete[] this->columnsArray;
//Complexity: Theta(1)
}
