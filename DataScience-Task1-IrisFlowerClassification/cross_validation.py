import joblib
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

# Load dataset
iris = load_iris()
X = iris.data
y = iris.target

# Keep final test data separate
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# Cross-validation only on training data
cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=200))
    ]),

    "KNN": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier(n_neighbors=5))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}

results = []

for name, model in models.items():

    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring="accuracy"
    )

    results.append({
        "Model": name,
        "Mean CV Accuracy": scores.mean(),
        "Standard Deviation": scores.std()
    })

results_df = pd.DataFrame(results)

print("\nCROSS-VALIDATION ON TRAINING DATA")
print(results_df.to_string(index=False))

# Select best model using mean CV accuracy
best_name = results_df.loc[
    results_df["Mean CV Accuracy"].idxmax(),
    "Model"
]

print("\nSelected model:", best_name)

# Fit selected model on complete training data
best_model = models[best_name]
best_model.fit(X_train, y_train)
# Save the complete fitted pipeline
joblib.dump(best_model, "iris_model.pkl")

print("\nModel saved successfully: iris_model.pkl")
# Final evaluation on untouched test data
test_predictions = best_model.predict(X_test)

from sklearn.metrics import accuracy_score, classification_report

print("\nFINAL TEST ACCURACY:")
print(accuracy_score(y_test, test_predictions))

print("\nFINAL CLASSIFICATION REPORT:")
print(classification_report(
    y_test,
    test_predictions,
    target_names=iris.target_names
))

