# NOTE(fragofer): based on Example CMakeLists.txt from project CryFS to automatically find OpenMP https://github.com/cryfs/cryfs/blob/08ed96680876c960d5aab0aabebb25206f0bda06/vendor/cryptopp/CMakeLists.txt

if(USE_OpenMP)
    if (MSVC)
        message(WARNING "MSVC does not support the OpenMP 4.0 standard used by Crypto++. Disabling OpenMP. This can cause degraded performance.")
    else()

        find_package(OpenMP)

        if (OPENMP_FOUND OR OPENMP_CXX_FOUND)
            message(STATUS "Found libomp without any special flags")
        endif()

        # If OpenMP wasn't found, try if we can find it in the default Macports location
        if((NOT OPENMP_FOUND) AND (NOT OPENMP_CXX_FOUND) AND EXISTS "/opt/local/lib/libomp/libomp.dylib") # older cmake uses OPENMP_FOUND, newer cmake also sets OPENMP_CXX_FOUND, homebrew installations seem only to get the latter set.
            set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp -I/opt/local/include/libomp/")
            set(OpenMP_CXX_LIB_NAMES omp)
            set(OpenMP_omp_LIBRARY /opt/local/lib/libomp/libomp.dylib)

            find_package(OpenMP)
            if (OPENMP_FOUND OR OPENMP_CXX_FOUND)
                message(STATUS "Found libomp in macports default location.")
            else()
                message(FATAL_ERROR "Didn't find libomp. Tried macports default location but also didn't find it.")
            endif()
        endif()

        # If OpenMP wasn't found, try if we can find it in the default Homebrew location
        if((NOT OPENMP_FOUND) AND (NOT OPENMP_CXX_FOUND) AND EXISTS "/usr/local/opt/libomp/lib/libomp.dylib")
            set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp -I/usr/local/opt/libomp/include")
            set(OpenMP_CXX_LIB_NAMES omp)
            set(OpenMP_omp_LIBRARY /usr/local/opt/libomp/lib/libomp.dylib)

            find_package(OpenMP)
            if (OPENMP_FOUND OR OPENMP_CXX_FOUND)
                message(STATUS "Found libomp in homebrew default location.")
            else()
                message(FATAL_ERROR "Didn't find libomp. Tried homebrew default location but also didn't find it.")
            endif()
        endif()

        set(Additional_OpenMP_Libraries_Workaround "")

        # Workaround because older cmake on apple doesn't support FindOpenMP
        if((NOT OPENMP_FOUND) AND (NOT OPENMP_CXX_FOUND))
            if((APPLE AND ((CMAKE_CXX_COMPILER_ID STREQUAL "AppleClang") OR (CMAKE_CXX_COMPILER_ID STREQUAL "Clang")))
                    AND ((CMAKE_CXX_COMPILER_VERSION VERSION_GREATER_EQUAL "7.0") AND (CMAKE_VERSION VERSION_LESS "3.12.0")))
                message(STATUS "Applying workaround for OSX OpenMP with old cmake that doesn't have FindOpenMP")
                set(OpenMP_CXX_FLAGS "-Xclang -fopenmp")
                set(Additional_OpenMP_Libraries_Workaround "-lomp")
            else()
                message(FATAL_ERROR "Did not find OpenMP. Build with -DDISABLE_OPENMP=ON if you want to allow this and are willing to take the performance hit.")
            endif()
        endif()

        if(NOT TARGET OpenMP::OpenMP_CXX)
            # We're on cmake < 3.9, handle behavior of the old FindOpenMP implementation
            message(STATUS "Applying workaround for old CMake that doesn't define FindOpenMP using targets")
            add_library(OpenMP_TARGET INTERFACE)
            add_library(OpenMP::OpenMP_CXX ALIAS OpenMP_TARGET)
            target_compile_options(OpenMP_TARGET INTERFACE ${OpenMP_CXX_FLAGS}) # add to all targets depending on this
            find_package(Threads REQUIRED)
            target_link_libraries(OpenMP_TARGET INTERFACE Threads::Threads)
            target_link_libraries(OpenMP_TARGET INTERFACE ${OpenMP_CXX_FLAGS} ${Additional_OpenMP_Libraries_Workaround})
        endif()
    endif()
else()
#    message(WARNING "OpenMP is disabled. This can cause degraded performance.")
    set(OpenMP_FOUND OFF)
endif()

#if (NOT OpenMP_FOUND)
#    message("OpenMP not found. Ignoring unknown pragmas during compile-time.")
#    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-unknown-pragmas")
#
#    add_library(OpenMP_TARGET INTERFACE)
#    add_library(OpenMP::OpenMP_CXX ALIAS OpenMP_TARGET)
#    target_compile_options(OpenMP_TARGET INTERFACE ${OpenMP_CXX_FLAGS}) # add to all targets depending on this
##    find_package(Threads REQUIRED)
##    target_link_libraries(OpenMP_TARGET INTERFACE Threads::Threads)
##    target_link_libraries(OpenMP_TARGET INTERFACE ${OpenMP_CXX_FLAGS} ${Additional_OpenMP_Libraries_Workaround})
#endif()