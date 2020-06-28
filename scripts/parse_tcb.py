#!/usr/bin/env python3

import sys
import os
from pathlib import Path
import time
import copy

import subprocess as sp
import numpy as np
import matplotlib.pyplot as plt

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl

# #%%gui qt
# from IPython import get_ipython
# ipython = get_ipython()
# if ipython is not None:
#     ipython.magic("gui qt")


def recurse_union(inp):
    datalen = inp.shape[0]

    if datalen < 3:
        ld = ""
        for lrow in inp:
            ld += "\ttranslate(v = [{0}, {1}, {2}])".format(lrow[0], lrow[1], lrow[2]) + \
                  " {\n\t\tcube(size = [1.1,1.1,1.1], center = true);\n\t}\n"
        return ld

    else:
        datalen_half = int(datalen / 2)
        ld = "union() {\n"
        ld += recurse_union(inp[0:datalen_half])
        ld += recurse_union(inp[datalen_half:])
        ld += "}\n"

        return ld


def pc2vox(pc, shaded=True, solid_iso_value=0.2):
    vx = np.zeros((pc[:, 0].max().astype(int) + 1,
                   pc[:, 1].max().astype(int) + 1,
                   pc[:, 2].max().astype(int) + 1) + (4,), dtype=np.ubyte)

    # pc[:, 3] = np.sqrt(pc[:, 3]) * 255
    pc[:, 3] = pc[:, 3] * 255
    pc_uint8 = pc.astype(np.ubyte)

    vx[pc_uint8[:, 0], pc_uint8[:, 1], pc_uint8[:, 2], 3] = pc_uint8[:, 3]

    if shaded:
        vx[..., 0] = vx[..., 3]
        vx[..., 1] = vx[..., 3]
        # vx[..., 2] = 255 - vx[..., 3]

        vx[vx[..., 3] < 255*solid_iso_value, 2] = 255 - vx[vx[..., 3] < 255*solid_iso_value, 3]
        # vx[vx[..., 3] < 255*solid_iso_value, 0] = 0 #vx[vx[..., 3] < 255*solid_iso_value, 3]
        # vx[vx[..., 3] < 255*solid_iso_value, 1] = 0 #vx[vx[..., 3] < 255*solid_iso_value, 3]
        # (255/1 - vx[vx[..., 3] < 255*solid_iso_value, 3]/1).astype(np.ubyte)

    else:
        vx[..., 0] = vx[..., 3]
        vx[..., 1] = vx[..., 3]

        vx[vx[..., 3] > 255*solid_iso_value, 3] = 255
        vx[np.logical_not(vx[..., 3] > 255*solid_iso_value), 3] = 0

    return vx


def get_data(l_bin_file_path):

    point_cloud = np.fromfile(l_bin_file_path, dtype=np.float32).reshape((-1, 4))

    point_cloud[:, 0] = point_cloud[:, 0] - point_cloud[:, 0].min()
    point_cloud[:, 1] = point_cloud[:, 1] - point_cloud[:, 1].min()
    point_cloud[:, 2] = point_cloud[:, 2] - point_cloud[:, 2].min()

    solid_iso_value = 0.2
    # plt.plot(np.array(sorted(point_cloud[:, 3].tolist())))
    point_cloud_sorted = point_cloud[point_cloud[:, 3] > solid_iso_value, 0:4]
    pc_ratio = point_cloud_sorted.shape[0]/point_cloud.shape[0]
    print("R:" + str(pc_ratio))

    point_cloud_sorted = point_cloud_sorted[point_cloud_sorted[:, 0].argsort()]  # First sort doesn't need to be stable.
    point_cloud_sorted = point_cloud_sorted[point_cloud_sorted[:, 1].argsort(kind='mergesort')]
    point_cloud_sorted = point_cloud_sorted[point_cloud_sorted[:, 2].argsort(kind='mergesort')]

    voxels = pc2vox(point_cloud, solid_iso_value=solid_iso_value, shaded=True)
    # voxels = pc2vox(point_cloud, solid_iso_value=solid_iso_value, shaded=False)

    with open(l_bin_file_path + ".scad", "w") as of:
        of.write(recurse_union(point_cloud_sorted))

    return voxels, pc_ratio


