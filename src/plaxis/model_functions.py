from plxscripting.easy import * # External package that comes with Plaxis installation

def initiate_model(si, gi, data_dict):
    """
    Initiates a plaxis model with boundary conditions based on model width and depth.
    
    The model is centered at x = 0 and surface located in 0.
    """
    
    si.new()
    gi.soilContour.initializerectangular(-data_dict['model_width']/2,-data_dict['model_depth'],data_dict['model_width']/2,0)

def create_borehole(gi, data_dict):
    """
    Creates a borehole in the model, and creates the layers in the model based on data argument.
    
    Iterates through each layer in the data argument.
    Applies the create_layer function to create the layer in the model.
    """
    gi.borehole(0)
    for E_soil in data_dict['soils']:
        create_layer(gi,data_dict['soilModel'],E_soil,data_dict['soil_layer_thickness'])

def create_layer(gi,soilModel,E_soil,soil_layer_thickness):
    """
    Creates a layer based on arguments soilModel and E-modulus.
    
    The soil model can be either linear or MC.
    
    The remaining parameters are hardcoded into this function.
    """
    material = gi.soilmat()
    if soilModel == 'linear':
        material.setproperties("SoilModel", 1, "gammaUnsat", 20,"gammaSat", 20, "ERef", E_soil, "nu", 0.3)
    elif soilModel == 'MC':
        material.setproperties("SoilModel", 2, "gammaUnsat", 20, "gammaSat", 20, "ERef", E_soil, "nu", 0.3, "phi", 40, "cRef", 300)    
    gi.soillayer(soil_layer_thickness)
    gi.Soils[-1].Material = material

def insert_foundation(gi, data_dict):
    """
    Creates a plate based on data input and sets material parameters.
    
    The plate is set with center x=0 and is modelled elastic.
    
    Plate stiffnesses has been hardcoded very large.
    """
    gi.gotostructures()
    gi.plate((-data_dict['foundationWidth']/2,0),(data_dict['foundationWidth']/2,0))
    material = gi.platemat()
    material.setproperties('MaterialType','Elastic','EA1',10**12,'EI',10**9)
    gi.plates[0].Material = material



def insert_pointload(gi, data_dict):
    """
    A pointload is added at x= (0 + eccentricity).
    
    The pointload is equivalent to a foundation pressure of 100 kPa times foundation width.
    """
    gi.pointload((data_dict['eccentricity']*data_dict['foundationWidth'],0))
    gi.pointloads[-1].setproperties('Fy', -100*data_dict['foundationWidth'])

def mesh(gi):
    """
    Creating a standard fine mesh for the model.
    """
    gi.gotomesh()
    gi.mesh(0.03)
    
def stage_construction(gi):
    """
    Creating the stage construction phases for the calculation and calculates the model.
    
    Returns the phase that which will contain relevant results for extraction.
    """
    gi.gotostages()
    calculation_phase = gi.phase(gi.Phases[0])
    gi.plates.activate(calculation_phase)
    gi.pointloads.activate(calculation_phase)
    gi.calculate()
    return calculation_phase
    
def output_and_extraction(gi, result_phase,plaxis_password):
    """
    Extract min(Uy) and max(Uy) for the only plate in the model, for a phase given as argument.
    
    Returns min and max Uy as two variables.
    """    
    output_port = gi.view(result_phase)
    s_o, g_o = new_server('localhost', output_port, password=plaxis_password)
    if gi.phases[-1].Reached.SumMstage.value == 1:
        Uy = g_o.getresults(g_o.plates[0], g_o.phases[-1], g_o.Resulttypes.Plate.Uy, 'node')
        Uy_unzipped = [i for i in zip(Uy)]
        Uy_max = max(Uy_unzipped)[0]
        Uy_min = min(Uy_unzipped)[0]
    else:
        Uy_max = 'Calculation failed'
        Uy_min = Uy_max
        print('Calculation failed')
    g_o.close()
    return [Uy_max, Uy_min]