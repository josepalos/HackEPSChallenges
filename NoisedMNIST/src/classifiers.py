import numpy as np

import sklearn.ensemble
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.base import BaseEstimator, TransformerMixin

import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.models import Sequential

# TODO REMOVE THIS
# Those lines tell tf to use only one cpu
#tf.config.threading.set_inter_op_parallelism_threads(2)
#tf.config.threading.set_intra_op_parallelism_threads(2)


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
    def __init__(self, n_estimators=20, max_depth=10):
        self.preprocessing_pipeline = Pipeline([
            # Normalize values for each pixel between (1, 0)
            ('scale', ImageScaler(255)),
            # Standarize values
            ('standardize', StandardScaler())
        ])
        self.model = sklearn.ensemble.RandomForestClassifier(
            n_estimators=n_estimators, max_depth=max_depth)

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
    def __init__(self,
                 batch_size=64,
                 epochs=60,
                 verbose=False,
                 dense_layers=[(128, "relu"), (512, "relu")],
                 convolutions=[(32, (3, 3), "relu"), (64, (3, 3), "relu")]):

        self.verbose = verbose

        self.preprocessing_pipeline = Pipeline([
            # Normalize values for each pixel between (1, 0)
            ('scale', ImageScaler(255)),
            # Standarize values
            ('standardize', StandardScaler())
        ])
        self.convolutions = convolutions
        self.dense_layers = dense_layers
        self.input_shape = (28, 28, 1)  # 28 pixels x 28 pixels x 1 channel
        self.output_classes = 10
        self.batch_size = batch_size
        self.epochs = epochs
        self.model = self._create_model()

    def _create_model(self):
        model = Sequential()

        first_conv = True
        for size, kernel, activation in self.convolutions:
            if first_conv:
                first_conv = False
                model.add(Conv2D(size, kernel_size=kernel,
                                 activation=activation,
                                 input_shape=self.input_shape))
                continue
            model.add(Conv2D(size, kernel_size=kernel, activation=activation))

        model.add(MaxPooling2D(pool_size=(2, 2)))

        model.add(Flatten())

        for units, activation in self.dense_layers:
            model.add(Dense(units=units, activation=activation))

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
                       epochs=self.epochs, verbose=self.verbose,
                       validation_split=.1)

    def predict(self, x_data):
        preprocessed_data = self._preprocess_data(x_data)
        return self.model.predict_classes(preprocessed_data)

    def _preprocess_data(self, data, train=False):
        if train:
            # Preprocess, but also let StandardScaler to learn the std deviation
            # and the mean
            preprocessed_data = self.preprocessing_pipeline.fit_transform(data)
        else:
            preprocessed_data = self.preprocessing_pipeline.transform(data)
        
        shape = (-1, ) + self.input_shape
        return preprocessed_data.reshape(shape)
