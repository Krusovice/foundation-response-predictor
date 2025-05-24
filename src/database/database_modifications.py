import random
import json
import math

def read_and_append_datafile(dataFile_path,data):
    """
    Opens an existing database file and appends new data items to it.

    The function is used if Plaxis models are carried out in multiple steps,
    so the database can grow steadily over time.
    """
    try:
        with open(dataFile_path, "r") as file:
            dataFile = json.load(file)
    except FileNotFoundError:
        dataFile = []

    dataFile.append(data)
    with open(dataFile_path, "w") as file:
        json.dump(dataFile, file, indent=4)


def create_input_data_dict(foundationWidth, 
                           E_min, 
                           E_max, 
                           ecc_factor_min, 
                           ecc_factor_max,
                           soil_layer_thickness, 
                           soilModel,
                           modelWidthFactor,
                           modelDepthFactor) -> dict:
    
    '''
    Storing all the input data a dictionary.
    
    So each item can be appended with results at a later stage.
    '''
    data_dict = dict()
    data_dict['foundationWidth'] = float(format(random.choice(foundationWidth),'0.1f'))
    data_dict['model_depth'] = modelDepthFactor*data_dict['foundationWidth']
    data_dict['model_width'] = modelWidthFactor*data_dict['foundationWidth']
    data_dict['eccentricity'] = float(format(random.uniform(ecc_factor_min,ecc_factor_max),'0.2f'))
    data_dict['soilModel'] = soilModel
    data_dict['soil_layer_thickness'] = soil_layer_thickness
    numberOfLayers = data_dict['model_depth'] / soil_layer_thickness
    data_dict['soils'] = [float(format(random.uniform(E_min,E_max),'.0f')) for i in range(int(numberOfLayers))]
    return data_dict


def add_results_to_data_item(data_dict, Uy):
    """
    Adds results for ML to be trained on to a database item.
    
    Takes in a database input item and assicated results from the FE model, 
    Uy a list of 2 items with min and max Uy for the plate.
    
    returns the database item with the results added to it.
    """
    if Uy[0] == 'Calculation failed':
        data_dict['Uy'] = 'Calculation failed'
        data_dict['rot'] = 'Calculation failed'
    else:
        diffY = max(Uy) - min(Uy)
        data_dict['Uy'] = (min(Uy) + max(Uy))/2
        data_dict['rot'] = math.asin(diffY / data_dict['foundationWidth'])
    return data_dict