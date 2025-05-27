import matplotlib.pyplot as plt
import pandas as pd

def plot_feature_coefficients_linear_model(figsize, lin_model, X_train):
    """
    Creates a lying bar plot that shows feature coefficients for linear regression model.
    
    Args:
        figsize: Tuple that gives the figsize.
        lin_model: The linear regression model for evaluation.
        X: Inputs dataframe for training the model.
        
    Return:
        fig
    """
    coefficients = pd.DataFrame(lin_model.coef_, X_train.columns, columns=['Coefficient']).reset_index()

    fig = plt.figure(figsize=(12, 6))
    plt.barh(coefficients['index'], coefficients['Coefficient'])
    plt.xlabel('Feature Importance')
    plt.title('Feature coefficients on linear regression model')
    return fig