# -*- coding: utf-8 -*-

import os
import shutil
from pathlib import Path
from typing import Union
import numpy as np
from sklearn.linear_model import LogisticRegression
import requests


DATASET_URL = ('https://firebasestorage.googleapis.com/v0/b/hackeps-2019.'
               'appspot.com/o/noised-MNIST.npz?alt=media&token=4cee641b-9e31'
               '-42c4-b9c8-e771d2eecbad')


def download_file(url: str,
                  file_path: Union[str, Path],
                  force: bool = False):
    if not force and os.path.isfile(Path(file_path)):
        return

    with requests.get(url, allow_redirects=True, stream=True) as req, \
            open(Path(file_path), "wb") as file_:
        # Check if the request failed
        req.raise_for_status()
        # Copy the request stream to the file
        shutil.copyfileobj(req.raw, file_)


def train(data_x: np.ndarray,
          data_y: np.ndarray) -> LogisticRegression:
    lr_model = LogisticRegression(multi_class='auto',
                                  solver='lbfgs',
                                  max_iter=500)
    lr_model.fit(data_x, data_y)
    return lr_model


def create_submission_file(preds: np.ndarray,
                           base_path: Union[str, Path] = '.'):
    preds = preds.flatten().astype(str)
    preds = '\n'.join(preds)
    fname = Path(base_path)/'submission.txt'
    with open(fname, "w") as file_:
        file_.write(preds)
    return fname


def submit_model(model, force_download: bool = False):
    fname = 'noised-MNIST.npz'
    download_file(DATASET_URL, fname, force_download)

    data = np.load(fname)
    _, _, x_submission = data.values()

    y_pred = model.predict(x_submission)
    fname = create_submission_file(y_pred)
    print("Submission file created: %s" % fname)


def main():
    fname = 'noised-MNIST.npz'
    print("Downloading dataset")
    download_file(DATASET_URL, fname)

    print("Loading data")
    data = np.load(fname)
    data_x, data_y, _ = data.values()

    print("Training... This might take a while")
    model = train(data_x, data_y)

    print("Generate the submit file using this model")
    submit_model(model)

if __name__ == "__main__":
    main()
