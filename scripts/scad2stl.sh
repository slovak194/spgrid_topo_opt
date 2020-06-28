#!/usr/bin/env bash

TCB_ZIP_FILE_PATH="/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-10-03-r06510__v8_r0400/fem/00047.tcb.zip"
time ~/openscad/openscad -o $TCB_ZIP_FILE_PATH".bin.stl" $TCB_ZIP_FILE_PATH".bin.scad" &

TCB_ZIP_FILE_PATH="/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-40-14-r04804__v8_r0400/fem/00044.tcb.zip"
time ~/openscad/openscad -o $TCB_ZIP_FILE_PATH".bin.stl" $TCB_ZIP_FILE_PATH".bin.scad"


/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-10-03-r06510__v8_r0400/fem/00047.tcb.zip.bin.combined.stl

/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-40-14-r04804__v8_r0400/fem/mirror_stl.combined.stl

