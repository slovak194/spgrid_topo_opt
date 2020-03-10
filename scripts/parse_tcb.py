#!/usr/bin/env python3

import subprocess as sp
import numpy as np

import pyqtgraph as pg
import pyqtgraph.opengl as gl

#%%gui qt
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("gui qt")


tcb_file_path = "/home/slovak/Downloads/00023.tcb.zip"
file_path = tcb_file_path + ".csv"


pg.mkQApp()

view = gl.GLViewWidget()
view.show()

xgrid = gl.GLGridItem()
view.addItem(xgrid)

view.addItem(gl.GLAxisItem())


# sp1 = gl.GLScatterPlotItem(pos=np.ones(shape=(100, 3)), pxMode=True)
# view.addItem(sp1)


# sp.call(["ti", "run", "fem_to_dict", tcb_file_path])


# voxels = np.genfromtxt(file_path, delimiter=',')
#
# # voxels = voxels[voxels[:, 3] > 0.5, :]
#
# # voxels[:, 0] = voxels[:, 0] - (np.max(voxels[:, 0]) + np.min(voxels[:, 0]))/2.0
# # voxels[:, 1] = voxels[:, 1] - (np.max(voxels[:, 1]) + np.min(voxels[:, 1]))/2.0
# # voxels[:, 2] = voxels[:, 2] - (np.max(voxels[:, 2]) + np.min(voxels[:, 2]))/2.0
#
# sp1.setData(pos=voxels[:, 0:3])
# sp1.setData(size=voxels[:, 3]*2)
# # sp1.setData(color=col)
# sp1.setData(pxMode=True)
#
# view.update()
#

voxels = np.genfromtxt(file_path, delimiter=',')

# voxels = voxels[voxels[:, 3] > 0.5, :]

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

for row in voxels:
    d2[row[0].astype(int), row[1].astype(int), row[2].astype(int), 0] = int(row[3]*255)

d2[..., 2] = d2[..., 0]
d2[..., 3] = d2[..., 0]
d2[..., 3] = (d2[..., 3].astype(float) / 255.)**2 * 255


v = gl.GLVolumeItem(d2)
v.translate(-shape[0]/2, -shape[1]/2, -shape[2]/2)
view.addItem(v)
view.update()
