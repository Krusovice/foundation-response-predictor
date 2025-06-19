import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

def filter_failed_calculations(df):
    """
    Filtering out rows in dataframe where Uy=='Calculation failed'

    Returning dataframe
    """
    df = df[df['Uy'] != 'Calculation failed']
    return df

def inverse_soil_E(df):
    """
    Inversing the Emodulus for all soil layers in the dataframe.
    
    For all columns starting with "soil_layer_", the value will is inversed.
    If any value is 0 in the column, the inversed value will be kept at 0.

    That is due to the expectation that a layers strain is
    linearly correlated to the inversed E-modulus, not the E-modulus.

    returns df
    """
    for col in df.columns:
        if col.startswith('soil_layer_'):
            df[col] = df[col].apply(lambda x: 1/x if x != 0 else 0)
    return df


def extend_array(array,max_length):
    """
    Extending an array with zeros, so it matches max_length

    Takes in array.
    Returns array.
    """
    fillLength = max_length - len(array)
    array.extend([0] * fillLength)
    return array

def create_features_soil_layers(df, number_of_soil_layers=None):
    """
    The soil layers from column 'soils' comes as lists with various lengths.
    
    Each soil layer should be a feature.
    So each soil layer should have its own column in the dataframe.
    
    That is done by extending the length of all soil layer lists, so they're all having the same length.
    The reason for shorter lists is due to boundary conditions less deep. So each layer that is added, will
    be added as a soil layer with a very large stiffness, so it acts as not contributing to the settlements.
    
    Also drops the soils column which becomes insignificant after this step.

    Takes in a dataframe and number of soil layers. If not number of soil layers is evaluated on basis of max number of soil layers in the dataframe.
    Returns a dataframe and number_of_soil_layers.
    """

    # Calculating max number of rows among all soil layers in the input data
    if not number_of_soil_layers:
        number_of_soil_layers = df['soils'].apply(len).max()

    # Extends up to max soil rows, with zeros.
    df['soils'] = df.apply(lambda row: extend_array(row['soils'], max_length=number_of_soil_layers), axis=1)
    
    # Creates a dataframe with columns soil_layer_i for each soil layer.
    soils_df = pd.DataFrame(df['soils'].to_list(), columns=[f'soil_layer_{i}' for i in range(number_of_soil_layers)])
    
    # Adds the soil_layer_i columns to the main dataframe.
    df = pd.concat([df, soils_df], axis=1)
    df = df.drop('soils', axis=1)
    return df, number_of_soil_layers

def create_features_soil_interaction_layers(df,number_of_soil_layers):
    """
    Creates new features that are each soil layer * foundation with.

    That allows for the regression model to account for soil 
    layers influence based on foundation sizes.

    That is important, as larger foundations are significantly
    more influenced by deeper soil layers, compared to the smaller
    foundations.

    Takes in dataframe and number of soil layers.
    Returns dataframe.
    """

    for i in range(number_of_soil_layers):
        df[f'soil_layer_foundation_size_{i}'] = df[f'soil_layer_{i}'] * df['foundationWidth']

    return df