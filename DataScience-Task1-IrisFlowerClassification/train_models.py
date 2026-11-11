
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# 1. Load dataset
iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

y = iris.target

target_names = iris.target_names

# 2. Split dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

# 3. Define classification models
models = {
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=200))
    ]),

    "K-Nearest Neighbors": Pipeline([
        ("scaler", StandardScaler()),
        ("model", KNeighborsClassifier(n_neighbors=5))
    ]),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
}

# 4. Train and evaluate each model
results = []

for name, model in models.items():

    print("\n" + "=" * 50)
    print("MODEL:", name)
    print("=" * 50)

    # Train
    model.fit(X_train, y_train)

    # Predict
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    # Calculate accuracy
    train_accuracy = accuracy_score(
        y_train, train_predictions
    )

    test_accuracy = accuracy_score(
        y_test, test_predictions
    )

    results.append({
        "Model": name,
        "Training Accuracy": train_accuracy,
        "Testing Accuracy": test_accuracy
    })

    print("Training Accuracy:", round(train_accuracy, 4))
    print("Testing Accuracy:", round(test_accuracy, 4))

    # Classification report
    print("\nClassification Report:")
    print(classification_report(
        y_test,
        test_predictions,
        target_names=target_names
    ))

    # Confusion matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, test_predictions))

# 5. Compare all models
results_df = pd.DataFrame(results)

print("\n\nMODEL COMPARISON")
print(results_df.to_string(index=False))

# 6. Save comparison results
results_df.to_csv(
    "model_comparison.csv",
    index=False
)

print("\nModel comparison saved successfully!")
