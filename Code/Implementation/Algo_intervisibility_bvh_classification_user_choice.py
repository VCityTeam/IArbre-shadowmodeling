import math
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pdal
import json

"""
Step:
- User selection of classifications and date to use
- Load point clouds
- Create a Digital Surface Model
- Convert the Digital Surface Model into cells
- Bresenham (grid cell traversed by the ray)
- BVH on the cells
- Calculate sun position
- Traverse using BVH
- Process cell (calculate shadow)
- Display shadow

Result: good

Author : Karima Ouadah
"""

# [Position du soleil](https://www.mdpi.com/2220-9964/10/9/583)
def sunpos(latitude_deg, tau_deg, date):
    print("begin sunpos")
    # latitude -> radians
    phi = math.radians(latitude_deg)
    # Jour de l'année
    n = date.timetuple().tm_yday
    Delta = (2.0 * math.pi * n) / 365.25
    # déclinaison solaire
    delta = math.asin(
        0.3978 * math.sin(Delta - 1.4 + 0.0355 * math.sin(Delta - 0.0489))
    )
    # angle horaire du coucher
    omega_ss = math.acos(-math.tan(phi) * math.tan(delta))
    # angle horaire du lever
    omega_sr = -omega_ss
    # incrément
    tau_omega = math.radians(tau_deg)
    elevations = []
    azimuths = []
    hour_angles = []
    omega = omega_sr
    while omega <= omega_ss:
        # élévation
        alpha = math.asin(
            math.sin(delta) * math.sin(phi)
            + math.cos(delta) * math.cos(omega) * math.cos(phi)
        )
        # azimut
        cos_alpha = math.cos(alpha)
        # Protection contre les erreurs numériques
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

        omega += tau_omega

    return elevations, azimuths, hour_angles

def grille(points   ):
# Grille
    xmin = points[:,0].min()
    xmax = points[:,0].max()

    ymin = points[:,1].min()
    ymax = points[:,1].max()

    resolution = 1.0

    nx = int(np.ceil((xmax-xmin)/resolution))
    ny = int(np.ceil((ymax-ymin)/resolution))

    DSM = np.full((ny,nx), -np.inf)

    for x,y,z,_ in points:
        ix = int((x-xmin)/resolution)
        iy = int((y-ymin)/resolution)

        DSM[iy,ix] = max(DSM[iy,ix],z)

    # construction grille
    cells = []

    for iy in range(DSM.shape[0]):
        for ix in range(DSM.shape[1]):

            z = DSM[iy, ix]

            if z > -np.inf:   # cellule non vide
                cells.append([ix, iy, z])

    cells = np.asarray(cells)

# Breseham
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

# Caluclate Shadow Top
def process_cell(ix, iy, z, alpha, psi, DSM,  shadow):
    if alpha <= 0:
        return

    theta = psi - math.pi

    D = min(z / math.tan(alpha), 2 * max(DSM.shape)) # pour éviter d'avoir trop de points

    dx = -D * math.sin(theta)
    dy = -D * math.cos(theta)

    x_top = ix - dx
    y_top = iy - dy

    #
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

# Bvh
class BVHNode:
    def __init__(self, cells, leaf_size=512):
        self.left = None
        self.right = None
        self.cells = None

        # positions XY
        xy = cells[:, :2]

        self.min = xy.min(axis=0)
        self.max = xy.max(axis=0)

        # feuille
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

#Parcours du BVH
def traverse(node, alpha, psi, DSM, shadow):
    if node is None:
        return

    # feuille
    if node.cells is not None:

        for ix, iy, z in node.cells:

            process_cell(ix, iy, z, alpha, psi, DSM, shadow)

        return

    traverse(node.left, alpha, psi, DSM, shadow)
    traverse(node.right, alpha, psi, DSM, shadow)

# Plot shadow
def plot_shadow(shadow):
    # Security
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
    print("plot ready")
    plt.show()

# load laz file
def load_point_cloud(filename, user_choice):
    if user_choice == 1:     # All
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [filename]
        }))

    if user_choice == 2:    # végétation <1.5m to végétation 15m uniquement
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 3 || Classification == 4 || Classification == 5",
                }
            ]
        }))

    if user_choice == 3:    # végétation <1.5m to végétation > 15m uniquement
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 3 || Classification == 4 || Classification == 5 || Classification == 8",
                }
            ]
        }))

    if user_choice == 4:    # Bâtiments uniquement
        pipeline = pdal.Pipeline(json.dumps({
            "pipeline": [
                filename,
                {
                    "type": "filters.expression",
                    "expression": "Classification == 6",
                }
            ]
        }))

    pipeline.execute()
    arrays = pipeline.arrays[0]
    points = np.vstack((arrays['X'], arrays['Y'], arrays['Z'], arrays['Classification'])).transpose()
    return points

