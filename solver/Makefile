LIBRARY = libSPGridCPUSolver.so
CC = ~/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/bin/intel64/icc
# CXXFLAGS = -I../external/ -I../external/ -qopenmp -O3 -std=c++14 -fPIC -mkl -fma -xCORE-AVX512 -DUSING_AVX512 -DUSING_DOUBLE -DICC_18
CXXFLAGS = -I../external/ -I../external/ -qopenmp -O3 -std=c++14 -fPIC -mkl -fma -xCORE-AVX2 -DUSING_AVX2 -DUSING_DOUBLE -DICC_18
CG_FILES := $(wildcard CG/*.cpp)
SPGRID_FILES := $(wildcard ../../../Common_Libraries/SPGrid/Core/*.cpp)
KERNEL_FILES := $(wildcard CPU_Kernel/*.cpp)
AMG_FILES := $(wildcard MG/*.cpp)
CPP_FILES := $(wildcard *.cpp)
all:
	$(CC) -shared $(CXXFLAGS) $(CG_FILES) $(KERNEL_FILES) $(CPP_FILES) $(SPGRID_FILES) $(AMG_FILES) -o $(LIBRARY)
