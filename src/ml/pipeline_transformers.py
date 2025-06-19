from sklearn.base import BaseEstimator, TransformerMixin
from src.ml.feature_engineering import inverse_soil_E, create_features_soil_interaction_layers
from src.ml.feature_engineering import create_features_soil_layers

class ExpandSoils(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.number_of_soil_layers = max(len(l) for l in X["soils"])
        return self

    def transform(self, X):
        X = X.copy().reset_index()
        X, _ = create_features_soil_layers(X)
        return X
    
    def get_feature_names_out(self, input_features=None):
        return input_features

class FeatureInverseSoilE(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return inverse_soil_E(X.copy())
    
    def get_feature_names_out(self, input_features=None):
        return input_features

class FeatureInteractionLayers(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.number_of_soil_layers = len([c for c in X.columns if c.startswith("soil_layer_")])
        return self

    def transform(self, X):
        return create_features_soil_interaction_layers(X.copy(), self.number_of_soil_layers)

    def get_feature_names_out(self, input_features=None):
        return input_features