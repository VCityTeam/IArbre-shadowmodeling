import rasterio
import matplotlib.pyplot as plt

with rasterio.open("dtm.tif") as src:
    chm = src.read(1)

plt.imshow(chm, cmap="viridis")
plt.colorbar(label="Hauteur (m)")
#plt.title("Canopy Height Model")
plt.show()