# Construire Mode de surface numérique (DSM)
def build_dsm(points, resolution=1.0):
    print("begin building DSM")
    xmin, ymin = points[:,0].min(), points[:,1].min()
    xmax, ymax = points[:,0].max(), points[:,1].max()

    nx = int((xmax - xmin) / resolution) + 1
    ny = int((ymax - ymin) / resolution) + 1

    DSM = np.full((ny, nx), -np.inf)

    for x, y, z, _ in points:
        ix = int((x - xmin) / resolution)
        iy = int((y - ymin) / resolution)

        DSM[iy, ix] = max(DSM[iy, ix], z)

    return DSM, xmin, ymin, resolution

# Transformer DSM en cellules (ix, iy, z)
def dsm_to_cells(DSM):
    print("begin converting DSM to cells")
    cells = []

    for iy in range(DSM.shape[0]):
        for ix in range(DSM.shape[1]):

            z = DSM[iy, ix]

            if z > -np.inf:
                cells.append([ix, iy, z])

    return np.asarray(cells)

def user_classification_choice():
    print("Welcome to the urban shadow calculator.\n")
    print("1 : All classifications.")
    print("2 : Vegetation ranging from <1.5 m to 15 m only.")
    print("3 : Vegetation ranging from <1.5 m to >15 m only.")
    print("4 : Buildings only.\n")
    while True:
        choice = input("Please choose the classification to use (1, 2, 3, or 4): ")

        if choice in ("1", "2", "3", "4"):
            choice = int(choice)
            break

        print("Invalid input. Please enter 1, 2, 3, or 4.")

    print(f"You have chosen to calculate the shadow of classification number: {choice}")
    print("\n")
    return choice

def user_sun_phase_choice(alpha_list):
    if alpha_list[0]<=0:
        while True:
            print("\nPlease choose a phase of the day (from sunrise to sunset) between 1 and ", len(alpha_list) - 1, ":")
            user_time_index = input()
            if user_time_index.isdigit() and 1 <= int(user_time_index) < len(alpha_list):
                user_time_index = int(user_time_index)
                break
            print(f"Invalid entry. Please enter a number between 1 and {len(alpha_list) - 1}.")
        return user_time_index
    else:
        while True:
            print("\nPlease choose a phase of the day (from sunrise to sunset) between 0 and ", len(alpha_list)-1, ":")
            user_time_index = input()
            if user_time_index.isdigit() and 0 <= int(user_time_index) < len(alpha_list):
                user_time_index = int(user_time_index)
                break
            print(f"Invalid entry. Please enter a number between 0 and {len(alpha_list) - 1}.")
        return user_time_index

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

# Main void
def main():
    choice = user_classification_choice()
    year, month, day = user_date_choice()
    date = datetime(year, month, day)

    points = load_point_cloud("18420_51760.laz", choice) #18535_51805.laz
    print("points loaded")

    grille(points)
    print("grille created")
    DSM, xmin, ymin, resolution = build_dsm(points)
    print("DSM created")
    cells = dsm_to_cells(DSM)
    print("cells created:", len(cells))

    print("begin to create BVHNode")
    bvh = BVHNode(cells)
    print("BVH created")

    #date = datetime(2023, 6, 6) # 2023 06 21

    alpha_list, psi_list, omega = sunpos(
        latitude_deg=45.75, #20.20
        tau_deg= 45, #15 - 25
        date=date
    )

    time_index = user_sun_phase_choice(alpha_list)

    print("\nValeurs :")
    print("elevation value :", alpha_list[time_index])
    print("azimuth value :", psi_list[time_index])
    print("hour angle value :", omega[time_index])
    print("\n")

    """
    print("\nValeurs :")
    print("elevation list :", alpha_list)
    print("azimuth :", psi_list)
    print("hour angle list :", omega)
    print("\n")
    """

    alpha = math.radians(alpha_list[time_index])
    psi = math.radians(psi_list[time_index])
    shadow = []

    print("begin traverse")
    traverse(
        bvh,
        alpha,
        psi,
        DSM,
        shadow
    )

    shadow = np.asarray(shadow)
    plot_shadow(shadow)

if __name__ == "__main__":
    main()
