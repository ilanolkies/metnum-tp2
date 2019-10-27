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
	//Matrix<tipo, filas, columnas>
	
	
	int filas = X.rows();
	
	Vector mu = X.rowwise().sum();
	mu = mu/filas;
	
	
	Vector iesima;
	
	Matrix res;
	for(int i = 0; i < filas; i++){
		iesima = X.row(i);
		iesima = iesima - mu;
		iesima = iesima/sqrt(filas - 1);
		res.row(i) = iesima;
	}
	
	covarianza = (res.transpose())*res; 
}


MatrixXd PCA::transform(SparseMatrix X)
{
	Matrix denseX = Matrix(X);
	fit(denseX);
	
	
	
	pair<Vector, Matrix> eigenV = get_first_eigenvalues(covarianza, alpha); //definir esos dos valores
	//Devuelve vector de los alpha autovalores de mayor valor absoluto con sus autovectores asociados.
	//Autovectores son las columnas de la matriz X. 
	//ordenados por valor absoluto -> de mayor a menor.
	
	MatrixXd res;
	
	for(int i = 0; i < denseX.rows(); i++){
		Vector filai = denseX.row(i);
		
		res.row(i) = tc(filai, get<1>(eigenV));
		
	}
	
	return res;
}

Vector PCA::tc(Vector f, Matrix eigen){
	Vector res;
	
	for(unsigned int i = 0; i < alpha; i++){
		Vector vec = eigen.col(i);
		res(i) = vec.dot(f);//dot product entre f y vec
		
	}
	
	
	
	return res;
}


