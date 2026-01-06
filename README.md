🛰️ Satellite Imagery–Based Property Valuation

This project implements a Multimodal Regression Pipeline to predict residential property market values by combining traditional tabular housing data with high-resolution satellite imagery (Zoom 19). The goal is to enrich standard valuation models with environmental and neighborhood context captured from overhead imagery.

🚀 Project Overview

Conventional real estate valuation models rely heavily on interior attributes such as square footage, number of bedrooms, and construction grade.
This project extends that paradigm by leveraging Convolutional Neural Networks (CNNs) to extract visual features from satellite images, aiming to quantify:

Neighborhood density

Green space and vegetation

Urban layout and surrounding infrastructure

Proxy indicators of curb appeal

Satellite images are treated as an auxiliary data source and integrated with structured features in a hybrid learning framework.

📊 Performance Summary

After extensive experimentation and 5-fold cross-validation, the following results were achieved:

Model Architecture	R² Score	Status
Tabular Baseline (Ensemble)	0.89898	🏆 Winner
Hybrid Multimodal (Tabular + CNN)	0.89353	Benchmark
🔍 Key Insight

The tabular ensemble model captured nearly 90% of the price variance, primarily driven by features such as grade, latitude, and longitude.
While satellite imagery added contextual information, it did not outperform the strong tabular baseline on this dataset—highlighting the dominance of high-quality structured features in housing price prediction.

🏗️ Methodology
1.⁠ ⁠Data Acquisition & Preprocessing

Tabular Data

Source: King County housing dataset

Cleaning, outlier handling, and feature standardization

Log Transformations

Applied log(1 + x) to:

Target variable (price)

Skewed numerical features (e.g., sqft_living)

Satellite Image Fetching

Downloaded Zoom 19 satellite tiles using Esri World Imagery

Coordinates derived directly from property latitude and longitude

No API key required

2.⁠ ⁠Feature Engineering

Temporal Features

house_age = current_year - year_built

is_renovated flag based on renovation year

Visual Feature Extraction

Pre-trained ResNet-50 (ImageNet weights)

Final classification layer removed

Output: 2,048-dimensional visual embeddings

Dimensionality Reduction

Principal Component Analysis (PCA)

Reduced visual features to top 50 components to mitigate overfitting

3.⁠ ⁠Modeling Strategy
📌 Tabular Baseline (Ensemble)

Weighted ensemble of:

XGBoost – 40%

CatBoost – 40%

LightGBM – 20%

📌 Hybrid Multimodal Model

Concatenation of:

Tabular features

PCA-compressed visual embeddings

Trained using gradient-boosted tree models

📌 Validation

5-Fold Cross-Validation

Out-of-Fold (OOF) predictions

Leakage-safe evaluation using R² score

📂 Repository Structure
├── data_fetcher.py
│   └── Downloads Zoom-19 satellite tiles (no API key required)
│
├── preprocessing.ipynb
│   └── EDA, cleaning, feature engineering, log transforms
│
├── model_training.ipynb
│   └── Training pipeline for tabular and hybrid models
│
├── final_multimodal_predictions.csv
│   └── Final test-set predictions
│
└── property_images/
    └── Satellite image tiles for each property

🛠️ Setup & Usage
1️⃣ Install Dependencies
pip install pandas numpy scikit-learn xgboost catboost lightgbm torch torchvision pillow tqdm

2️⃣ Fetch Satellite Images
python data_fetcher.py


This will populate the property_images/ directory using latitude-longitude coordinates.

3️⃣ Train & Predict

Run the training notebook/script:

Trains the Tabular Baseline

Trains the Hybrid Multimodal Model

Compares cross-validated R² scores

Automatically selects the superior model
