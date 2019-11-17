import numpy as np

import sklearn.ensemble
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential

# We can define custom transformers of pipelines
class ImageScaler(BaseEstimator, TransformerMixin):
    def __init__(self, scale_factor):
        self.scale_factor = scale_factor

    def fit(self, x, y=None):
        return self

    def transform(self, x):
        x = x.astype(np.float64)
        x = x / float(self.scale_factor)
        return x


class RandomForestClassifier:
    def __init__(self):
        self.preprocessing_pipeline = Pipeline([
            # Normalize values for each pixel between (1, 0)
            ('scale', ImageScaler(255)),
            # Standarize values
            ('standardize', StandardScaler())
        ])
        self.model = sklearn.ensemble.RandomForestClassifier(n_estimators=20,
                                                             max_depth=10)

    def fit(self, x_data, y_data):
        preprocessed_data = self._preprocess_data(x_data, train=True)
        self.model.fit(preprocessed_data, y_data)

    def predict(self, x_data):
        preprocessed_data = self._preprocess_data(x_data)
        return self.model.predict(preprocessed_data)

    def _preprocess_data(self, data, train=False):
        if train:
            # Preprocess, but also let StandardScaler to learn the std deviation
            # and the mean
            return self.preprocessing_pipeline.fit_transform(data)
        
        return self.preprocessing_pipeline.transform(data)


class NNClassifier:
    def __init__(self):
        self.preprocessing_pipeline = Pipeline([
            # Normalize values for each pixel between (1, 0)
            ('scale', ImageScaler(255)),
            # Standarize values
            ('standardize', StandardScaler())
        ])
        self.layers = [128, 512]
        self.input_shape = (784,)
        self.output_classes = 10
        self.batch_size = 64
        self.epochs = 60
        self.model = self._create_model()

    def _create_model(self):
        model = Sequential()

        model.add(Dense(units=self.layers[0], activation="sigmoid",
                        input_shape=self.input_shape))

        for layer in self.layers[1:]:
            model.add(Dense(units=layer, activation="sigmoid"))

        model.add(Dense(units=self.output_classes, activation="softmax"))

        model.summary()

        model.compile(optimizer="sgd", loss="categorical_crossentropy",
                      metrics=["accuracy"])
        return model

    def fit(self, x_data, y_data):
        preprocessed_data = self._preprocess_data(x_data, train=True)

        # Use one hot encoding
        y_data = to_categorical(y_data, self.output_classes)

        self.model.fit(preprocessed_data, y_data, batch_size=self.batch_size,
                       epochs=self.epochs, verbose=False, validation_split=.1)

    def predict(self, x_data):
        preprocessed_data = self._preprocess_data(x_data)
        return self.model.predict_classes(preprocessed_data)

    def _preprocess_data(self, data, train=False):
        if train:
            # Preprocess, but also let StandardScaler to learn the std deviation
            # and the mean
            return self.preprocessing_pipeline.fit_transform(data)
        else:
            return self.preprocessing_pipeline.transform(data)
