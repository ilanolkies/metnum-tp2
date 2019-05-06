//
// Created by pachi on 5/6/19.
// Ejemplo basado en la pregunta de stackoverflow:
// https://stackoverflow.com/questions/47762543/segfault-when-using-pybind11-wrappers-in-c

#include <iostream>
#include "pca.h"
#include "eigen.h"

#include <pybind11/embed.h>

namespace py = pybind11;

int main(int argc, char** argv){

  py::scoped_interpreter guard{};

  py::print("Hola pybind!");

  return 0;
}
