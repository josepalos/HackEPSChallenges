"""
Adapted from LleidaHack challenges:
https://github.com/LleidaHack/HackEPSChallenges/
"""
import os

from typing import Union
from pathlib import Path

import requests
import numpy as np
from sklearn.datasets import fetch_openml

IMAGE_SIZE = 28
DATASET_URL = ('https://firebasestorage.googleapis.com/v0/b/hackeps-2019.'      
               'appspot.com/o/noised-MNIST.npz?alt=media&token=4cee641b-9e31'   
               '-42c4-b9c8-e771d2eecbad')  

#@title Code to add noise to MNIST images
class Deformation(object):

  def __init__(self, mutation_chance):
    self.mutation_chance = mutation_chance

  def transform(self, x):
    pass

  def __call__(self, x):
    if np.random.random() > self.mutation_chance:
      return x
    
    return self.transform(x)

class WhitePatch(Deformation):
  def transform(self, x):
    patch_size = np.random.randint(5, high=15, size=2)
    patch_location = np.random.randint(IMAGE_SIZE/5, IMAGE_SIZE - IMAGE_SIZE/5,
                                       size=2)
    x1, y1 = patch_location
    x2, y2 = np.clip(patch_size + patch_location, 0, IMAGE_SIZE - 1)
    x[y1: y2, x1: x2] = 255.
    return x

class DropPixels(Deformation):
  def transform(self, x):
    pix_2_drop = np.random.choice([0, 1], p=[.75, .25], size=(28, 28))
    pix_2_drop = np.where(pix_2_drop)
    x[pix_2_drop] = 255.
    return x

class DeformationPipeline(object):
  def __init__(self, *deformations):
    self.deformations = deformations
  
  def __call__(self, x):
    x = x.reshape(IMAGE_SIZE, IMAGE_SIZE)
    for d in self.deformations:
      x = d(x)
    return x.reshape(-1)

noise_mnist = DeformationPipeline(WhitePatch(7.), 
                                  DropPixels(8.))

def generate_noised_mnist(times: int=1):
    x, y = fetch_openml('mnist_784', return_X_y=True)
    y = y.astype(np.int32)

    noise = list()
    for n in range(0, times):
        noise.extend([noise_mnist(o) for o in x])

    noised_x = np.stack(noise)
    return noised_x, np.tile(y, times)


def fetch_remote_dataset(file_path: Union[str, Path], force: bool = False):
    if not force and os.path.isfile(Path(file_path)):
        print("Dataset already downloaded")
        return

    with requests.get(DATASET_URL, allow_redirects=True, stream=True) as req, \
            open(Path(file_path), "wb") as dataset_file:
        req.raise_for_status()
        shutil.copyfileobj(req.raw, dataset_file)

