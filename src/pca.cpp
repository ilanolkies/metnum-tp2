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


	int filas = X.rows();
	
	Vector mu = X.rowwise().sum();
	mu = mu/filas;
	
	
	Vector iesima;
	
	Matrix res(X.rows(), X.cols());
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
	//fit(denseX);
	


	pair<Vector, Matrix> eigenV = get_first_eigenvalues(covarianza, alpha); //definir esos dos valores
	//Devuelve vector de los alpha autovalores de mayor valor absoluto con sus autovectores asociados.
	//Autovectores son las columnas de la matriz X. 
	//ordenados por valor absoluto -> de mayor a menor.



	Matrix eigen = eigenV.second;
	MatrixXd res(eigen.rows(), alpha);

	cout << eigen.rows() << " " << eigen.cols() << endl;

	//cout << eigen << endl;
	for(int i = 0; i < denseX.rows(); i++){
		Vector filai = denseX.row(i).head(alpha);

		res.row(i) = tc(filai, eigen);
		
		Vector a = Vector(alpha);
		

		res.row(i) = a;

		

		
	}

	cout << "res:" << res.rows() << "  " << res.cols() << endl; 
	return res;
}

Vector PCA::tc(Vector &f, Matrix &eigen){
	Vector res = Vector(alpha);
	
	for(unsigned int i = 0; i < alpha; i++){
		Vector vec = eigen.col(i);

		auto a = vec.dot(f);
		res(i) = a;
	}
	
	
	
	return res;
}


