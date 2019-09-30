cmake_minimum_required(VERSION 2.8.12)
project(tp2)

set (CMAKE_CXX_STANDARD 14)
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall")


IF(CMAKE_BUILD_TYPE MATCHES Debug)
    message("Debug mode")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g3 -O0")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror")
ENDIF()

IF(CMAKE_BUILD_TYPE MATCHES Release)
    message("Release mode")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")
ENDIF()

# si se usa un virtual environment setearlo aca
#set(PYTHON_EXECUTABLE "/anaconda3/envs/metnum/bin/python")
#set(PYTHON_LIBRARY "/anaconda3/envs/metnum/lib/libpython3.6m.dylib")

# Prender y apagar este flga para soporte OpenMP
#set(USE_OpenMP ON)
# Script cmake ``multi-plataforma`` (testeado en MacOS y Ubuntu)
#include(OpenMP.cmake)

include_directories(eigen)

add_subdirectory(pybind11)

pybind11_add_module(sentiment
                    src/sentiment.cpp
                    src/knn.cpp
                    src/pca.cpp
                    src/eigen.cpp)

# Por cada módulo que use OpenMP ponerlo como dependencia de esta forma
target_link_libraries(sentiment)#LINK_PUBLIC OpenMP::OpenMP_CXX)

# This variable is used to locate the bin directory where the application will be installed
set(CMAKE_INSTALL_PREFIX
        ${PROJECT_SOURCE_DIR}
        CACHE PATH "Python custom modules directory" FORCE)

message(CMAKE_INSTALL_PREFIX = "${CMAKE_INSTALL_PREFIX}")

install(TARGETS sentiment DESTINATION ${CMAKE_INSTALL_PREFIX}/notebooks)
