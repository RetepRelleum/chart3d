## Chart3d  

Python package to create from a numpy Array a 3d triangle Chart like 
https://skfb.ly/osJAz


```{python}
import chart3d as c3d
from chart3d import EnumColor

_date=datetime.now()-timedelta(366)
pointMatrix = None

for x in range(366):
    ay = np.array(_date)
    for y in range(25):
        ay=np.append(ay,random()*15+3)
    if pointMatrix is None:
        pointMatrix=np.array([ay])
    else:
        pointMatrix=np.append(pointMatrix,[ay],axis=0)
    _date = _date + timedelta(1)

pointMatrix2 = np.array([[datetime.now()-timedelta(-2),1, 2, 3, 4, 5, 6, 7, 8, 9],
                        [datetime.now()-timedelta(-1),5, 5, 5, 5, 5, 5, 5, 5, 5],
                        [datetime.now()-timedelta(-0),9, 8, 7, 6, 5, 4, 3, 2, 1]])


vertices, vcolors, triangles = c3d.matrix_to_vertices_quader(pointMatrix,
                                                             colx=EnumColor.r2b,
                                                             xlabel='Stunde',
                                                             ylabel='Tage',
                                                             zlabel='kW',
                                                             ueber='Random Test')
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(vertices)
vertices1, vcolors1, triangles1 = c3d.matrix_to_vertices(pointMatrix2,dxyz=c3d.Point(0,24+10,0))
pcd1 = o3d.geometry.PointCloud()
pcd1.points = o3d.utility.Vector3dVector(vertices1)
o3d.visualization.draw_geometries([pcd,pcd1])

mesh = o3d.geometry.TriangleMesh()
mesh.vertices = o3d.utility.Vector3dVector(vertices)
mesh.triangles = o3d.utility.Vector3iVector(triangles)
mesh.vertex_colors = o3d.utility.Vector3dVector(vcolors)
mesh.compute_vertex_normals()

mesh1 = o3d.geometry.TriangleMesh()
mesh1.vertices = o3d.utility.Vector3dVector(vertices1)
mesh1.triangles = o3d.utility.Vector3iVector(triangles1)
mesh1.vertex_colors = o3d.utility.Vector3dVector(vcolors1)
mesh1.compute_vertex_normals()

o3d.visualization.draw_geometries([mesh,mesh1], mesh_show_wireframe=False)
#o3d.io.write_triangle_mesh("copy_of_knot_pv00.ply", mesh)
```