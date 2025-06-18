from sklearn.base import BaseEstimator, TransformerMixin
from src.ml.feature_engineering import inverse_soil_E, create_features_soil_interaction_layers

class FeatureInverseSoilE(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return inverse_soil_E(X.copy())
    
    def get_feature_names_out(self, input_features=None):
        return input_features

class FeatureInteractionLayers(BaseEstimator, TransformerMixin):
    def __init__(self, n_layers):
        self.n_layers = n_layers
    
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return create_features_soil_interaction_layers(X.copy(), self.n_layers)

    def get_feature_names_out(self, input_features=None):
        return input_features