

file_path = "/home/slovak/topoopt/taichi/outputs/topo_opt/bridge/task-2020-03-08-23-45-35-r09094__v8_r0256/fem/00999.tcb.zip.csv"

import numpy as np

# %gui qt
from IPython import get_ipython
ipython = get_ipython()
ipython.magic("gui qt")

import pyqtgraph as pg
pg.mkQApp()

import pyqtgraph.opengl as gl

view = gl.GLViewWidget()
view.show()

xgrid = gl.GLGridItem()
view.addItem(xgrid)

view.addItem(gl.GLAxisItem())

sp1 = gl.GLScatterPlotItem(pos=np.ones(shape=(100, 3)), pxMode=True)
view.addItem(sp1)

# %%

voxels = np.genfromtxt(file_path, delimiter=',')

voxels = voxels[voxels[:, 3] > 0.5, :]

voxels[:, 0] = voxels[:, 0] - (np.max(voxels[:, 0]) + np.min(voxels[:, 0]))/2.0
voxels[:, 1] = voxels[:, 1] - (np.max(voxels[:, 1]) + np.min(voxels[:, 1]))/2.0
voxels[:, 2] = voxels[:, 2] - (np.max(voxels[:, 2]) + np.min(voxels[:, 2]))/2.0

sp1.setData(pos=voxels[:, 0:3])
sp1.setData(size=voxels[:, 3]*10)
# sp1.setData(color=col)
sp1.setData(pxMode=True)

view.update()
