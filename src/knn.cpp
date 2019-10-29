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
  auto result = Vector(X.rows());
  cout << X.cols() <<"  " << X.rows() << endl; 
  cout << X.outerSize() << endl; 

  cout << matrizX.cols() << "   " << matrizX.rows();
  for (int i = 0; i < X.rows(); i++)
    result(i) = predecirFila(X, i);

  return result;
}

bool KNNClassifier::predecirFila(SparseMatrix &X, int fila){
  // min heap para almacenar las distancias, asociadas con la reseña
  priority_queue<cercano> queue;

  double distancia;

  // calculamos la distancia a cada fila de la matriz
  for (uint i = 0; i < matrizX.rows(); i++) {
    distancia = 0;

    // SparseMatrix::InnerIterator itera las columnas existentes
    SparseMatrix::InnerIterator it_train(matrizX, i);
    SparseMatrix::InnerIterator it_test(X, fila);

    // vamos a ir sumando prograsivamente por los indices existentes
    while (it_test && it_train) {
      // si el indice de train es menor que el de test
      while (it_train.index() < it_test.index()) {
        distancia += pow(it_train.value(), 2);
        ++it_train;
      }

      // si el indice de test es menor que el de train
      while (it_test.index() < it_train.index()) {
        distancia += pow(it_test.value(), 2);
        ++it_test;
      }

      // si los indices son iguales
      if (it_test && it_train && it_train.index() == it_test.index()) {
        distancia += pow(it_test.value() - it_train.value(), 2);
        ++it_test;
        ++it_train;
      }
    }

    //Agregado a priority queue
    cercano a;
    a.distancia = sqrt(distancia);
    a.resenia = matrizY(0, i);
    queue.push(a);
  }

  unsigned int positivas = 0;

  // obtenemos los k mas cercanos
  for (unsigned int i = 0; i < k; i++)
    if (queue.empty())
      cerr << "Error cola vacia: K es mayor a cantidad de filas " << endl;
    else {
      cercano a = queue.top();

      if (a.resenia)
        positivas++;

      cout << "distancia" << a.distancia << endl;
      queue.pop();
    }

  return positivas * 2 >= k;
}
