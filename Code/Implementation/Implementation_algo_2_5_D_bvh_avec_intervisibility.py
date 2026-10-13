import math
from datetime import datetime
import numpy as np
import laspy
import matplotlib.pyplot as plt

# Principale
"""
Etape :
- Load les points cloud
- Crée un Mode de surface numérique
- Transformer le mode de surface numérique en Cellules
- Breseham (cellule de la grille traversée par le rayon)
- Bvh sur les cellules 
- calculer la position du soleil
- tranverser avec bvh
- process cell
- afficher l'ombre

Resultat : begin to be good
"""


# Lecture file
las = laspy.read("18460_51765.laz")

points = np.column_stack([
    las.x,
    las.y,
    las.z,
    las.classification
])

# Position du soleil
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

    D = z / math.tan(alpha)

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

        print("begin BVHNode")
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

    print("begin plot")
    plt.figure(figsize=(12, 12))

    plt.scatter(
        shadow[:, 0],
        shadow[:, 1],
        alpha=1, # a voir
        s=0.2,
        c="black",
        label="Projection"
    )

    plt.axis("equal")
    plt.legend()
    plt.show()

def load_point_cloud(filename):
    print("begin load point cloud")
    las = laspy.read(filename)

    return np.column_stack([
        las.x,
        las.y,
        las.z,
        las.classification
    ])

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

#
def main():
    points = load_point_cloud("18460_51765.laz")
    print("points loaded")

    DSM, xmin, ymin, resolution = build_dsm(points)
    print("DSM created")

    cells = dsm_to_cells(DSM)
    print("cells created:", len(cells))

    # BVH sur grille
    bvh = BVHNode(cells)
    print("BVH created")

    date = datetime(2025, 6, 21)

    alpha_list, psi_list, omega = sunpos(
        latitude_deg=45.75, #20.20
        tau_deg= 45, #15 - 25
        date=date
    )

    print("Valeurs :")
    print("alpha list :", alpha_list)
    print("psi list :", psi_list)
    print("omega list :", omega)

    time_index = 1

# a tester radians
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
