#pragma once

#include "types.h"



class KNNClassifier {
public:
    KNNClassifier(unsigned int n_neighbors);

    void fit(SparseMatrix X, Matrix y);

    Vector predict(SparseMatrix X);
private:
	unsigned int k;
	SparseMatrix matrizX;
	Matrix matrizY;

	bool predecirFila(SparseMatrix &X, int fila);


};
	
struct cercano
{
	double distancia;
	bool resenia;

	bool operator<(const struct cercano& other) const
    {
        return other.distancia < distancia;
    }


};