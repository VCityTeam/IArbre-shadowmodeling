import laspy
import numpy as np
import matplotlib.pyplot as plt

# teste bvh : https://pbr-book.org/3ed-2018/Primitives_and_Intersection_Acceleration/Bounding_Volume_Hierarchies

las = laspy.read("18460_51765.laz")

points = np.vstack((las.x, las.y, las.z)).T

class_colors = {
    1: "gray",
    2: "brown",
    3: "lightgreen",
    4: "green",
    5: "darkgreen",
    6: "red",
    8: "yellow",
    9: "blue"
}

colors = [class_colors.get(c, "black") for c in las.classification]

class Node:
    def __init__(self, indices, bbox):
        self.indices = indices
        self.bbox = bbox
        self.left = None
        self.right = None

def compute_bbox(points, idx):
    pts = points[idx]
    return np.min(pts, axis=0), np.max(pts, axis=0)

def build_bvh(points, indices, max_leaf=500):  #1000?
    bbox = compute_bbox(points, indices)

    node = Node(indices, bbox)

    if len(indices) <= max_leaf:
        return node

    # axe de split (variance)
    pts = points[indices]
    axis = np.argmax(np.var(pts, axis=0))

    sorted_idx = indices[np.argsort(pts[:, axis])]
    mid = len(sorted_idx) // 2

    node.left = build_bvh(points, sorted_idx[:mid], max_leaf)
    node.right = build_bvh(points, sorted_idx[mid:], max_leaf)

    return node


def draw_leaf_nodes(node, ax):
    if node is None:
        return

    if node.left is None and node.right is None:
        (xmin, ymin, _), (xmax, ymax, _) = node.bbox

        ax.plot(
            [xmin, xmax, xmax, xmin, xmin],
            [ymin, ymin, ymax, ymax, ymin],
            color="black",
            linewidth=0.3,
            alpha=0.5
        )
        return

    draw_leaf_nodes(node.left, ax)
    draw_leaf_nodes(node.right, ax)


indices = np.arange(len(points))
bvh = build_bvh(points, indices, max_leaf=300)

fig, ax = plt.subplots(figsize=(10, 8))

# points colorés LAS
ax.scatter(points[:, 0], points[:, 1], c=colors, s=0.2)

# grille BVH (feuilles uniquement)
draw_leaf_nodes(bvh, ax)

ax.set_aspect("equal")
plt.show()