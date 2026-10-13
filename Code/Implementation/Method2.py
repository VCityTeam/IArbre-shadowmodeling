import math
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pdal
import json
from pathlib import Path
import requests
import laspy
from scipy.stats import binned_statistic_2d
from skimage.feature import peak_local_max
from skimage.segmentation import watershed

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Purpose : This program generates a 2.5D urban cast-shadow map and improves the calculation of vegetation shadows.
# Author : Karima Ouadah < ouadkarima@outlook.com >
# Created : June-September 2026
# Description : it takes the coordinates of an area as input, retrieves the corresponding tile from the DataGrandLyon website (LiDAR data), calculates the sun's position for a given date, optimizes the calculation using BVH,
# separates the calculation of vegetation shadows by taking into account only the foliage (the upper third of the tree) and finally generates the shadow map based on the selected time of day.
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def sunpos(latitude_deg, tau_deg, date):
    phi = math.radians(latitude_deg)
    n = date.timetuple().tm_yday
    Delta = (2.0 * math.pi * n) / 365.25
    delta = math.asin(
        0.3978 * math.sin(Delta - 1.4 + 0.0355 * math.sin(Delta - 0.0489))
    )
    omega_ss = math.acos(-math.tan(phi) * math.tan(delta))
    omega_sr = -omega_ss
    tau_omega = math.radians(tau_deg)
    elevations = []
    azimuths = []
    hour_angles = []
    time_list = []
    omega = omega_sr
    while omega <= omega_ss:
        alpha = math.asin(
            math.sin(delta) * math.sin(phi)
            + math.cos(delta) * math.cos(omega) * math.cos(phi)
        )
        cos_alpha = math.cos(alpha)
        value = (
            math.sin(delta) * math.cos(phi)
            - math.cos(delta) * math.cos(omega) * math.sin(phi)
        ) / cos_alpha
        value = max(-1.0, min(1.0, value))
        psi = math.acos(value)
        if omega >= 0:
            psi = 2 * math.pi - psi

        elevations.append(math.degrees(alpha))
        azimuths.append(math.degrees(psi))
        hour_angles.append(math.degrees(omega))

        solar_hour = 12 + math.degrees(omega) / 15
        hours = int(solar_hour)
        minutes = int((solar_hour - hours) * 60)
        time_list.append(f"{hours:02d}:{minutes:02d}")

        omega += tau_omega

    return elevations, azimuths, hour_angles, time_list

def bresenham(x0, y0, x1, y1):
    x0, y0 = int(round(x0)), int(round(y0))
    x1, y1 = int(round(x1)), int(round(y1))

    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    return points

def process_cell(ix, iy, z, alpha, psi, DSM,  shadow):
    if alpha <= 0:
        return

    theta = psi - math.pi

    D = min(z / math.tan(alpha), 2 * max(DSM.shape))

    dx = -D * math.sin(theta)
    dy = -D * math.cos(theta)

    x_top = ix - dx
    y_top = iy - dy

    line = bresenham(ix, iy, x_top, y_top)

    ix = int(ix)
    iy = int(iy)
    z_source = DSM[iy, ix]

    for x, y in line[1:]:

        if (
                x < 0 or x >= DSM.shape[1] or
                y < 0 or y >= DSM.shape[0]
        ):
            continue

        z_cell = DSM[y, x]

        if z_cell == -np.inf:
            continue

        d = np.hypot(x - ix, y - iy)

        if d == 0:
            continue

        beta = math.atan((z_source - z_cell) / d)

        if beta >= alpha:   #
            shadow.append((x, y))

