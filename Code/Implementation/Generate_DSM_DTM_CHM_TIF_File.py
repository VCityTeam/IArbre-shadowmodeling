import laspy
import numpy as np
import rasterio
from rasterio.transform import from_bounds
from scipy.spatial import cKDTree

# https://gist.github.com/krishnaglodha/66a32ba4cc65aceaf7bd83986305f12d#file-terrain-from-las-py

mycrs = 'EPSG:26985'
las_file = 'Data/tile_1853500_5180500.laz'
# 1. Read Bounds from LAZ File
def read_laz_bounds(filename):
    las = laspy.read(filename)
    min_x, min_y = las.x.min(), las.y.min()
    max_x, max_y = las.x.max(), las.y.max()
    print(f"Bounds from {filename}:")
    print(f"Min X: {min_x}, Min Y: {min_y}")
    print(f"Max X: {max_x}, Max Y: {max_y}")
    return min_x, min_y, max_x, max_y,las

# 2. Create Grid
def create_grid_from_bounds(min_x, min_y, max_x, max_y, resolution=0.1):
    x = np.arange(min_x, max_x, resolution)
    y = np.arange(min_y, max_y, resolution)
    return np.meshgrid(x, y)

# Interpolate Points to Grid
def interpolate_points(x, y, z, grid_x, grid_y, method="nearest"):
    points = np.column_stack((x, y))
    grid_shape = grid_x.shape
    flat_grid_points = np.column_stack((grid_x.ravel(), grid_y.ravel()))

    # Convert point cloud Z to a NumPy array
    z = np.asarray(z, dtype=np.float32)

    # Perform nearest-neighbor interpolation
    tree = cKDTree(points)
    _, idx = tree.query(flat_grid_points)

    # Ensure correct reshaping
    interpolated_z = z[idx].reshape(grid_shape)
    return interpolated_z

# Save Raster
def save_raster(filename, x, y, data, crs):
    # Ensure the x and y are 1D arrays for bounds calculation
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()

    # Correct transform creation for saving raster (bottom-left origin)
    transform = from_bounds(x_min, y_max, x_max, y_min, data.shape[1], data.shape[0])
    data = np.flipud(data)

    # Save raster
    with rasterio.open(
        filename, "w",
        driver="GTiff",
        height=data.shape[0], width=data.shape[1],
        count=1, dtype=data.dtype,
        crs=crs, transform=transform
    ) as dst:
        dst.write(data, 1)

#Calculate CHM
def filter_chm(dsm, dtm, min_height):
    chm = dsm - dtm
    mask = chm >= min_height
    return np.where(mask, chm, np.nan)


# Read LAZ Data
min_x, min_y, max_x, max_y,las = read_laz_bounds(las_file)
# Create Grid
grid_x, grid_y = create_grid_from_bounds(min_x, min_y, max_x, max_y, resolution=0.1)
# Filter Points for DSM and DTM
ground_points = (las.classification == 2) | (las.classification == 9)  # Ground points (DTM)
non_ground_points = ~ground_points  # Non-ground points (DSM)
# Generate DSM and DTM
dsm_z = interpolate_points(las.x[non_ground_points], las.y[non_ground_points], las.z[non_ground_points], grid_x, grid_y)
dtm_z = interpolate_points(las.x[ground_points], las.y[ground_points], las.z[ground_points], grid_x, grid_y)

save_raster("dsm.tif", grid_x, grid_y, dsm_z,mycrs)
save_raster("dtm.tif", grid_x, grid_y, dtm_z,mycrs)

# calculate CHM
chm_z = filter_chm(dsm_z, dtm_z, min_height=10)

save_raster("chm.tif", grid_x, grid_y, chm_z,mycrs)
