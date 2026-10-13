
"""
Plot YZ Axes foreach X, with classification (Laz file)
author : karima ouadah
"""

import numpy as np
import laspy
import matplotlib.pyplot as plt

las = laspy.read("18455_51780.laz") #Data : https://data.grandlyon.com/portail/fr/jeux-de-donnees/nuage-de-points-lidar-2023-de-la-metropole-de-lyon/donnees

class_colors = {
        1: "gray",  # non classé
        2: "brown",  # sol
        3: "lightgreen", #végétation faible, <1.5m
        4: "green", # végétation moyenne 1.5-5m
        5: "darkgreen", # végétation forte 5-15m
        6: "red",  # bâtiments
        8: "yellow", # Réservé, végétation > 15m
        9: "blue"  # eau
    }

x = las.x
y = las.y
z = las.z
classification = las.classification

pas = 50

xmin = x.min()
xmax = x.max()

for begin in np.arange(xmin, xmax, pas):
    end = begin + pas

    mask = (x >= begin) & (x < end)

    if mask.sum() == 0:
        continue

    colors = [class_colors.get(c, "black") for c in classification[mask]]

    plt.figure(figsize=(8, 6))
    plt.scatter(y[mask], z[mask], c=colors,  s=0.1)
    plt.title(f"X : {begin:.0f} à {end:.0f}")
    plt.axis("equal")
    plt.show()
