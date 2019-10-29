	#include <iostream>
#include "pca.h"
#include "eigen.h"

using namespace std;

PCA::PCA(unsigned int n_components)
{
	alpha = n_components;
}

void PCA::fit(Matrix X)
{
	int n = X.rows();

	Vector mu = X.rowwise().sum();
	mu = mu / n;

	Vector iesima(X.cols());

	Matrix res(X.rows(), X.cols());

	for(int i = 0; i < n; i++)
		res.row(i) = (X.row(i) - mu) / sqrt(n - 1);

	covarianza = (res.transpose())*res;
}

MatrixXd PCA::transform(SparseMatrix X)
{
	Matrix denseX = Matrix(X);

	// obtenemos alpha autovalores para calcular la transformacion caracteristica
	pair<Vector, Matrix> eigenV = get_first_eigenvalues(covarianza, alpha);

	Matrix eigen = eigenV.second;
	MatrixXd res(denseX.rows(), alpha);
	
	// calculamos la transformacion carcteristica de cada fila
	int i = 0;
	for(; i < denseX.rows(); i++) {
		Vector row = denseX.row(i).head(alpha);
		res.row(i) = tc(row, eigen);
	}


	return res;
}

Vector PCA::tc(Vector &f, Matrix &eigen) {
	Vector res = Vector(alpha);

	for(unsigned int i = 0; i < alpha; i++)
		res(i) = eigen.col(i).dot(f);

	return res;
}


