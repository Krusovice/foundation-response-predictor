from sklearn.base import BaseEstimator, TransformerMixin
from src.ml.feature_engineering import inverse_soil_E, create_soil_features

class InverseSoilE(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return inverse_soil_E(X.copy())

class SoilFeatures(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.n_layers = X.filter(like="E").shape[1]
        return self

    def transform(self, X):
        X, _ = create_soil_features(X.copy())
        return X

class InteractionLayer(BaseEstimator, TransformerMixin):
    def __init__(self, n_layers):
        self.n_layers = n_layers

    def fit(self, X, y=None):
        return sel

    def transform(self, X):
        return create_interaction_layer(X.copy(), self.n_layers)
