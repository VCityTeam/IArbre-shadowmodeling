import laspy
import pandas as pd

laz = laspy.read(r"18455_51780.laz")

df = pd.DataFrame({
    "C1": laz.X,
    "C2": laz.Z
})


df["C1"] = df["C1"].astype(str).apply(
    lambda x: float(x[0] + "." + x[1:])
)

df["C2"] = df["C2"].astype(str).apply(
    lambda x: float(x[0] + "." + x[1:])
)


df.to_csv(r"output_int.csv", index=False)

#print(df.head(3))