import joblib
from sklearn.datasets import load_iris

# Load the saved model and species names
model = joblib.load("iris_model.pkl")
iris = load_iris()
species_names = iris.target_names

print("\nIRIS FLOWER SPECIES PREDICTOR")
print("-" * 35)
print("Enter the flower measurements in centimeters.\n")

try:
    sepal_length = float(input("Sepal length (cm): "))
    sepal_width = float(input("Sepal width (cm): "))
    petal_length = float(input("Petal length (cm): "))
    petal_width = float(input("Petal width (cm): "))

    measurements = [
        sepal_length,
        sepal_width,
        petal_length,
        petal_width
    ]

    if any(value <= 0 for value in measurements):
        raise ValueError("Measurements must be positive numbers.")

    prediction = model.predict([measurements])[0]
    probabilities = model.predict_proba([measurements])[0]

    print("\nPREDICTION RESULT")
    print("-" * 35)
    print("Predicted species:", species_names[prediction])
    print(f"Prediction confidence: {probabilities[prediction] * 100:.2f}%")

except ValueError as error:
    print("\nInvalid input:", error)

