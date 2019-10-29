#include <iostream>
#include "pca.h"
#include "eigen.h"
#include <fstream>
#include <ctime>

using namespace std;

int main(int argc, char** argv) {
    Eigen::Matrix<double, 5, 5> D;
    D << 5.0, 0.0, 0.0, 0.0, 0.0,
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
    B << 1.0, 0.0, 0.0, 0.0, 0.0,
    0.0, 1.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 1.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 1.0, 0.0,
    0.0, 0.0, 0.0, 0.0, 1.0;

    B -= 2 * v * v.transpose();
    Eigen::Matrix<double, 5, 5 > M;
    M = B.transpose() * D * B;
<<<<<<< Updated upstream

    Eigen::VectorXd expected(5);
    expected << 5, 4, 3, 2, 1;

    ofstream myfile("results/met-pot-it-errors.out");
    if (!myfile.is_open()) {
        cerr << "Unable to open file";
        return 1;
    }

    unsigned t0, t1;

    for (uint i = 100; i <= 10000; i+=100) {
        t0 = clock();
        auto t = get_first_eigenvalues(M, 5, i, 0.0000000001);
        t1 = clock();

        myfile << i << "," << (t.first - expected).norm() << "," << (t0-t1) << endl;
    }

    myfile.close();


    ofstream myfile2("results/met-pot-eps-errors.out");
    if (!myfile2.is_open()) {
        cerr << "Unable to open file";
        return 1;
    }

    for (double i = 0.001; i >= 0.000000000000000001; i/=10) {
        t0 = clock();
        auto t = get_first_eigenvalues(M, 5, 1000, i);
        t1 = clock();

        myfile2 << i << "," << (t.first - expected).norm() << "," << (t0-t1) << endl;
    }

    myfile2.close();


    return 0;
}

/*
=======
    auto t = get_first_eigenvalues(M, 5, 10000);
    std::cout << t.first << std::endl;   //debería dar [5, 4, 3, 2, 1]
    std::cout << t.second << std::endl;   //debería quedar -0.6 en la diagonal y 0.4 en el resto

        
>>>>>>> Stashed changes
*/