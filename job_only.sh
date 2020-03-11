#!/usr/bin/env bash

export CUDA_ARCH=50
export TC_USE_DOUBLE=1
export LD_LIBRARY_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin/:$LD_LIBRARY_PATH
export TC_MKL_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/
export INTEL_LICENSE_FILE=/content/intel/licenses/intel-sw-tools-license.lic
export TAICHI_NUM_THREADS=4
export TAICHI_REPO_DIR=/content/taichi
export PYTHONPATH=/content/taichi/python/:$PYTHONPATH
export PATH=/content/taichi/bin/:$PATH

cd /content/taichi/projects/spgrid_topo_opt/scripts && python3 opt_bridge.py
