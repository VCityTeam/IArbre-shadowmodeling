
"""
Plot 2D LiDAR with color classification
author : karima ouadah
"""
import laspy
import matplotlib.pyplot as plt

las = laspy.read("18460_51765.laz")
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
colors = [class_colors.get(c, "black") for c in classification]
plt.figure(figsize=(12, 12))
plt.scatter(x, y, c=colors,  s=0.1)
plt.show()