def process_cell_vegetation(ix, iy, z, alpha, psi, DSM,  shadow_vegetation, dsm_canope_top, dsm_canope_bottom, DTM):
    if alpha <= 0:
        return

    theta = psi - math.pi

    D = min(z / math.tan(alpha), 2 * max(DSM.shape))

    dx = -D * math.sin(theta)
    dy = -D * math.cos(theta)

    x_top = ix - dx
    y_top = iy - dy

    line = bresenham(ix, iy, x_top, y_top)

    ix = int(ix)
    iy = int(iy)

    ombre = False

    for x, y in line[1:]:

        if (
                x < 0 or x >= DSM.shape[1] or
                y < 0 or y >= DSM.shape[0]
        ):
            continue

        d = np.hypot(x - ix, y - iy)

        if d == 0:
            continue

        z_canope_source = dsm_canope_top[iy, ix]
        z_canope_ray = z_canope_source - d * math.tan(alpha)
        z_canope_top = dsm_canope_top[y, x]
        z_canope_bottom = dsm_canope_bottom[y, x]

        if not ombre:

            if z_canope_top != -np.inf:

                if z_canope_bottom <= z_canope_ray <= z_canope_top:
                    ombre = True

            continue

        z_sol = DTM[y, x]

        if dsm_canope_top[y, x] != -np.inf:
            continue

        if z_canope_ray <= z_sol:
            shadow_vegetation.append((x, y))

class BVHNode:
    def __init__(self, cells, leaf_size=512):
        self.left = None
        self.right = None
        self.cells = None

        xy = cells[:, :2]

        self.min = xy.min(axis=0)
        self.max = xy.max(axis=0)

        if len(cells) <= leaf_size:
            self.cells = cells
            return

        extent = self.max - self.min
        axis = np.argmax(extent)

        order = np.argsort(cells[:, axis])
        cells = cells[order]

        mid = len(cells) // 2

        self.left = BVHNode(cells[:mid], leaf_size)
        self.right = BVHNode(cells[mid:], leaf_size)

def traverse(node, alpha, psi, DSM, shadow):
    if node is None:
        return

    if node.cells is not None:

        for ix, iy, z in node.cells:

            process_cell(ix, iy, z, alpha, psi, DSM, shadow)

        return

    traverse(node.left, alpha, psi, DSM, shadow)
    traverse(node.right, alpha, psi, DSM, shadow)

def traverse_vegetation(node, alpha, psi, DSM, shadow_vegetation, dsm_canope_top, dsm_canope_bottom, dtm):
    if node is None:
        return

    if node.cells is not None:

        for ix, iy, z in node.cells:

            process_cell_vegetation(ix, iy, z, alpha, psi, DSM, shadow_vegetation, dsm_canope_top, dsm_canope_bottom, dtm)

        return

    traverse_vegetation(node.left, alpha, psi, DSM, shadow_vegetation, dsm_canope_top, dsm_canope_bottom, dtm)
    traverse_vegetation(node.right, alpha, psi, DSM, shadow_vegetation, dsm_canope_top, dsm_canope_bottom, dtm)

def plot_shadow(shadow, time, time_index, x_min, y_min, day, month, year, title):
    if shadow is None:
        print("Error: shadow is None.")
        return

    if shadow.ndim != 2 or shadow.shape[1] < 2:
        print(f"Error: shadow must have shape (N, 2). Current shape : {shadow.shape}")
        print("Too many points; please choose a different classification or time of day.")
        return

    if len(shadow) == 0:
        print("No points to display.")
        return

    if shadow.size == 0:
        print("No points to display.")
        return

    plt.figure(figsize=(12, 12))

    plt.scatter(
        shadow[:, 0],
        shadow[:, 1],
        alpha=1,
        s=0.2,
        c="black",
        label="Projection"
    )

    plt.axis("equal")
    plt.legend()
    plt.title(f"{title}\nX_min : {x_min} Y_min : {y_min}\nPeriod : {time_index} Hour : {time[time_index]}\nDate : {day}-{month}-{year}")
    print("plot ready")
    plt.show()

def load_point_cloud(filename, classification_choice):
    if classification_choice == 1:
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [filename]
        }))

    if classification_choice == 2:
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 3 || Classification == 4 || Classification == 5",
                }
            ]
        }))

    if classification_choice == 3:
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 3 || Classification == 4 || Classification == 5 || Classification == 8",
                }
            ]
        }))

    if classification_choice == 4:
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 6",
                }
            ]
        }))

    if classification_choice == 5:
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification != 3 && Classification != 4 && Classification != 5 && Classification != 8",
                }
            ]
        }))

    pipeline.execute()
    arrays = pipeline.arrays[0]
    points = np.vstack((arrays['X'], arrays['Y'], arrays['Z'], arrays['Classification'])).transpose()
    return points

