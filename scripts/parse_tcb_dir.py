#!/usr/bin/env python3

import sys
import os
import fnmatch
import time

import subprocess as sp
import numpy as np

import PyQt5
import pyqtgraph as pg
pg.setConfigOption('background', 'k')
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl

# #%%gui qt
# from IPython import get_ipython
# ipython = get_ipython()
# if ipython is not None:
#     ipython.magic("gui qt")
#     tcb_file_path = "/home/slovak/Downloads/00145.tcb.zip"
    # tcb_file_path = \
    #     "/home/slovak/topoopt/taichi/outputs/topo_opt/bridge/task-2020-03-11-10-30-51-r01108__v8_r0256/fem/00034.tcb.zip"
# else:


def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

ress = set()

while True:
    res = find('*.tcb.zip', sys.argv[1])
    diff = set(res).difference(ress)
    if len(diff) > 0:
        last = sorted(diff)[-1]
        print(last)
    ress = set(res)
    time.sleep(2)

tcb_file_path = sys.argv[1]

csv_file_path = tcb_file_path + ".csv"
bin_file_path = tcb_file_path + ".bin"

if not os.path.isfile(bin_file_path):
    sp.call(["ti", "run", "fem_to_dict", tcb_file_path])

# voxels = np.genfromtxt(csv_file_path, delimiter=',')

voxels_bin = np.fromfile(bin_file_path, dtype=np.float32)
voxels_bin = voxels_bin.reshape((-1, 4))


voxels = voxels_bin

voxels[:, 0] = voxels[:, 0] - voxels[:, 0].min()
voxels[:, 1] = voxels[:, 1] - voxels[:, 1].min()
voxels[:, 2] = voxels[:, 2] - voxels[:, 2].min()

shape = (
    voxels[:, 0].max().astype(int) + 1,
    voxels[:, 1].max().astype(int) + 1,
    voxels[:, 2].max().astype(int) + 1)

d2 = np.zeros(
    shape + (4,)
    , dtype=np.ubyte
)

# for row in voxels:
#     d2[row[0].astype(int), row[1].astype(int), row[2].astype(int), 0] = int(row[3]*255)

voxels[:, 3] = voxels[:, 3] * 255

voxelsint = voxels.astype(np.ubyte)

d2[voxelsint[:, 0], voxelsint[:, 1], voxelsint[:, 2], 0] = voxelsint[:, 3]

#
# for row in voxelsint:
#     d2[row[0], row[1], row[2], 0] = row[3]

d2[..., 2] = d2[..., 0]
d2[..., 3] = d2[..., 0]
d2[..., 3] = (d2[..., 3].astype(float) / 255.)**2 * 255



app = QtGui.QApplication([])

view = gl.GLViewWidget()
# view.show()

# xgrid = gl.GLGridItem()
# view.addItem(xgrid)

# view.addItem(gl.GLAxisItem())

v = gl.GLVolumeItem(d2, smooth=True)
v.translate(-shape[0]/2, -shape[1]/2, -shape[2]/2)
view.addItem(v)

view.opts = \
{'azimuth': 22,
 'bgcolor': (0.0, 0.0, 0.0, 1.0),
 'center': PyQt5.QtGui.QVector3D(0.0, 0.0, 0.0),
 'distance': 398.6759281410123,
 'elevation': 18.0,
 'fov': 60,
 'viewport': None}

view.update()

# view.showMaximized()

d = view.renderToArray((1920, 1080))
image_file_path = tcb_file_path + ".png"
pg.makeQImage(d, alpha=False).save(image_file_path)

print(image_file_path)

# Start Qt event loop unless running in interactive mode.
# if __name__ == '__main__':
#     import sys
#     if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#         QtGui.QApplication.instance().exec_()


# %%import pyinotify
#
# class ModHandler(pyinotify.ProcessEvent):
#     # evt has useful properties, including pathname
#     def process_IN_CLOSE_WRITE(self, evt):
#             webbrowser.open(URL)
#
# handler = ModHandler()
# wm = pyinotify.WatchManager()
# notifier = pyinotify.Notifier(wm, handler)
# wdd = wm.add_watch(FILE, pyinotify.IN_CLOSE_WRITE)
# notifier.loop()
