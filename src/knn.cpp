#include <algorithm>
//#include <chrono>
#include <iostream>
#include "knn.h"
#include <limits>  
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

  for (unsigned k = 0; k < X.rows(); ++k)
  {
      //Para cada elemento de la matriz X entrante predecimos
      ret(k) = 0;
  }

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
	

  /*
  for(int k = 0; k < matrizX.rows(); k++){
    for(SparseMatrix::InnerIterator it(matrizX,k); it; ++it){
      printf("k:%d\n",k );
      printf("row:%lu col:%lu value:%f\n",it.row(),it.col(),it.value());
      printf("index:%lu\n", it.index() );
    }
  }
  */



  cercano a;
	a.distancia = numeric_limits<int>::max();
	a.resenia = false;
  list<cercano > distances(k,a);



  double distancia = 0;
  //Para cada dato calculo la distancia euclediana
  for(int k = 0 ; k < matrizX.outerSize(); k++){
  	SparseMatrix::InnerIterator it(X, fila); 
  	SparseMatrix::InnerIterator it_interno(matrizX,k);



  	while(it || it_interno){

      //Mientras sea menor 
  		while(it.index() < it_interno.index()){
  			distancia += it.value() * it.value();
  			++it;

  		}
  		while(it_interno.index() < it.index()){
  			distancia += it_interno.value()*it_interno.value();
  			++it_interno;
        //printf("col:%ld row:%ld\n  k: %d", it.col(), it.row(), k);
  		}
  		if(it_interno.index() == it.index() ){
  			distancia += pow(it.value()-it_interno.value(), 2);
  			++it_interno;
  			++it;
        //printf("col:%ld row:%ld\n  k: %d", it.col(), it.row(), k);
  		}

      //printf("col:%ld row:%ld\n  k: %d", it.col(), it.row(), k);

  	}





  	//Agregado a lista
  	cercano a;
  	a.distancia = distancia;


  	//Puede generar error:
  	a.resenia = matrizY(0,k); 
  	bool agregado = false;
  	for(auto it_lista = distances.begin(); it_lista != distances.end(); it_lista++){
  		if((*it_lista).distancia < a.distancia){
  			distances.insert(it_lista,a);
  			agregado = true;
  			break;
  		}

  	}

  	if(!agregado){
  		distances.push_back(a);
  	}

  	//Borro un elemento de la lista
  	distances.pop_front();

  }

  unsigned int positivas = 0;
  for(auto it_lista = distances.begin(); it_lista != distances.end(); it_lista++){
    if((*it_lista).resenia){
      positivas++;
    }


  }
  if(positivas >= k/2){
    return true;
  }else{
    return false;
  }


}
 


/*
unsigned int predictPoint(vector<int, int> point){
    list<int >distances;
    
    for(int i = 0; i < trainx.size(); i++){
        float distancia;
        int k = 0;
        for(int j = 0; j < point.size(); j++){
            while(get<0>(trainx[i][k]) < get<0>(point[j])){
                distancia += get<1>(trainx[i][k])^2;
                k++;
            }
            if(get<0>(train[i][k]) == get<0>(point[j])){
                distancia += (get<1>train[i][k] - get<1>point[j])^2;
                k++;
            }
        }
        while(k < trainx[i].size()){
            distancia += get<1>(trainx[i][k])^2;
            k++;
        }
        distancia = sqrt(distancia);
        //Insercion lista
        
        for(auto it = distances.begin(); it != distances.end(); it++){
            
        }
}
    
*/    
    
    