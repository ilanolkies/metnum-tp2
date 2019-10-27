//
// Created by pachi on 5/6/19.
//

#include <iostream>
#include "pca.h"
#include "eigen.h"



int main(int argc, char** argv){
  Eigen::Matrix<double, 5, 5> D;
  D <<    5.0, 0.0, 0.0, 0.0, 0.0,
          0.0, 4.0, 0.0, 0.0, 0.0,
          0.0, 0.0, 3.0, 0.0, 0.0,
          0.0, 0.0, 0.0, 2.0, 0.0,
          0.0, 0.0, 0.0, 0.0, 1.0;
  Eigen::VectorXd v(5);
  v(0) = 1;
  v(1) = 1;
  v(2) = 1;
  v(3) = 1;
  v(4) = 1;
    v = v / v.norm();
    Eigen::Matrix<double, 5, 5 > B;
    B <<      1.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 1.0;
    B -= 2 * v * v.transpose();
    Eigen::Matrix<double, 5, 5 > M;
    M = B.transpose() * D * B;
    auto t = get_first_eigenvalues(M, 5, 10000);
    std::cout << t.first << std::endl;   //debería dar [5, 4, 3, 2, 1]
    std::cout << t.second << std::endl;   //debería quedar -0.6 en la diagonal y 0.4 en el resto
    return 0;
}
