import joblib
import numpy as np
from src.utils.paths import MODEL_EXPORT_DIR


model = joblib.load(fr"{MODEL_EXPORT_DIR}/linear_model/linear_model_latest.pkl")  # Adjust path as needed

# 2. Create input data (example: one sample with 4 features)
# Make sure the number and order of features match what the model expects
X_new = np.array([[1.2, 150.0, 0.3, 12000]])  # Example: [width, load, eccentricity, soil_modulus]

# 3. Predict
y_pred = model.predict(X_new)

print("Prediction:", y_pred[0])
