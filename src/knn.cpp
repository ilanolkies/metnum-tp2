#include <algorithm>
//#include <chrono>
#include <iostream>
#include "knn.h"
#include <limits>  
#include <queue>
using namespace std;


KNNClassifier::KNNClassifier(unsigned int n_neighbors)
{
	k = n_neighbors;
}

void KNNClassifier::fit(SparseMatrix X, Matrix y)
{
	
	matrizX = X;
	matrizY = y;



}


Vector KNNClassifier::predict(SparseMatrix X)
{
	// Creamos vector columna a devolver
	auto ret = Vector(X.rows());



	//Creamos arreglo para guardar las filas


	//Predecimos el resultado para cada fila
	for(int i = 0; i < X.rows(); i++)
	{ 
		
		ret(i) = predecirFila(X, i);
		printf("%d\n",i );
	}

	return ret;
}

//SparseMatrix<double>::InnerIterator it(mat,k)

//int k, SparseMatrix X,
bool KNNClassifier::predecirFila(SparseMatrix &X, int fila){


	priority_queue<cercano> queue; 

	double distancia;
	//Para cada fila de la matriz de practica
	for(int k = 0 ; k < matrizX.outerSize(); k++){
		distancia = 0;
		//Calculo distancia con la fila de la matriz de test
		SparseMatrix::InnerIterator it(X, fila); 
		SparseMatrix::InnerIterator it_interno(matrizX,k);


		//Recorro ambos iteradores hasta el final
		while(it || it_interno){

			//Mientras el indice de it es menor entonces no existe ese indice en la otra matriz por lo tanto su valor es 0
			while(it.index() < it_interno.index()){

				//En este caso la distancia de 0 a it.value  = it.value
				distancia += abs(it.value());
				++it;

			}
			//Mismo que anterior pero con indices al revez
			while(it_interno.index() < it.index()){
				distancia += abs(it_interno.value());
				++it_interno;

			}

			//Si los indices son iguales, la distancia es igual al absoluto de la resta entre ambos valores
			if(it_interno.index() == it.index() ){
				distancia += abs( (it.value()-it_interno.value()) );
				++it_interno;
				++it;

			}



		}



		//Agregado a priority queue
		cercano a;
		a.distancia = distancia;
		a.resenia = matrizY(0,k);
		queue.push(a);

	}


	unsigned int positivas = 0;
	for(unsigned int i = 0; i < k; i++){
		if(queue.empty()){
			cerr << "Error cola vacia: K es mayor a cantidad de filas " << endl;
		}else{
			cercano a = queue.top();
			if(a.resenia){
				positivas++;
			}

			queue.pop();
		}	


	}

	if(positivas >= k/2){
		return true;
	}else{
		return false;
	}


}
 

