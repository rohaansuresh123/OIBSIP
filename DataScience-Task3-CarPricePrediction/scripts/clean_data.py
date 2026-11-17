from pathlib import Path

import pandas as pd


# --------------------------------------------------
# 1. Project paths and configuration
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_DIR / "dataset" / "Car details v3.csv"
OUTPUT_FILE = PROJECT_DIR / "processed" / "cleaned_car_data.csv"

REFERENCE_YEAR = 2020


# --------------------------------------------------
# 2. Helper functions for numeric conversion
# --------------------------------------------------

def extract_numeric_value(series):
    """Extract the first numeric value from text."""
    values = series.astype("string").str.extract(
        r"([-+]?\d*\.?\d+)",
        expand=False
    )
    return pd.to_numeric(values, errors="coerce")


def convert_torque_to_nm(value):
    """
    Convert identifiable torque values into Nm.

    Nm values are retained.
    kgm values are converted using 1 kgm = 9.80665 Nm.
    Ambiguous values are treated as missing.
    """
    if pd.isna(value):
        return float("nan")

    text = str(value).strip().lower()

    number_match = pd.Series([text]).str.extract(
        r"([-+]?\d[\d,]*\.?\d*)",
        expand=False
    ).iloc[0]

    if pd.isna(number_match):
        return float("nan")

    number = float(number_match.replace(",", ""))

    if "kgm" in text:
        return number * 9.80665

    if "nm" in text:
        return number

    # Do not guess the units for ambiguous formats.
    return float("nan")


# --------------------------------------------------
# 3. Load original dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

original_rows = len(df)

print("=" * 65)
print("ORIGINAL DATASET")
print("=" * 65)
print("Shape:", df.shape)


# --------------------------------------------------
# 4. Remove exact duplicate records
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

df = df.drop_duplicates().copy()

print("\nExact duplicate rows removed:", duplicate_count)
print("Rows after duplicate removal:", len(df))


# --------------------------------------------------
# 5. Convert vehicle specifications
# --------------------------------------------------

# Mileage: preserve its original unit separately.
df["mileage_value"] = extract_numeric_value(df["mileage"])

df["mileage_unit"] = (
    df["mileage"]
    .astype("string")
    .str.extract(r"(kmpl|km/kg)", expand=False)
    .str.lower()
)

# Engine capacity in CC.
df["engine_cc"] = extract_numeric_value(df["engine"])

# Maximum power in BHP.
df["max_power_bhp"] = extract_numeric_value(df["max_power"])

# Torque standardized to Nm.
df["torque_nm"] = df["torque"].apply(convert_torque_to_nm)


# --------------------------------------------------
# 6. Feature engineering
# --------------------------------------------------

df["car_age"] = REFERENCE_YEAR - df["year"]


# --------------------------------------------------
# 7. Basic validation
# --------------------------------------------------

print("\n" + "=" * 65)
print("CLEANED DATASET VALIDATION")
print("=" * 65)

print("Original rows:", original_rows)
print("Duplicate rows removed:", duplicate_count)
print("Remaining rows:", len(df))
print("Remaining exact duplicates:", df.duplicated().sum())

print("\nMissing values in engineered features:")
engineered_columns = [
    "mileage_value",
    "mileage_unit",
    "engine_cc",
    "max_power_bhp",
    "torque_nm",
    "car_age",
]

print(df[engineered_columns].isnull().sum().to_string())

print("\nMileage unit distribution:")
print(df["mileage_unit"].value_counts(dropna=False).to_string())

print("\nTorque conversion examples:")
print(
    df[["torque", "torque_nm"]]
    .dropna(subset=["torque_nm"])
    .head(10)
    .to_string(index=False)
)


# --------------------------------------------------
# 8. Save cleaned dataset
# --------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)

print("\n" + "=" * 65)
print("CLEANING COMPLETED")
print("=" * 65)
print("Saved to:", OUTPUT_FILE)
print("Final shape:", df.shape)
