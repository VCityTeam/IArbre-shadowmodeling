import math
from datetime import datetime
import numpy as np
import laspy
import matplotlib.pyplot as plt

las = laspy.read("18460_51765.laz")

points = np.column_stack([
    las.x,
    las.y,
    las.z,
    las.classification
])

def sunpos(latitude_deg, tau_deg, date):

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

# classifications qui projettent une ombre
SHADOW_CLASSES = {4, 5, 6, 8}


def shadow_top(points, alpha_list, psi_list, time_index):

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

if __name__ == "__main__":

    date = datetime(2025, 6, 21)

    alpha, psi, omega = sunpos(
        latitude_deg=45.75,   # Lyon
        tau_deg=15,           # toutes les heures
        date=date
    )

    print("ω (°)   α (°)   ψ (°)")
#
    for w, a, p in zip(omega, alpha, psi):
        print(f"{w:6.1f} {a:7.2f} {p:8.2f}")
#
    shadow = shadow_top(
        points,
        alpha,
        psi,
        time_index=8
    )

#
    class BVHNode:

        def __init__(self, points, leaf_size=512):
            self.left = None
            self.right = None
            self.points = None

            xyz = points[:, :3]

            self.min = xyz.min(axis=0)
            self.max = xyz.max(axis=0)

            if len(points) <= leaf_size:
                self.points = points
                return

            extent = self.max - self.min
            axis = np.argmax(extent)

            order = np.argsort(points[:, axis])

            points = points[order]

            mid = len(points) // 2

            self.left = BVHNode(points[:mid], leaf_size)
            self.right = BVHNode(points[mid:], leaf_size)


    bvh = BVHNode(points)


    def traverse(node, alpha, psi, shadow):

        if node is None:
            return

        # feuille
        if node.points is not None:
            shadow.extend(
                shadow_top(
                    node.points,
                    alpha,
                    psi,
                    time_index=8
                )
            )

            return

        traverse(node.left, alpha, psi, shadow)
        traverse(node.right, alpha, psi, shadow)


    alpha, psi, omega = sunpos(
        latitude_deg=45.75,  # Lyon
        tau_deg=15,  # toutes les heures
        date=date
    )

    bvh = BVHNode(points)

    shadow = []

    traverse(bvh, alpha, psi, shadow)

    shadow = np.asarray(shadow)

    plt.figure(figsize=(12, 12))

    plt.scatter(
        shadow[:, 0],
        shadow[:, 1],
        s=0.2,
        c="black"
    )

    plt.scatter(
        shadow[:, 3],
        shadow[:, 4],
        s=0.2,
        c="red"
    )

    plt.axis("equal")
    plt.show()