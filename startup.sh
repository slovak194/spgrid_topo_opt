#!/usr/bin/env bash
set +e

wget https://raw.githubusercontent.com/yuanming-hu/taichi/legacy/install.py
python3 install.py
python3 install.py

set -e

cp -r /content/spgrid_topo_opt /content/taichi/projects/
# rm -rf /content/spgrid_topo_opt
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1LM-2ZztT1_iFccGFRQhR21Cj5wWktctv' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1LM-2ZztT1_iFccGFRQhR21Cj5wWktctv" -O intel_arch.tar.xz && rm -rf /tmp/cookies.txt

!tar xf intel_arch.tar.xz

export CUDA_ARCH=50
export TC_USE_DOUBLE=1
ld_path = %env LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin/:$LD_LIBRARY_PATH
export TC_MKL_PATH=/content/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/
export INTEL_LICENSE_FILE=/content/intel/licenses/intel-sw-tools-license.lic
cd /content/taichi/projects/spgrid_topo_opt/solver && make
cd /content

export TAICHI_NUM_THREADS=8
export TAICHI_REPO_DIR=/content/taichi

export PYTHONPATH=/content/taichi/python/:$PYTHONPATH
export PATH=/content/taichi/bin/:$PATH

sudo apt-get install xorg-dev libglu1-mesa-dev
sudo apt install libnlopt-dev

cd /content/taichi && ti build

cd /content/taichi/projects/spgrid_topo_opt/scripts/ && python3 opt_bridge.py


# export CUDA_ARCH=50
# export TC_USE_DOUBLE=1
# export LD_LIBRARY_PATH=/home/slovak/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/:$LD_LIBRARY_PATH
# export LD_LIBRARY_PATH=/home/slovak/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/compiler/lib/intel64_lin/:$LD_LIBRARY_PATH
# export TC_MKL_PATH=/home/slovak/intel/sw_dev_tools/compilers_and_libraries_2020.0.166/linux/mkl/lib/intel64_lin/

