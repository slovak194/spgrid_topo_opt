from topo_opt import TopoOpt
import taichi as tc

version = 8
wireframe = False
narrow_band = True
plane_force = True
volume_fraction = 0.2

use_mirror = False

# Initialize
n = 256
#tc.core.set_core_trigger_gdb_when_crash(True);
opt = TopoOpt(res=(n, n, n), version=version,
              volume_fraction=volume_fraction,
              grid_update_start=5 if narrow_band else 1000000,
              progressive_vol_frac=5, cg_tolerance=1e-3,
              minimum_stiffness=0, minimum_density=1e-2,
              fix_cells_at_dirichlet=False,
              fix_cells_near_force=True,
              connectivity_filtering=True,
              adaptive_min_fraction=False,
              verbose_snapshot=False,
              fixed_cell_density=1
              )

k = 1

x, y, z = 1*k, 1*k, 1*k


if use_mirror:
    mirror = 'xy'
else:
    mirror = ''


opt.populate_grid(domain_type='box', size=(x, y, z), mirror=mirror)
# opt.populate_grid(domain_type='cylinder', radius=rad, thickness=rad/2, height=rad*1)

# opt.populate_grid(domain_type='box', size=(x, y, z), mirror=mirror)


# opt.add_load(center=(x, y, z), force=(0,  0,  -8), size=0.01)
# opt.add_load(center=(-x, y, z), force=(0,  0,  -8), size=0.01)
# opt.add_load(center=(x, -y, z), force=(0,  0,  -8), size=0.01)
# opt.add_load(center=(-x, -y, z), force=(0,  0,  -8), size=0.01)
#
#
# opt.add_load(center=(0, 0, 0), force=(0,  0,  -5), size=0.01)
# opt.add_load(center=(-x/2, y/2, z), force=(0,  0,  -8), size=0.01)
# opt.add_load(center=(x/2, -y/2, z), force=(0,  0,  -8), size=0.01)
# opt.add_load(center=(-x/2, -y/2, z), force=(0,  0,  -8), size=0.01)

# opt.add_load(center=(x, 0, z-0.01), force=(0,  5,  -10), size=0.02)
# opt.add_load(center=(0, y, z-0.01), force=(5,  0,  -10), size=0.02)
# opt.add_load(center=(-x, 0, z-0.01), force=(0,  -5,  -10), size=0.02)
# opt.add_load(center=(0, -y, z-0.01), force=(-5,  0,  -10), size=0.02)

# opt.add_load(center=(x, 0, z), force=(0,  0,  -10), size=0.01)
# opt.add_plane_load(force=(-10, 0, 0), axis=2, extreme=1)
# opt.add_plane_load(force=(-10, 0, 0), axis=0, extreme=1)
# opt.add_plane_load(force=(10, 0, 0), axis=0, extreme=-1)
# opt.add_plane_load(force=(0, -10, 0), axis=1, extreme=1)
# opt.add_plane_load(force=(0, 10, 0), axis=1, extreme=-1)
# opt.add_plane_load(force=(0, 0, -10), axis=2, extreme=1)
# opt.add_plane_load(force=(0, 0, 1), axis=2, extreme=-1)
# opt.add_plane_load(force=(0, 0, 10), axis=2, extreme=-1)
# opt.add_plane_load(force=(10, 0, 0), axis=1, extreme=-1)

# opt.add_load(center=(0, 0, 0), force=(0,  -10,  0), size=0.01)

# rod_size = 0.01


# opt.add_load(center=(-x, 0, z), force=(0,  0,  -10), size=0.01)
# opt.add_load(center=(0, -y, z), force=(0,  0,  -10), size=0.01)

# opt.add_plane_load(force=(0, 0, -10), axis=2, extreme=1)

# opt.add_load(center=(0, y, z), force=(0,  -10,  0), size=0.01)
# opt.add_load(center=(-x/4, y, z/2), force=(0,  -10,  0), size=0.01)
# opt.add_load(center=(-x/2, y, 0), force=(0,  -10,  0), size=0.01)
# opt.add_load(center=(-2*x/3, y, -z/2), force=(0,  -10,  0), size=0.01)


# opt.add_load(center=(-x, y, z), force=(0,  -10,  0), size=0.01)


# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=1, extreme=1)
# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=1, extreme=-1)

# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(x, y, -z), bound1=(x-rod_size, y-rod_size, z))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(-x, y, -z), bound1=(-x+rod_size, y-rod_size, z))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(x, -y, -z), bound1=(x-rod_size, -y+rod_size, z))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(-x, -y, -z), bound1=(-x+rod_size, -y+rod_size, z))

#

# opt.add_dirichlet_bc((x, y, -z), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((-x, y, -z), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((x, -y, -z), radius=0.01, axis='xyz', value=(0, 0, 0))



opt.add_dirichlet_bc((0.84075976, -0.08940331, 0.02817660), radius=0.01, axis='xyz', value=(0, 0, 0))

opt.add_load(center=(0.84054296, -0.05227500, 0.00000000), force=(0,  -10,  0), size=0.01)
opt.add_load(center=(0.80227500, -0.09054296, 0.00000000), force=(0,  -10,  0), size=0.01)


# rod_size = 0.01
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='z', bound0=(x-rod_size, y-rod_size, -z), bound1=(x, y, -z+rod_size))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='z', bound0=(-x, y-rod_size, -z), bound1=(-x+rod_size, y, -z+rod_size))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='z', bound0=(x-rod_size, -y, -z), bound1=(x, -y+rod_size, -z+rod_size))
# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(-x, -y, -z), bound1=(-x+rod_size, -y+rod_size, -z+rod_size))

# opt.general_action(action='add_box_dirichlet_bc', axis_to_fix='xyz', bound0=(-rod_size, -rod_size, -z), bound1=(rod_size, rod_size, -z+rod_size))

# opt.add_dirichlet_bc((-x, -y, -z), radius=0.01, axis='xyz', value=(0, 0, 0))


# opt.add_dirichlet_bc((-x, 0, -z), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((0, -y, -z), radius=0.01, axis='xyz', value=(0, 0, 0))

# opt.add_dirichlet_bc((x, y, 0), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((-x, y, 0), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((x, -y, 0), radius=0.01, axis='xyz', value=(0, 0, 0))
# opt.add_dirichlet_bc((-x, -y, 0), radius=0.01, axis='xyz', value=(0, 0, 0))

# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=2, extreme=-1)
# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=0, extreme=1)
# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=0, extreme=-1)
# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=1, extreme=1)

# opt.add_dirichlet_bc((0, 0, 0), radius=0.05, axis='xyz', value=(0, 0, 0))

# opt.add_dirichlet_bc((0, 0, -z), radius=0.01, axis='xyz', value=(0, 0, 0))

# opt.add_plane_dirichlet_bc(axis_to_fix="xyz", axis_to_search=2, extreme=-1)
# opt.add_dirichlet_bc((0, 0, -z), radius=0.01, axis='xyz', value=(0, 0, 0))


# Optimize
opt.run()
