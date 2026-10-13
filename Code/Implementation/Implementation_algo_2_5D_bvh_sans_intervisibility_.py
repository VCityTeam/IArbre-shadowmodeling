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
- Bvh sur les cellules 
- calculer la position du soleil
- tranverser avec bvh
- process cell
- afficher l'ombre

Resultat : not good
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

"""
if __name__ == "__main__":

    date = datetime(2025, 6, 21)

    alpha, psi, omega = sunpos(
        latitude_deg=45.75,   # Lyon
        tau_deg=15,           # toutes les heures
        date=date
    )

    print("ω (°)   α (°)   ψ (°)")
    for w, a, p in zip(omega, alpha, psi):
        print(f"{w:6.1f} {a:7.2f} {p:8.2f}")
"""

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

# classifications qui projettent une ombre
# SHADOW_CLASSES = {4, 5, 6, 8}

# Caluclate Shadow Top
def process_cell(ix, iy, z, alpha, psi, shadow):

    if alpha <= 0:
        return

    theta = psi - math.pi

    D = z / math.tan(alpha)

    dx = -D * math.sin(theta)
    dy = -D * math.cos(theta)

    x_top = ix - dx
    y_top = iy - dy

    shadow.append([ix, iy, x_top, y_top])
"""
# Calcul des ombres
def shadow_top(points, alpha_list, psi_list, time_index):

    print("begin shadow top")
    alpha = math.radians(alpha_list[time_index])
    psi = math.radians(psi_list[time_index])

    theta = psi - math.pi

    result = []

    for x, y, z, cls in points:

        if int(cls) not in SHADOW_CLASSES:
            continue

        if alpha <= 0:
            continue

        D = z / math.tan(alpha)

        dx = D * math.sin(theta)
        dy = D * math.cos(theta)

        x_top = x - dx
        y_top = y - dy

        result.append([x, y, z, x_top, y_top, cls])

    return np.asarray(result)
"""
# Bvh
class BVHNode:

    def __init__(self, cells, leaf_size=512):
        """
        cellules (ix, iy, zmax)
        """
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
def traverse(node, alpha, psi, shadow, time_index):

    print("begin traverse")
    if node is None:
        return

    # feuille
    if node.cells is not None:

        for ix, iy, z in node.cells:

            process_cell(ix, iy, z, alpha, psi, shadow)

        return

    traverse(node.left, alpha, psi, shadow, time_index)
    traverse(node.right, alpha, psi, shadow, time_index)

# Plot shadow
def plot_shadow(shadow):

    print("begin plot")
    plt.figure(figsize=(12, 12))

# Il faudrait afficher le avant

# Grille
    plt.scatter(
        shadow[:, 0],
        shadow[:, 1],
        s=0.2,
        c="black",
        label="Point"
    )
    plt.show()
# Projection ombres

    '''
    las = laspy.read("18460_51765.laz")
    class_colors = {
        1: "gray",  # non classé
        2: "brown",  # sol
        3: "lightgreen",  # végétation faible, <1.5m
        4: "green",  # végétation moyenne 1.5-5m
        5: "darkgreen",  # végétation forte 5-15m
        6: "red",  # bâtiments
        8: "yellow",  # Réservé, végétation > 15m
        9: "blue"  # eau
    }
    x = las.x
    y = las.y
    z = las.z
    classification = las.classification
    colors = [class_colors.get(c, "black") for c in classification]
    plt.figure(figsize=(12, 12))
    plt.scatter(x, y, c=colors, s=0.1)
    '''

    plt.scatter(
        shadow[:, 2],
        shadow[:, 3],
        alpha=0.1,
        s=0.2,
        c="black",
        label="Projection"
    )

    plt.axis("equal")
    # plt.legend(loc="upper right")
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

    #print(alpha_list.len)

    #alpha = alpha_list[time_index]
    #psi = psi_list[time_index]
# a tester radians
    alpha = math.radians(alpha_list[time_index])
    psi = math.radians(psi_list[time_index])

    print("alpha:", alpha, "psi:", psi)

    shadow = []

    traverse(
        bvh,
        alpha,
        psi,
        shadow,
        time_index
    )

    shadow = np.asarray(shadow)

    plot_shadow(shadow)

if __name__ == "__main__":
    main()
