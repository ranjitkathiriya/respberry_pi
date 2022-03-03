import open3d as o3d
import numpy as np

pcd = o3d.io.read_triangle_mesh("save_28_02_2022-03:13:48_PM_100.ply")


print(pcd)

o3d.io.write_triangle_mesh("copy_of_knot.off", pcd)