class Visualizer(gl.GLViewWidget):
    read_collected = QtCore.pyqtSignal(np.ndarray)
    latest_log_path = ""
    centered = False
    last_call = 0
    latest_test_dir_path = ""
    latest_test_name = ""
    latest_task_path = ""
    latest_task_name = ""
    latest_fem_path = ""
    latest_log_name = ""

    def __init__(self, log_dir):
        super(Visualizer, self).__init__()

        self.log_dir = log_dir

        self.show()
        
        self.ax = gl.GLAxisItem()
        self.ax.setSize(100,100,100)
        self.addItem(self.ax)

        self.v = gl.GLVolumeItem(np.zeros((10, 10, 10) + (4,), dtype=np.ubyte), smooth=False)
        self.addItem(self.v)
        self.setCameraPosition(azimuth=150, distance=150, elevation=0)
        self.read_collected.connect(self.set_data)

    def get_latest_log_path(self):

        self.latest_test_dir_path = sorted(Path(self.log_dir).iterdir(), key=os.path.getmtime)[-1]

        self.latest_task_path = list(filter(lambda x: os.path.isdir(x), sorted(self.latest_test_dir_path.iterdir(), key=os.path.getmtime)))[-1]
        self.latest_task_name = self.latest_task_path.stem

        latest_fem_path = self.latest_task_path.joinpath("fem")

        if self.latest_fem_path != latest_fem_path:
            self.centered = False
            self.latest_fem_path = latest_fem_path

        l_tcb_file_path = list(filter(lambda x: x.as_posix().endswith(".tcb.zip"), sorted(latest_fem_path.iterdir(), key=os.path.getmtime)))[-1].as_posix()

        return l_tcb_file_path

    def set_data(self, data):
        self.v.setData(data)
        if not self.centered:
            self.v.resetTransform()
            self.v.translate(-data.shape[0] / 2, -data.shape[1] / 2, -data.shape[2] / 2)
            self.centered = True

        d = self.renderToArray((1920, 1080))
        image_file_path = self.latest_test_dir_path.joinpath(self.latest_task_name + ".png").as_posix()
        print(image_file_path)
        pg.makeQImage(d, alpha=False).save(image_file_path)
        

    def emit_data(self):
        latest_log_path = self.get_latest_log_path()
        since_last_called = time.time() - self.last_call

        l_bin_file_path = latest_log_path + ".bin"

        if not os.path.isfile(l_bin_file_path):
            sp.call(["ti", "run", "fem_to_dict", latest_log_path])

        file_size = os.path.getsize(l_bin_file_path)

        if (self.latest_log_path != latest_log_path) and (since_last_called > 5) and (file_size > 0):
            self.latest_log_path = latest_log_path
            data, ratio = get_data(l_bin_file_path)
            self.read_collected.emit(data)
            self.last_call = time.time()
            print(latest_log_path)
        else:
            pass
            # print("|", end='')




# %%

if __name__ == '__main__':
    # tcb_file_path = \
    #     "/home/slovak/topoopt/taichi/outputs/topo_opt/bridge/task-2020-03-17-18-31-06-r09248__v8_r0256/fem/00201.tcb.zip"
    # tcb_file_path = sys.argv[1]
    tcb_log_dir_path = "/home/slovak/topoopt/taichi/outputs/topo_opt"

    app = QtGui.QApplication([])

    viz = Visualizer(tcb_log_dir_path)

    t = QtCore.QTimer()
    t.timeout.connect(viz.emit_data)
    t.start(1000) #QTimer takes ms

    # app.exec_()

    QtGui.QApplication.instance().exec_()

# plt.show()

# %%

exit(0)
# %%

# time ~/openscad/openscad -o /home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-10-03-r06510__v8_r0400/fem/00047.tcb.zip.bin.stl /home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-10-03-r06510__v8_r0400/fem/00047.tcb.zip.bin.scad

/home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-30-22-40-14-r04804__v8_r0400/fem/00044.tcb.zip



# meshlabserver -i /home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-28-22-24-03-r09329__v8_r0256/fem/00192.tcb.zip.bin.stl -o /home/slovak/topoopt/taichi/outputs/topo_opt/test/task-2020-03-28-22-24-03-r09329__v8_r0256/fem/00192.tcb.zip.bin.new2.stl -s /home/slovak/topoopt/taichi/projects/spgrid_topo_opt/scripts/modmesh.mlx
# ~/Downloads/PrusaSlicer-2.2.0+linux-x64-202003211856.AppImage

# cd ../../$(ls ../../ -t | head -1)/fem

