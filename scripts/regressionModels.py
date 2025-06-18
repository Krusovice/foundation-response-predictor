#%% Standard packages
import sys
from pathlib import Path
import pandas as pd

# Setting project root
try:
    ROOT_DIR = Path(__file__).resolve().parents[1]
except NameError:
    ROOT_DIR = Path.cwd()
sys.path.append(str(ROOT_DIR))

# Selfmade packages
from src.utils.paths import DATA_DIR, MODEL_EXPORT_DIR
from src.ml.feature_engineering import filter_failed_calculations, create_features_soil_layers
from src.plotting.erorr_plots import scatterplot_errors
from src.plotting.coefficient_plots import plot_feature_coefficients_linear_model
from src.ml.export_model import export_regression_model
from sklearn.pipeline import Pipeline
from src.ml.pipeline_transformers import FeatureInverseSoilE, FeatureInteractionLayers
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data_file_name = 'dataFile_2025-01-30.json'
df = pd.read_json(DATA_DIR / data_file_name)
df = filter_failed_calculations(df) # Filtering failed calculations.
df = df[df['soilModel'] == 'MC'].drop(columns=['soilModel']).reset_index() # Filtering out calculations that are not using MC soil model.
df, number_of_soil_layers = create_features_soil_layers(df) # The soil layers are transformed from one column, containing a list, into separate columns.

X = df.drop(columns=['Uy','rot'])
y = df['Uy']

# Applying featuer engineering
feature_engineering_pipeline = Pipeline(
    steps=[
        ("inverse_E", FeatureInverseSoilE()),
        ("interaction_soil_layers", FeatureInteractionLayers(number_of_soil_layers)),
        ("scale", StandardScaler()),
    ]
)

# Linear regression pipeline
linear_pipeline = Pipeline(
    steps=[
        ("features", feature_engineering_pipeline),
        ("regressor", LinearRegression())
    ]
)

# Polynomial regression pipeline
poly_pipeline = Pipeline(
    steps=[
        ("features", feature_engineering_pipeline),
        ("poly", PolynomialFeatures(degree=2, include_bias=False)),
        ("regressor", LinearRegression())
    ]
)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

linear_pipeline.fit(X_train, y_train)
poly_pipeline.fit(X_train, y_train)

# Plotting
fig = scatterplot_errors((8,6), X_test, y_test,
            (linear_pipeline, 'Linear Regression', 'b'),
            (poly_pipeline, 'Polynomial Regression (deg=2)', 'r'))

fig = plot_feature_coefficients_linear_model((8,6), linear_pipeline, X_train)

# Exporting the models
export_regression_model(linear_pipeline, MODEL_EXPORT_DIR, 'linear_model')
export_regression_model(poly_pipeline, MODEL_EXPORT_DIR, 'poly_2nd_deg_model')
