"""
Adapted from LleidaHack challenges:
https://github.com/LleidaHack/HackEPSChallenges/
"""
import numpy as np
from sklearn.datasets import fetch_openml

IMAGE_SIZE = 28

#@title Code to add noise to MNIST images
class Deformation(object):

  def __init__(self, probability):
    self.probability = probability

  def transform(self, x):
    pass

  def __call__(self, x):
    if np.random.random() > self.probability:
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

def get_noised_mnist():
    x, y = fetch_openml('mnist_784', return_X_y=True)
    y = y.astype(np.int32)
    return np.stack([noise_mnist(o) for o in x]), y
