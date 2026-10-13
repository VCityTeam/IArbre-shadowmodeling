import argparse
from pathlib import Path
import numpy as np
import laspy
import matplotlib.pyplot as plt


def plot_laz_files(file):
    las = laspy.read(file)
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
    plt.show()

def main():
    parser = argparse.ArgumentParser(
        "LAS recursive splitter", description="Splits a las file bounds recursively"
    )
    parser.add_argument("input_file")
    parser.add_argument("output_dir")
    parser.add_argument("--points-per-iter", default=10**6, type=int)

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with laspy.open(args.input_file) as file:
        x_min = file.header.x_min
        x_max = file.header.x_max
        y_min = file.header.y_min
        y_max = file.header.y_max

        x_mid = (x_min + x_max) / 2
        y_mid = (y_min + y_max) / 2

        sub_bounds = [
            (x_min, y_min, x_mid, y_mid),  # bas gauche
            (x_mid, y_min, x_max, y_mid),  # bas droite
            (x_min, y_mid, x_mid, y_max),  # haut gauche
            (x_mid, y_mid, x_max, y_max),  # haut droite
        ]

        writers = [None] * len(sub_bounds)
        try:
            count = 0
            for points in file.chunk_iterator(args.points_per_iter):
                print(f"{count / file.header.point_count * 100}%")

                x, y = points.x.copy(), points.y.copy()

                point_piped = 0

                for i, (x_min, y_min, x_max, y_max) in enumerate(sub_bounds):
                    mask = (x >= x_min) & (x <= x_max) & (y >= y_min) & (y <= y_max)

                    if np.any(mask):
                        if writers[i] is None:
                            output_path = output_dir / f"output_{i}.laz"
                            writers[i] = laspy.open(
                                output_path, mode="w", header=file.header
                            )
                        sub_points = points[mask]
                        writers[i].write_points(sub_points)

                    point_piped += np.sum(mask)
                    if point_piped == len(points):
                        break
                count += len(points)
            print(f"{count / file.header.point_count * 100}%")
        finally:
            for writer in writers:
                if writer is not None:
                    writer.close()

    for i in range(4):
        file=f"output/output_{i}.laz"
        plot_laz_files(file)

if __name__ == "__main__":
    main()
    # python split_Laz_File.py file.laz outputDir; ex: python split_Laz_File.py 18535_51805.laz output