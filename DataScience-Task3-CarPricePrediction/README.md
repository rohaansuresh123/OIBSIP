# Car Price Prediction with Machine Learning

## Overview
A machine learning project that predicts used-car selling prices using historical CarDekho data.

## Objectives
- Clean and preprocess vehicle data.
- Perform exploratory data analysis.
- Engineer relevant car features.
- Train and compare regression models.
- Evaluate and save the best model.
- Predict car prices using a standalone Python script.

## Dataset
- Source file: Car details v3.csv
- Original records: 8,128
- Records after duplicate removal: 6,926
- Target: selling_price

## Technologies
Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, Joblib and Jupyter Notebook.

## Models Compared

| Model | MAE (₹) | RMSE (₹) | R² |
|---|---:|---:|---:|
| Random Forest | 70,780.51 | 116,786.50 | 0.9378 |
| Linear Regression | 132,937.49 | 261,730.89 | 0.6877 |

Random Forest was selected based on its stronger test-set performance.

## Project Structure

- dataset/ — Original datasets
- notebooks/ — Exploratory analysis and model training
- scripts/ — Data cleaning and prediction scripts
- processed/ — Cleaned dataset
- models/ — Saved trained model
- screenshots/ — Project visualizations

## Run

Activate the environment:

    source ~/DIRECTORIES/OIBSIP/.venv/bin/activate

Clean the dataset:

    python scripts/clean_data.py

Open the notebook:

    jupyter notebook notebooks/01_car_price_eda.ipynb

Run the prediction script:

    python scripts/predict_car_price.py

## Sample Prediction

Illustrative Maruti Swift prediction: ₹609,448.30.

This is a model estimate, not a guaranteed market price.

## Limitations
- Model predictions depend on historical dataset quality.
- Vehicle condition and current market demand are not directly represented.
- Brand is extracted from the first word of the car name.
- Input range validation does not guarantee that every combination of specifications is realistic.

## Conclusion
This project demonstrates data preprocessing, EDA, feature engineering, regression model comparison, evaluation, model persistence and standalone prediction.
