import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.datasets import fetch_openml
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import confusion_matrix, classification_report

import matplotlib.pyplot as plt

import noiser

NOISED_MNIST_FILENAME = 'noised-MNIST.npz'
SEED = 12345


def load_data(filename):
    data = np.load(filename)
    # Data has 3 np arrays: x values, y values, and x values for submission
    x, y, _ = data.values()
    return x, y

def plot_sample(x_28x28, y):
    cols = 10
    rows = 1
    plt.figure(figsize=(10, 10))
    for l in range(10): # Digits from 0 to 9
        plt.subplot(rows, cols, l + 1)
        l_digits = x_28x28[y == l]
        idx = np.random.randint(0, high=l_digits.shape[0])
    
        im = l_digits[idx]
        im = im.astype(np.float32) / 255.  # Normalize values
  
        plt.title(l)
        plt.imshow(im, cmap='binary')
        plt.axis('off')

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
    

class Classifier:
    def __init__(self):
        self.preprocessing_pipeline = Pipeline([
            # Normalize values for each pixel between (1, 0)
            ('scale', ImageScaler(255)),
            # Standarize values
            ('standardize', StandardScaler())
        ])
        self.model =  RandomForestClassifier(n_estimators=20, max_depth=10)
    
    def train(self, x_data, y_data):
        preprocessed_data = self._preprocess_data(x_data, train=True)
        self.model.fit(preprocessed_data, y_data)

    def test(self, x_data):
        preprocessed_data = self._preprocess_data(x_data)
        return self.model.predict(preprocessed_data)        

    def _preprocess_data(self, data, train=False):
        if train:
            # Preprocess, but also learn the std deviation and the mean
            # in the StandardScaler.
            return self.preprocessing_pipeline.fit_transform(data)
        else:
            return self.preprocessing_pipeline.transform(data)


def plot_confusion_matrix(y_true, y_pred,
                          cmap=plt.cm.Blues):

    title = 'Confusion matrix'
    cm = confusion_matrix(y_true, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
      
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    fig.tight_layout()

def main(generate_new_noised_dataset: bool = False,
         test_original: bool = False):
    np.random.seed(SEED)

    if generate_new_noised_dataset:
        x, y = noiser.generate_noised_mnist()
    else:
        noiser.fetch_remote_dataset(NOISED_MNIST_FILENAME)
        x, y = load_data(NOISED_MNIST_FILENAME)

    x_28x28 = x.reshape((-1, 28, 28))

    print('Total images {}, Image size in pixels {}'.format(*x.shape))
    plot_sample(x_28x28, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                        test_size=.33,
                                                        random_state=SEED)

    classifier = Classifier()
    classifier.train(x_train, y_train)
    y_pred = classifier.test(x_test)

    print(classification_report(y_test, y_pred))
    plot_confusion_matrix(y_test, y_pred)
    plt.show()

    if test_original:
        x, y = fetch_openml('mnist_784', return_X_y=True)
        y = y.astype(np.int32)

        x_test_prep = preprocessing_pipeline.transform(x_test)
        y_pred = classifier.test(x_test)

        print(classification_report(y_test, y_pred))
        plot_confusion_matrix(y_test, y_pred)
        plt.show()


if __name__ == "__main__":
    main()
