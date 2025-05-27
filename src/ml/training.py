from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

def train_test_split_scaled(X, y, test_size, random_state):
	"""
	Applies scipi's train_test_split and scales the X-values.

	Takes X and y as dataframes, test_size and random_state.

	Returns X_train and scaled x-values for training ang testing, and y-values for training and testing.
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
	scaler = StandardScaler()
	X_train_scaled = scaler.fit_transform(X_train)
	X_test_scaled = scaler.transform(X_test)

	return X_train_scaled, X_test_scaled, y_train, y_test

def linear_regression_model(X_train_scaled, X_test_scaled, y_train, y_test):
	"""
	Training linear regression model.

	Takes in scaled X dataframe and associated y values.

	returns model, predictions and errors.
	"""
	model = LinearRegression()
	model.fit(X_train_scaled, y_train)
	predictions = model.predict(X_test_scaled)
	errors = (predictions-y_test)/y_test

	return model, predictions, errors

def polynomial_regression_model(X_train_scaled, X_test_scaled, y_train, y_test, degree):
	"""
	Training poynomial regression model.

	Takes in scaled X dataframe and associated y values.
	Also takes in degree of the polynomial

	returns model, predictions and errors.
	"""
	model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
	model.fit(X_train_scaled, y_train)
	predictions = model.predict(X_test_scaled)
	errors = (predictions-y_test)/y_test

	return model, predictions, errors