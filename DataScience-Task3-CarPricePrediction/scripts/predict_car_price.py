from pathlib import Path

import joblib
import pandas as pd


# Load trained model
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "car_price_model.pkl"

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = joblib.load(MODEL_PATH)


def get_number(prompt, minimum, maximum):
    while True:
        try:
            value = float(input(prompt))
            if minimum <= value <= maximum:
                return value
            print(f"Enter a value between {minimum} and {maximum}.")
        except ValueError:
            print("Please enter a valid number.")


def get_category(prompt, allowed_values):
    lookup = {value.lower(): value for value in allowed_values}

    while True:
        value = input(prompt).strip().lower()
        if value in lookup:
            return lookup[value]
        print("Valid options:", ", ".join(allowed_values))


print("\n========== CAR PRICE PREDICTION ==========\n")

name = input("Car name (example: Maruti Swift): ").strip()

if not name:
    raise ValueError("Car name cannot be empty.")

car_age = get_number("Car age (years): ", 0, 37)
km_driven = get_number("Kilometres driven: ", 0, 2360457)
mileage_value = get_number("Mileage value: ", 1, 100)

mileage_unit = get_category(
    "Mileage unit (kmpl/km/kg): ",
    ["kmpl", "km/kg"]
)

engine_cc = get_number("Engine capacity (CC): ", 500, 10000)
max_power_bhp = get_number("Maximum power (BHP): ", 1, 1000)
torque_nm = get_number("Torque (Nm): ", 1, 2000)
seats = get_number("Number of seats: ", 2, 14)

fuel = get_category(
    "Fuel (Diesel/Petrol/CNG/LPG): ",
    ["Diesel", "Petrol", "CNG", "LPG"]
)

transmission = get_category(
    "Transmission (Manual/Automatic): ",
    ["Manual", "Automatic"]
)

seller_type = get_category(
    "Seller type (Individual/Dealer/Trustmark Dealer): ",
    ["Individual", "Dealer", "Trustmark Dealer"]
)

owner = get_category(
    "Owner: ",
    [
        "First Owner",
        "Second Owner",
        "Third Owner",
        "Fourth & Above Owner",
        "Test Drive Car"
    ]
)

brand = name.split()[0].title()

car_data = pd.DataFrame([{
    "brand": brand,
    "car_age": car_age,
    "km_driven": km_driven,
    "mileage_value": mileage_value,
    "mileage_unit": mileage_unit,
    "engine_cc": engine_cc,
    "max_power_bhp": max_power_bhp,
    "torque_nm": torque_nm,
    "seats": seats,
    "fuel": fuel,
    "transmission": transmission,
    "seller_type": seller_type,
    "owner": owner,
}])

predicted_price = model.predict(car_data)[0]

print("\n========== PREDICTION RESULT ==========")
print("Car:", name)
print(f"Estimated Selling Price: ₹{predicted_price:,.2f}")
print("\nNote: This is a machine-learning estimate,")
print("not a guaranteed market selling price.")
