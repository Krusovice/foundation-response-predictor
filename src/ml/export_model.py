import joblib
from datetime import datetime
import os

def export_regression_model(model_variable, root_export_folder, model_id):
	"""
	Exports a scikit-learn regression model using joblib.

	Exports into a folder structure from root_export_folder based on
	root_export_folder
		model_id (representing model)
			model_id_timestamp

	Hence, the root_export_folder may contain multiple models by filenames and each of the versions.
	Each model always contains a file named filename_latest, which is updated for each export.

	args:
		model_variable: The model variable to be exported.
		path: path to the root export folder directory, to be exported to.
		model_id: the model_id of the exported model file.
	"""

	now = datetime.now()
	timestamp = now.strftime("%Y%m%d_%H%M%S")

	export_directory = rf"{root_export_folder}/{model_id}"
	os.makedirs(export_directory, exist_ok=True)

	export_file_path_timestamp = rf"{export_directory}/{model_id}_{timestamp}.pkl"
	export_file_path_latest = rf"{export_directory}/{model_id}_latest.pkl"

	joblib.dump(model_variable, export_file_path_timestamp)
	joblib.dump(model_variable, export_file_path_latest)