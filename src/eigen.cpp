#include <algorithm>
#include <chrono>
#include <iostream>
#include "eigen.h"
#include <math.h>

using namespace std;


pair<double, Vector> power_iteration(const Matrix& X, unsigned num_iter, double eps)
{
    Vector b = Vector::Random(X.cols());
    double eigenvalue;
    Vector w;
    double n;
    for(unsigned i = 0; i < num_iter; i++){
        w = X * b;
        n = w.norm();
        if((b - w / n).norm() < eps){
            break;
        }
        b = w / n;
    }
    eigenvalue = b.transpose() * X * b;
    n = pow(b.norm(), 2);
    eigenvalue = eigenvalue / n;
    return make_pair(eigenvalue, b / b.norm());
}

pair<Vector, Matrix> get_first_eigenvalues(const Matrix& X, unsigned num, unsigned num_iter, double epsilon)
{
    Matrix A(X);
    Vector eigvalues(num);
    Matrix eigvectors(A.rows(), num);
    pair<double, Vector > tmp;
    Vector v;
    double autovalor;
    for(unsigned i = 0; i < num; i++){
        tmp = power_iteration(A, num_iter, epsilon);
        v = tmp.second;
        autovalor = tmp.first;
        A = A - autovalor * v * v.transpose();
        eigvalues(i) = autovalor;
        eigvectors.col(i) = v;
    }
    return make_pair(eigvalues, eigvectors);
}
