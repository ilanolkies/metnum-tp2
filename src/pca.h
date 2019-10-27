#pragma once
#include "types.h"

class PCA {
public:
    PCA(unsigned int n_components);

    void fit(Matrix X);

    Eigen::MatrixXd transform(SparseMatrix X);
private:
	unsigned int alpha;
	
	Vector tc(Vector f, Matrix eigen);

	//Matrix matrizX;
	Matrix covarianza;

};