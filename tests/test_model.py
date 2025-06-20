#%%
import joblib
from pathlib import Path
import pandas as pd
import sys

# Setting project root
try:
    ROOT_DIR = Path(__file__).resolve().parents[1]
except NameError:
    ROOT_DIR = Path.cwd()
sys.path.append(str(ROOT_DIR))

model_test_input = [{
	'foundationWidth': 2.0,
	'eccentricity': 0.0,
	'soils': [60000]*16
}]

model = joblib.load("../model_exports/linear_model/linear_model_latest.pkl")
df = pd.DataFrame(model_test_input)
prediction = model.predict(df)
print(prediction)
#%%