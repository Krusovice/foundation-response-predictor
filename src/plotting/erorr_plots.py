import matplotlib.pyplot as plt

def scatterplot_errors(figsize, X_test, y_test, *model_inputs):
    """
    Create a scatterplot with model errors as predictions relative deviation from actual value.
    
    Args:
        figsize: Tuple that is the size of the plot figure.
        X_test: Array of test inputs.
        y_test: Array of test results.
        *model_error_inputs: Tuple that contains:
            model pipeline that can be used for predictions.
            label as string.
            color as string.
            
    Returns:
        fig, ax1
    """
    
    fig, (ax1) = plt.subplots(1, 1, figsize=figsize)

    for i in model_inputs:
        prediction = i[0].predict(X_test)
        errors = (prediction - y_test) / y_test
        ax1.plot(y_test*1000,errors,marker='o',linestyle='',color=i[2],label=i[1],alpha=0.3)

    ax1.invert_xaxis()
    ax1.set_xlabel('Actual Settlement, U$_{actual}$ [mm]')
    ax1.set_ylabel('(U$_{pred}$ - U$_{test}$) / U$_{test}$ [-]')
    ax1.minorticks_on()
    ax1.grid(which='major',alpha=0.5)
    ax1.grid(which='minor',alpha=0.2)
    ax1.legend()
    ax1.set_title('Relative Model Deviations')
    
    return fig, ax1