def build_dsm(points, resolution=1.0):
    print("begin building DSM")
    xmin, ymin = points[:, 0].min(), points[:, 1].min()
    xmax, ymax = points[:, 0].max(), points[:, 1].max()
    nx = int((xmax - xmin) / resolution) + 1
    ny = int((ymax - ymin) / resolution) + 1

    DSM = np.full((ny, nx), -np.inf)

    for x, y, z, _ in points:
        ix = int((x - xmin) / resolution)
        iy = int((y - ymin) / resolution)

        DSM[iy, ix] = max(DSM[iy, ix], z)

    return DSM, xmin, ymin, resolution

def dsm_to_cells(DSM):
    cells = []

    for iy in range(DSM.shape[0]):
        for ix in range(DSM.shape[1]):

            z = DSM[iy, ix]

            if z > -np.inf:
                cells.append([ix, iy, z])

    return np.asarray(cells)

def user_sun_phase_choice(alpha_list, horaire_list):
    if alpha_list[0] <= 0:
        start_index = 1
    else:
        start_index = 0

    while True:
        print("\nPlease choose a phase of the day (from sunrise to sunset):\n")

        for i in range(start_index, len(alpha_list)):
            print(f"{i} : {horaire_list[i]}")

        user_time_index = input("\nEnter the index of the desired time: ")

        if user_time_index.isdigit():
            user_time_index = int(user_time_index)

            if start_index <= user_time_index < len(alpha_list):
                return user_time_index

        print(f"Invalid entry. Please enter a number between {start_index} and {len(alpha_list)-1}.")

def user_date_choice():
    while True:
        day = input("Please enter the day : ")
        month = input("Please enter the month : ")
        year = input("Please enter the year : ")
        print("\n")

        try:
            date = datetime(int(year), int(month), int(day))
            return date.year, date.month, date.day
        except ValueError:
            print("Invalid date. Please try again.")

def user_entry_data():
    user_x_min = input("Please enter x min: ")
    user_y_min = input("Please enter y min: ")

    return user_x_min, user_y_min

def user_laz_api(url_api, user_x_min, user_y_min):
    answer = requests.get(url_api)
    data = answer.json()

    for value in data["values"]:
        if value["x_min"] == int(user_x_min) and value["y_min"] == int(user_y_min):
            url = value["url"].strip()
            break
    else:
        raise ValueError("Tile not found")

    r = requests.get(url)
    r.raise_for_status()

    output_dir = Path("Data")
    output_dir.mkdir(exist_ok=True)
    filename = output_dir / f"tile_{user_x_min}_{user_y_min}.laz"

    with open(filename, "wb") as f:
        f.write(r.content)

    return str(filename)

def capone_laz_generate (laz_file) :

    las=laspy.read(laz_file)

    x = np.asarray(las.x)
    y = np.asarray(las.y)
    z = np.asarray(las.z)
    cls = las.classification
    ground = cls == 2

    x_ground = x[ground]
    y_ground = y[ground]
    z_ground = z[ground]
    trees = np.isin(cls, [3, 4, 5, 8])

    x_tree = x[trees]
    y_tree = y[trees]
    z_tree = z[trees]
    resolution = 1.0

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
            np.arange(xmin, xmax + resolution, resolution),
            np.arange(ymin, ymax + resolution, resolution)
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
            np.arange(xmin, xmax + resolution, resolution),
            np.arange(ymin, ymax + resolution, resolution)
        ]
    )

    dsm = dsm.T
    dtm = dtm.T

    dsm = np.nan_to_num(dsm, nan=0)
    dtm = np.nan_to_num(dtm, nan=np.nanmedian(dtm))

    chm = dsm - dtm

    dsm_top, _, _, _ = binned_statistic_2d(
        x_tree,
        y_tree,
        z_tree,
        statistic="max",
        bins=[
            np.arange(xmin, xmax + resolution, resolution),
            np.arange(ymin, ymax + resolution, resolution)
        ]
    )

    dsm_bottom, _, _, _ = binned_statistic_2d(
        x_tree,
        y_tree,
        z_tree,
        statistic="min",
        bins=[
            np.arange(xmin, xmax + resolution, resolution),
            np.arange(ymin, ymax + resolution, resolution)
        ]
    )

    dsm_top = dsm_top.T
    dsm_bottom = dsm_bottom.T
    dsm_top = np.nan_to_num(dsm_top, nan=-np.inf)
    dsm_bottom = np.nan_to_num(dsm_bottom, nan=np.inf)

