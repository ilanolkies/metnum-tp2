#include <algorithm>
#include <chrono>
#include <iostream>
#include "eigen.h"
#include <math.h>

using namespace std;


pair<double, Vector> power_iteration(const Matrix& X, unsigned num_iter, double eps) {
  // x_0 arbitrario
  Vector xk = Vector::Random(X.cols());

  Vector w, _xk;

  // metodo de la potencia
  for(unsigned i = 0; i < num_iter; i++) {
    w = X * xk;
    w /= w.norm();

    // criterio de parada
    if((xk - w).norm() < eps)
      break;

    xk = w;
  }

  // xk es autovector, y esta normalizado
  _xk = X * xk;

  // _xk esmmultiplo de xk
  double eigenvalue = _xk[0] * xk[0];

  return make_pair(eigenvalue, xk);
}

pair<Vector, Matrix> get_first_eigenvalues(const Matrix& X, unsigned num, unsigned num_iter, double epsilon) {
  Matrix A(X);
  Vector eigvalues(num);
  Matrix eigvectors(A.rows(), num);

  pair<double, Vector> tmp;
  Vector v;
  double autovalor;

  // metodo de deflacion
  for (unsigned i = 0; i < num; i++) {
    // obtenemos autoval y autovec asociado normalizado
    tmp = power_iteration(A, num_iter, epsilon);

    autovalor = tmp.first;
    v = tmp.second;

    // lo recordamos
    eigvalues(i) = autovalor;
    eigvectors.col(i) = v;

    // paso iterativo
    A = A - autovalor * v * v.transpose();
  }
  return make_pair(eigvalues, eigvectors);
}
