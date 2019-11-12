# -*- coding: utf-8 -*-

import requests
from pathlib import Path
from typing import Union

import numpy as np

from sklearn.linear_model import LogisticRegression


DATASET_URL = ('https://firebasestorage.googleapis.com/v0/b/hackeps-2019.'
              'appspot.com/o/noised-MNIST.npz?alt=media&token=4cee641b-9e31'
              '-42c4-b9c8-e771d2eecbad')


def download_file(url: str, 
                  file_path: Union[str, Path]):
  r = requests.get(DATASET_URL, allow_redirects=True)
  Path(file_path).open('wb').write(r.content)


def train(x: np.ndarray, 
          y: np.ndarray) -> LogisticRegression:
  lr = LogisticRegression(multi_class='auto', 
                          solver='lbfgs',
                          max_iter=500)
  lr.fit(x, y)
  return lr


def create_submission_file(preds: np.ndarray, 
                           base_path: Union[str, Path] = '.'):
  preds = preds.flatten().astype(str)
  preds = '\n'.join(preds)
  fname = Path(base_path)/'submission.txt'
  fname.open('w').write(preds)


fname = 'noised-MNIST.npz'
download_file(DATASET_URL, fname)

# Download the sumission data
data = np.load(fname)
x, y, x_submission = data.values()

# Train the model with whole data provided in the noised MNIST data
model = train(x, y)

# Inference on the x_submission data
y_pred = model.predict(x_submission)

# Remember to commit and push this file
create_submission_file(y_pred)
