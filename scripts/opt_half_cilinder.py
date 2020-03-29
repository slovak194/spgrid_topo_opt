from topo_opt import TopoOpt
import taichi as tc

# import crash_report
# crash_report.enable()

version = 10
narrow_band = True
volume_fraction = 0.2
# Initialize
n = 128
opt = TopoOpt(res=(n, n, n), version=version, volume_fraction=volume_fraction,
              grid_update_start=2 if narrow_band else 1000000,
              fix_cells_at_dirichlet=True,
              fix_cells_near_force=True,
              progressive_vol_frac=0, fixed_cell_density=0.3,
            #   minimum_stiffness=0, minimum_density=1e-2,
            #   connectivity_filtering=True,
              cg_max_iterations=100)


# obj_file_path = '/home/slovak/topoopt/taichi/projects/spgrid_topo_opt/data/wing_2.obj'
# obj_file_path = '/home/slovak/topoopt/taichi/projects/spgrid_topo_opt/data/Halfcilinder.obj'
# obj_file_path = '/home/slovak/topoopt/taichi/projects/spgrid_topo_opt/data/HalfcilinderThin.obj'
# obj_file_path = '/home/slovak/topoopt/taichi/projects/spgrid_topo_opt/data/HalfcilinderMiddle.obj'
obj_file_path = '/home/slovak/topoopt/taichi/projects/spgrid_topo_opt/data/Cube.obj'




s = 1
tex = tc.Texture(
    'mesh',
    translate=(0.5, 0.5, 0.5),
    scale=(s, s, s),
    adaptive=False,
    filename=obj_file_path)

s *= 0.95
tex_shell = tc.Texture(
    'mesh',
    translate=(0.5, 0.5, 0.5),
    scale=(s, s, s),
    adaptive=False,
    filename=obj_file_path)

opt.populate_grid(domain_type='texture', tex_id=tex.id)
# opt.general_action(action='make_shell', tex_id=tex_shell.id)
opt.general_action(action='voxel_connectivity_filtering')

# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(-0.01, -0.01+0.09, -0.025), bound1=(0.01, 0.01+0.09, 0.025))

opt.add_dirichlet_bc((0, 0, 0), radius=0.02, axis='xyz', value=(0, 0, 0))

# opt.add_dirichlet_bc((0, 0.0654, 0), radius=0.02, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((0, 0.0654, -0.3345/2), radius=0.02, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((0, 0.0654, 0.3345/2), radius=0.02, axis='xyz', value=(0, 0, 0))

# opt.add_dirichlet_bc((0.15, 0.1, -0.4), radius=0.02, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((0.15, 0.1,  0.4), radius=0.02, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((-0.15, 0.1, -0.4), radius=0.02, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((-0.15, 0.1,  0.4), radius=0.02, axis='xyz', value=(0, 0, 0))

# opt.add_plane_load(force=(0, 0, -10), axis=2, extreme=1)
# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=2, extreme=-1)

opt.general_action(action='add_mesh_normal_force', mesh_fn=obj_file_path, magnitude=-1, center=(0, 0, 0), falloff=3000, maximum_distance=0.005)


# Optimize
opt.run()

# %%


# time ~/openscad/openscad -o /home/slovak/topoopt/taichi/outputs/topo_opt/plane_wing/task-2020-03-19-21-01-25-r00644__v10_r0320/fem/00023.tcb.zip.bin.scad.stl /home/slovak/topoopt/taichi/outputs/topo_opt/plane_wing/task-2020-03-19-21-01-25-r00644__v10_r0320/fem/00023.tcb.zip.bin.scad
