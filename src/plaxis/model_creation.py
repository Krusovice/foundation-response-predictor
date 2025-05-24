from src.plaxis.model_functions import initiate_model, create_borehole, insert_foundation, insert_pointload, mesh, stage_construction, output_and_extraction
from src.plaxis import external_libs
from plxscripting.easy import * # External package that comes with Plaxis installation


# Plaxis objects, new_server comes from the plaxis module
def start_plaxis_web_server(plaxis_password):
    """
    Connects to plaxis webserver on localhost and port 10000.

    Takes in plaxis password. Requires plaxis webserver to be activated on port 10000.

    Returns objects si and gi for further plaxis api usage.
    """
    si, gi = new_server('localhost', 10000, password=plaxis_password)
    return si, gi

def create_model(si, gi, data_dict, plaxis_password):
    """
    Creating the a plaxis model with prescribed model logic and model functions.
    
    Takes in plaxis server input and global input and dictionary data.

    Returns min and max displacements for the single plate that is in the model.
    """
    # Plaxis modelling
    initiate_model(si, gi, data_dict)
    create_borehole(gi, data_dict)
    insert_foundation(gi, data_dict)
    insert_pointload(gi, data_dict)
    mesh(gi)
    calculation_phase = stage_construction(gi)
    Uy = output_and_extraction(gi, calculation_phase, plaxis_password)
    return Uy