#
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

    row = np.clip(row, 0, labels.shape[0] - 1)
    col = np.clip(col, 0, labels.shape[1] - 1)
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

        seuil = 0.66 * hmax

        keep[pts] = height[pts] >= seuil

    new_las = laspy.LasData(las.header)
    new_las.points = las.points[trees][keep]

    x_keep = x_tree[keep]
    y_keep = y_tree[keep]
    z_keep = z_tree[keep]

    dsm_filtered, _, _, _ = binned_statistic_2d(
        x_keep,
        y_keep,
        z_keep,
        statistic="max",
        bins=[
            np.arange(xmin, xmax + resolution, resolution),
            np.arange(ymin, ymax + resolution, resolution)
        ]
    )

    dsm_filtered = dsm_filtered.T
    dsm_filtered = np.nan_to_num(dsm_filtered, nan=0)

    chm_filtered = dsm_filtered - dtm
    chm_filtered[chm_filtered < 0] = 0

    output_file = "Data/canopeetest2.laz"
    new_las.write(output_file)

    return output_file, dsm_top, dsm_bottom, chm_filtered, dtm

def main():
    url = "https://data.grandlyon.com/fr/datapusher/ws/grandlyon/ima_gestion_images.imamnt2023laz500mcc46/all.json?maxfeatures=-1&start=1&filename=nuage-de-points-lidar-2023-de-la-metropole-de-lyon"

    year, month, day = user_date_choice()
    date = datetime(year, month, day)
    x_min, y_min = user_entry_data()
    laz_file = user_laz_api(url, x_min, y_min)

    canope_laz, dsm_canope_top, dsm_canope_bottom, chm, dtm = capone_laz_generate(laz_file)

    points = load_point_cloud(laz_file, 5)
    DSM, xmin, ymin, resolution = build_dsm(points)
    cells = dsm_to_cells(DSM)
    bvh = BVHNode(cells)

    alpha_list, psi_list, omega, time = sunpos(
        latitude_deg=45.75,
        tau_deg= 45,
        date=date
    )

    time_index = user_sun_phase_choice(alpha_list, time)

    print("\nValeurs :")
    print("elevation value :", alpha_list[time_index])
    print("azimuth value :", psi_list[time_index])
    print("hour angle value :", omega[time_index])
    print("\n")

    alpha = math.radians(alpha_list[time_index])
    psi = math.radians(psi_list[time_index])
    shadow = []

    traverse(
        bvh,
        alpha,
        psi,
        DSM,
        shadow
    )

    shadow = np.asarray(shadow)
    cells_vegetation_2 = dsm_to_cells(chm)
    bvh_vegetation_2 = BVHNode(cells_vegetation_2)
    shadow_vegetation = []
    traverse_vegetation(
        bvh_vegetation_2,
        alpha,
        psi,
        chm,
        shadow_vegetation,
        dsm_canope_top,
        dsm_canope_bottom,
        dtm

    )

    shadow_vegetation = np.asarray(shadow_vegetation)

    shadow_all = np.unique(
        np.concatenate((shadow, shadow_vegetation), axis=0),
        axis=0
    )

    plot_shadow(shadow, time, time_index, x_min, y_min, day, month, year, "Method 2 Vegetation-free Shadow Map")
    plot_shadow(shadow_vegetation, time, time_index, x_min, y_min, day, month, year, "Method 2 Shadow Map with vegetation")
    plot_shadow(shadow_all, time, time_index, x_min, y_min, day, month, year, "Method 2 Global Shadow Map")

if __name__ == "__main__":
    main()
