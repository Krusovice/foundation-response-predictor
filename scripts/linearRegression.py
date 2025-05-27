#%% Standard packages
import sys
from pathlib import Path
import pandas as pd

# Setting project root
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

# Selfmade packages
from src.utils.paths import DATA_DIR
from src.ml.feature_engineering import filter_failed_calculations, inverse_soil_E, create_soil_features, create_interaction_layer
from src.ml.training import train_test_split_scaled, linear_regression_model, polynomial_regression_model
from src.plotting.erorr_plots import scatterplot_errors
from src.plotting.coefficient_plots import plot_feature_coefficients_linear_model

data_file_name = 'dataFile_2025-01-30.json'
df = pd.read_json(DATA_DIR / data_file_name)
df = filter_failed_calculations(df)
df = inverse_soil_E(df)
df, number_of_soil_layers = create_soil_features(df)
df = create_interaction_layer(df,number_of_soil_layers)

# Filtering out linear model results
df = df[df['soilModel'] == 'MC'].drop(columns=['soilModel'])

X = df.drop(columns=['Uy','rot'])
y = df['Uy']

X_train_scaled, X_test_scaled, y_train, y_test = train_test_split_scaled(X, y, test_size=0.1, random_state=42)

lin_model, lin_predictions, lin_errors = linear_regression_model(X_train_scaled, X_test_scaled, y_train, y_test)
poly_model, poly_predictions, poly_errors = polynomial_regression_model(X_train_scaled, X_test_scaled, y_train, y_test, degree=2)

# Plotting
fig = scatterplot_errors((8,6), y_test, 
            (lin_errors, 'Linear Regression', 'b'),
            (poly_errors, 'Polynomial Regression (deg=2)', 'r'))

fig = plot_feature_coefficients_linear_model((8,6), lin_model, X)