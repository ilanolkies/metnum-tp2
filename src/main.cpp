#include <iostream>
#include "pca.h"
#include "eigen.h"
#include <fstream>
#include <ctime>
#include <sstream>
#include <string>

using namespace std;

int main(int argc, char** argv) {
    string line;

    // matrix de covarianza
    ifstream con_input("../results/predict_cov_matrix.txt");

    Eigen::Matrix<double, 100, 100> M;

    while(getline(con_input, line)) {
        vector<int> lineData;
        stringstream lineStream(line);

        double value;
        while(lineStream >> value)
            M << value;
    }

    // autovalores esperados
    ifstream eigen_input("../results/predict_eigen_v.txt");

    Vector expected(100);

    while(getline(eigen_input, line)) {
        vector<int> lineData;
        stringstream lineStream(line);

        double value;
        while(lineStream >> value) {
            expected << value;
        }
    }

    ofstream myfile("../results/met-pot-it-errors.out");

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

    ofstream myfile2("../results/met-pot-eps-errors.out");

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
