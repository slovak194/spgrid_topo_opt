#!/usr/bin/env bash
set +e

sudo apt-get install xorg-dev libglu1-mesa-dev
sudo apt install libnlopt-dev

pip3 install --user colorama numpy Pillow flask scipy pybind11 flask_cors GitPython yapf distro requests PyQt5
pip3 install --user colorama numpy Pillow flask scipy pybind11 flask_cors GitPython yapf distro requests PyQt5

cp /content/gdrive/My\ Drive/intel_arch.tar.xz ./
tar xvf intel_arch.tar.xz

cp /content/gdrive/My\ Drive/taichi.tar ./
tar xvf taichi.tar.xz

cd /content/taichi/projects/spgrid_topo_opt/ && git pull

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

ln -s /content/gdrive/My\ Drive/topoopt/outputs /content/taichi/

cd /content/taichi/projects/spgrid_topo_opt/scripts && python3 opt_bridge.py

#cd /content/taichi && ti build
