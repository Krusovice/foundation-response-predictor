import matplotlib.pyplot as plt
import pandas as pd

def plot_feature_coefficients_linear_model(figsize, linear_model_pipeline, X_train):
    """
    Creates a lying bar plot that shows feature coefficients for linear regression model.
    
    Args:
        figsize: Tuple that gives the figsize.
        linear_model_pipeline: The linear regression model pipeline for evaluation.
        X: Inputs dataframe for training the model.
        
    Return:
        fig
    """
    feature_names = linear_model_pipeline.named_steps["features"].get_feature_names_out()
    coefficients = linear_model_pipeline.named_steps["regressor"].coef_

    coefficients = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": coefficients
})

    fig = plt.figure(figsize=(12, 6))
    plt.barh(coefficients['Feature'], coefficients['Coefficient'])
    plt.xlabel('Feature Importance')
    plt.title('Feature coefficients on linear regression model')
    return fig