
# from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, LassoCV
# from sklearn.preprocessing import PolynomialFeatures
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
# from sklearn.ensemble import RandomForestRegressor
# import seaborn as sns
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

data_file_name = 'dataFile_2025-01-30.json'
df = pd.read_json(DATA_DIR / data_file_name)
df = filter_failed_calculations(df)
df = inverse_soil_E(df)
df, number_of_soil_layers = create_soil_features(df)
df = create_interaction_layer(df,number_of_soil_layers)

# Additional selected feature engineering
# df = df[df['foundationWidth'] > 2]
# df = df[df['Uy'] < -0.001]
# df = df[df['foundationWidth'] == 4]
# df = df[df['eccentricity'] > 0.01]

# Filtering out linear model results
df = df[df['soilModel'] == 'MC'].drop(columns=['soilModel'])

X = df.drop(columns=['Uy','rot'])
y = df['Uy']

X_train_scaled, X_test_scaled, y_train, y_test = train_test_split_scaled(X, y, test_size=0.1, random_state=42)

lin_model, lin_predictions, lin_errors = linear_regression_model(X_train_scaled, X_test_scaled, y_train, y_test)
poly_model, poly_predictions, poly_errors = polynomial_regression_model(X_train_scaled, X_test_scaled, y_train, y_test, degree=2)

#%%

# Exploring max errors
errors = pd.DataFrame({'error':lin_errors})
X_test = X_test.apply(lambda x: 1/x if x.name.startswith('soil_layer') else x)
df2 = pd.concat([X_test,errors],axis=1)

# Plotting
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 5))

ax1.plot(y_test*1000,lin_errors,marker='o',linestyle='',color='b',label='Linear Regression',alpha=0.3)
ax1.plot(y_test*1000,poly_errors,marker='o',linestyle='',color='g',label='Polynomial Regression (deg=2)',alpha=0.3)
ax1.invert_xaxis()
ax1.set_xlabel('Actual settlement [mm]')
ax1.set_ylabel('Predicted settlement / Actual settlement [-]')
ax1.minorticks_on()
ax1.grid(which='major',alpha=0.5)
ax1.grid(which='minor',alpha=0.2)
ax1.legend()
plt.show()


#%% Feature importance on linear regression (linear coefficients)

coefficients = pd.DataFrame(lin_model.coef_, X_train.columns, columns=['Coefficient']).reset_index()
# Plot feature importance
plt.figure(figsize=(12, 6))
plt.barh(coefficients['index'], coefficients['Coefficient'])
plt.xlabel('Feature Importance')
plt.title('Feature coefficients on linear regression model')
plt.show()

# #%% Feature importance on polynomial regression (quadratic coefficients)

# coefficients = pd.DataFrame(lin_model.coef_, X_train.columns, columns=['Coefficient']).reset_index()
# # Plot feature importance
# plt.figure(figsize=(12, 6))
# plt.barh(coefficients['index'], coefficients['Coefficient'])
# plt.xlabel('Feature Importance')
# plt.title('Feature coefficients on linear regression model')
# plt.show()