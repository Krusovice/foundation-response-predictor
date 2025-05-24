
import random
import math
import json
from src.utils.paths import DATA_DIR

from datetime import datetime
from src.plaxis.model_creation import start_plaxis_web_server,create_model
from src.database.database_modifications import create_input_data_dict, add_results_to_data_item, read_and_append_datafile

foundationWidth = [1,1.5,2,2.5,3,3.5,4] # Foundation Sizes
E_min = 10000 # Soil E module variations
E_max = 100000
ecc_factor_min = 0 # Eccentricity variation in relation to foundation with 10
ecc_factor_max = 0.3 # This eccentricity factor is multiplied onto the foundation width.
soil_layer_thickness = 0.5 # Layer thickness
soilModel = 'MC' # Soil model
modelWidthFactor = 4 # Model with in total, in relation to the foundation width
modelDepthFactor = 2 # Model depth in relation to the foundation width

# Database storing location
timestamp = datetime.today().strftime("%Y%m%d_%H%M%S")
dataFile_path = fr'{DATA_DIR}\plaxis_data_file_{timestamp}.txt'

# Plaxis input information
plaxis_password = 'temporary_password'
calculations_to_run = 1

def calculation_iteration():
    si, gi = start_plaxis_web_server(plaxis_password)
    data_dict = create_input_data_dict(foundationWidth, 
                               E_min, 
                               E_max, 
                               ecc_factor_min, 
                               ecc_factor_max,
                               soil_layer_thickness, 
                               soilModel,
                               modelWidthFactor,
                               modelDepthFactor)
    Uy = create_model(si,gi,data_dict,plaxis_password) # Creating model and extracting results
    data_dict = add_results_to_data_item(data_dict,Uy)
    read_and_append_datafile(dataFile_path,data_dict)

for i in range(calculations_to_run):
    calculation_iteration()






# print('Calculation initiated')
# for i in range(calculationsToRun):
#     appendDataFile(dataFile_path, plaxis_password, foundationWidth, E_min, E_max, ecc_factor_min, ecc_factor_max,soilLayerThickness,soilModel)
#     print(f'Iteration {i} finalized')
