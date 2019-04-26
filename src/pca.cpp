#include <iostream>
#include "pca.h"
#include "eigen.h"

using namespace std;


PCA::PCA(unsigned int n_components)
{
    
}

void PCA::fit(Matrix X)
{
}


MatrixXd PCA::transform(SparseMatrix X)
{
  throw std::runtime_error("Sin implementar");
}
