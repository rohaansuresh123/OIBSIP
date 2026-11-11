
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris

# Load the Iris dataset
iris = load_iris()

# Create DataFrame
df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

df["species"] = iris.target_names[iris.target]

sns.set_theme(style="whitegrid")

# Create screenshots directory if needed
import os
os.makedirs("screenshots", exist_ok=True)

# 1. Histograms
df.drop(columns="species").hist(
    figsize=(10, 7),
    bins=15,
    edgecolor="black"
)

plt.suptitle("Iris Feature Distributions")
plt.tight_layout()
plt.savefig("screenshots/01_histograms.png", dpi=150)
plt.close()

# 2. Boxplots
df_melted = df.melt(
    id_vars="species",
    var_name="feature",
    value_name="measurement"
)

plt.figure(figsize=(12, 6))

sns.boxplot(
    data=df_melted,
    x="feature",
    y="measurement",
    hue="species"
)

plt.title("Iris Feature Boxplots by Species")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("screenshots/02_boxplots.png", dpi=150)
plt.close()

# 3. Pairplot
pair_plot = sns.pairplot(
    df,
    hue="species",
    diag_kind="hist"
)

pair_plot.savefig(
    "screenshots/03_pairplot.png",
    dpi=150
)

plt.close("all")

print("All three charts saved successfully!")
