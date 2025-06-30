from sklearn.metrics import r2_score, mean_absolute_percentage_error, root_mean_squared_error
import numpy as np

def performance_evaluation(X_test, y_test, pipeline):
    """
    Evaluate and returns a pipelines performance metrics.
    
    Takes in X_test, y_test and a pipeline.
    Returns:
        r2
        mape: mean absolute percentage error
        rmse: root mean squared error
        relative rmse, root mean squared error divided by the mean.
    """
    y_pred = pipeline.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = root_mean_squared_error(y_test, y_pred)
    relative_rmse = rmse / np.mean(y_test)
    
    return r2, mape, rmse, relative_rmse