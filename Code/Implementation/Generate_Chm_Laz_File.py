import laspy
import numpy as np
from skimage.feature import peak_local_max
from skimage.segmentation import watershed
from scipy.stats import binned_statistic_2d


las = laspy.read("Data/tile_1853500_5180500.laz")

x = np.asarray(las.x)
y = np.asarray(las.y)
z = np.asarray(las.z)
cls = las.classification
ground = cls == 2

x_ground = x[ground]
y_ground = y[ground]
z_ground = z[ground]
trees = np.isin(cls, [3,4,5,8])

x_tree = x[trees]
y_tree = y[trees]
z_tree = z[trees]
resolution = 0.5

xmin = x.min()
xmax = x.max()

ymin = y.min()
ymax = y.max()

gx = np.arange(xmin, xmax, resolution)
gy = np.arange(ymin, ymax, resolution)

grid_x, grid_y = np.meshgrid(gx, gy)
from scipy.spatial import cKDTree

tree_ground = cKDTree(
    np.column_stack((x_ground, y_ground))
)

_, idx = tree_ground.query(
    np.column_stack((grid_x.ravel(), grid_y.ravel()))
)

dtm, _, _, _ = binned_statistic_2d(
    x_ground,
    y_ground,
    z_ground,
    statistic="min",
    bins=[
        np.arange(xmin, xmax+resolution, resolution),
        np.arange(ymin, ymax+resolution, resolution)
    ]
)
tree_canopy = cKDTree(
    np.column_stack((x_tree, y_tree))
)

_, idx = tree_canopy.query(
    np.column_stack((grid_x.ravel(), grid_y.ravel()))
)

dsm, _, _, _ = binned_statistic_2d(
    x_tree,
    y_tree,
    z_tree,
    statistic="max",
    bins=[
        np.arange(xmin, xmax+resolution, resolution),
        np.arange(ymin, ymax+resolution, resolution)
    ]
)

dsm = dsm.T
dtm = dtm.T

dsm = np.nan_to_num(dsm, nan=0)
dtm = np.nan_to_num(dtm, nan=np.nanmedian(dtm))

chm = dsm - dtm

chm[chm < 0] = 0

tops = peak_local_max(
    chm,
    min_distance=8,
    threshold_abs=2
)

markers = np.zeros(chm.shape, dtype=np.int32)

for i, (r, c) in enumerate(tops):
    markers[r, c] = i + 1

labels = watershed(
    -chm,
    markers,
    mask=chm > 0
)

col = ((x_tree - xmin) / resolution).astype(int)
row = ((y_tree - ymin) / resolution).astype(int)

row = np.clip(row, 0, labels.shape[0]-1)
col = np.clip(col, 0, labels.shape[1]-1)
tree_id = labels[row, col]
_, idx = tree_ground.query(
    np.column_stack((x_tree, y_tree))
)

ground_z = z_ground[idx]

height = z_tree - ground_z
keep = np.zeros(len(z_tree), dtype=bool)
for tree in np.unique(tree_id):

    if tree == 0:
        continue

    pts = tree_id == tree

    hmax = height[pts].max()

    seuil = 0.70 * hmax

    keep[pts] = height[pts] >= seuil

new_las = laspy.LasData(las.header)
new_las.points = las.points[trees][keep]

new_las.write("canopeetest3.laz")
