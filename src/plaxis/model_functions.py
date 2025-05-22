from plxscripting.easy import * # External package that comes with Plaxis installation

def initiate_model(si, gi, data):
    """
    Initiates a plaxis model with boundary conditions based on model width and depth.
    
    The model is centered at x = 0 and surface located in 0.
    
    The model with is set to modelWidthFactor * foundationWidth
    The model with is set to modelDepthFactor * foundationDepth
    """
    model_width = modelWidthFactor*data['foundationWidth']
    model_depth = modelDepthFactor*data['foundationWidth']
    
    s_i.new()
    g_i.soilContour.initializerectangular(-model_width/2,-model_depth,model_width/2,0)

def create_borehole(gi, data):
    """
    Creates a borehole in the model, and creates the layers in the model based on data argument.
    
    Iterates through each layer in the data argument.
    Applies the create_layer function to create the layer in the model.
    """
    gi.borehole(0)
    for E_soil in data['soils']:
        create_layer(data['soilModel'],E_soil)

def create_layer(soilModel,E_soil):
    """
    Creates a layer based on arguments soilModel and E-modulus.
    
    The soil model can be either linear or MC.
    
    The remaining parameters are hardcoded into this function.
    """
    material = g_i.soilmat()
    if soilModel == 'linear':
        material.setproperties("SoilModel", 1, "gammaUnsat", 20,"gammaSat", 20, "ERef", E_soil, "nu", 0.3)
    elif soilModel == 'MC':
        material.setproperties("SoilModel", 2, "gammaUnsat", 20, "gammaSat", 20, "ERef", E_soil, "nu", 0.3, "phi", 40, "cRef", 300)    
    g_i.soillayer(soilLayerThickness)
    g_i.Soils[-1].Material = material

def insert_foundation(gi, data):
    """
    Creates a plate based on data input and sets material parameters.
    
    The plate is set with center x=0 and is modelled elastic.
    
    Plate stiffnesses has been hardcoded very large.
    """
    g_i.gotostructures()
    g_i.plate((-data['foundationWidth']/2,0),(data['foundationWidth']/2,0))
    material = g_i.platemat()
    material.setproperties('MaterialType','Elastic','EA1',10**12,'EI',10**9)
    g_i.plates[0].Material = material



def insert_pointload(gi, data):
    """
    A pointload is added at x= (0 + eccentricity).
    
    The pointload is equivalent to a foundation pressure of 100 kPa times foundation width.
    """
    g_i.pointload((data['eccentricity']*data['foundationWidth'],0))
    g_i.pointloads[-1].setproperties('Fy', -100*data['foundationWidth'])

def mesh(gi):
    """
    Creating a standard fine mesh for the model.
    """
    g_i.gotomesh()
    g_i.mesh(0.03)
    
def stage_construction(gi):
    """
    Creating the stage construction phases for the calculation and calculates the model.
    
    Returns the phase that which will contain relevant results for extraction.
    """
    g_i.gotostages()
    phase_1 = g_i.phase(g_i.Phases[0])
    g_i.plates.activate(phase_1)
    g_i.pointloads.activate(phase_1)
    g_i.calculate()
    return calculation_phase
    
def output_and_extraction(gi, result_phase):
    """
    Extract min(Uy) and max(Uy) for the only plate in the model, for a phase given as argument.
    
    Returns min and max Uy as two variables.
    """    
    output_port = g_i.view(result_phase)
    s_o, g_o = new_server('localhost', output_port, password=plaxis_password)
    if g_i.phases[-1].Reached.SumMstage.value == 1:
        Uy = g_o.getresults(g_o.plates[0], g_o.phases[-1], g_o.Resulttypes.Plate.Uy, 'node')
        Uy_unzipped = [i for i in zip(Uy)]
        Uy_max = max(Uy_unzipped)[0]
        Uy_min = min(Uy_unzipped)[0]
    else:
        Uy_max = 'Calculation failed'
        Uy_min = Uy_max
        print('Calculation failed')
    g_o.close()
    return Uy_max, Uy_min