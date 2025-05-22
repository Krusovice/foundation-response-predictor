def datafile_readAndAppend(dataFile_path,data):
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
                           soilLayerThickness, 
                           soilModel) -> dict:
    
    '''
    Storing all the input data a dictionary.
    
    So each item can be appended with results at a later stage.
    '''
    input_data_dict = dict()
    input_data_dict['foundationWidth'] = float(format(random.choice(foundationWidth),'0.1f'))
    model_depth = modelDepthFactor*input_data_dict['foundationWidth']
    input_data_dict['eccentricity'] = float(format(random.uniform(ecc_factor_min,ecc_factor_max),'0.2f'))
    input_data_dict['soilModel'] = soilModel
    numberOfLayers = model_depth / soilLayerThickness
    input_data_dict['soils'] = [float(format(random.uniform(E_min,E_max),'.0f')) for i in range(int(numberOfLayers))]
    return input_data_dict