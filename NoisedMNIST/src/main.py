import numpy as np

from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report

import matplotlib.pyplot as plt

import classifiers
import noiser
import submission


NOISED_MNIST_FILENAME = 'noised-MNIST.npz'
SEED = 12345


def load_data(filename):
    data = np.load(filename)
    # Data has 3 np arrays: x values, y values, and x values for submission
    x, y, _ = data.values()
    return x, y

def plot_sample(x, y):
    x_28x28 = x.reshape((-1, 28, 28))
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
         test_original: bool = False,
         create_submission: bool = False):
    np.random.seed(SEED)

    if generate_new_noised_dataset:
        x, y = noiser.generate_noised_mnist()
    else:
        noiser.fetch_remote_dataset(NOISED_MNIST_FILENAME)
        x, y = load_data(NOISED_MNIST_FILENAME)


    print('Total images {}, Image size in pixels {}'.format(*x.shape))
    # plot_sample(x, y)

    x_train, x_test, y_train, y_test = train_test_split(x, y,
                                                        test_size=.33,
                                                        random_state=SEED)

    # classifier = classifiers.RandomForestClassifier()
    classifier = classifiers.NNClassifier()

    classifier.fit(x_train, y_train)
    print("###################### TRAINED ##########################")
    y_pred = classifier.predict(x_test)
    print(y_pred)

    print(classification_report(y_test, y_pred))
    # plot_confusion_matrix(y_test, y_pred)
    # plt.show()

    if test_original:
        x_test2, y_test2 = fetch_openml('mnist_784', return_X_y=True)
        y_test2 = y_test2.astype(np.int32)

        y_pred2 = classifier.test(x_test2)

        print(classification_report(y_test2, y_pred2))
        plot_confusion_matrix(y_test, y_pred2)
        plt.show()
    
    if create_submission:
        submission.submit_model(classifier)


if __name__ == "__main__":
    main()
