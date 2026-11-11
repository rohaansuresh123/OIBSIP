import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris

# Load dataset
iris = load_iris()

df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

# Calculate correlation
correlation = df.corr()

print("Correlation Matrix:")
print(correlation.round(2))

# Visualize correlation
plt.figure(figsize=(9, 6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Iris Feature Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    "screenshots/04_correlation_heatmap.png",
    dpi=150
)

print("\nCorrelation heatmap saved successfully!")
