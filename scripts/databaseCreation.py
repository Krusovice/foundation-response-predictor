
import random
import math
import json
from src.utils.paths import DATA_DIR

from datetime import datetime
from src.plaxis.model_creation import start_plaxis_web_server,createModel

#%%
foundationWidth = [1,1.5,2,2.5,3,3.5,4] # Foundation Sizes
E_min = 10000 # Soil E module variations
E_max = 100000
soilModel = 'MC' # Soil model
ecc_factor_min = 0 # Eccentricity variation in relation to foundation with 10
ecc_factor_max = 0.3 # This eccentricity factor is multiplied onto the foundation width.
soilLayerThickness = 0.5 # Layer thickness
modelWidthFactor = 4 # Model with in total, in relation to the foundation width
modelDepthFactor = 2 # Model depth in relation to the foundation width

# Database storing location
timestamp = datetime.today().strftime("%Y%m%d_%H%M%S")
dataFile_path = fr'{DATA_DIR}\plaxis_data_file_{timestamp}.txt'

# Plaxis input information
plaxis_password = 'temporary_password'
calculationsToRun = 2500

# Starting plaxis web server
si, gi = start_plaxis_web_server(plaxis_password)
# Creating model and extracting results
Uy_max, Uy_min = createModel(si,gi,data)

def add_results_to_data_item(data, Uy_max, Uy_min):
    """
    Adds results for ML to be trained on to a database item.
    
    Takes in a database input item and assicated results from the FE model.
    
    returns the database item with the results added to it.
    """
    if Uy_max == 'Calculation failed':
        data['Uy'] = 'Calculation failed'
        data['rot'] = 'Calculation failed'
    else:
        diffY = Uy_max - Uy_min
        data['Uy'] = (Uy_min + Uy_max)/2
        data['rot'] = math.asin(diffY / data['foundationWidth'])
    return data






print('Calculation initiated')
for i in range(calculationsToRun):
    appendDataFile(dataFile_path, plaxis_password, foundationWidth, E_min, E_max, ecc_factor_min, ecc_factor_max,soilLayerThickness,soilModel)
    print(f'Iteration {i} finalized')
