"""

K-MEANS CLASSIFICATION

===================
This module performs the image classification based on K-means algorithm.
Inputs:
    - Original image,
    - Training samples,
    - Number of classes,
    - Maximum training error allowed, and
    - Maximum training iteration number allowed.
Output:
    - Classified image using K-means algorithm.

The algorithm finds at most "K" centroids during training phase using training
samples and settings. Each centoid has associated a class.
When training process ends, the method classifies each image pixel using 
K-means algorithm. Pixel class is the nearest centroid class.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

import Image
from scipy.cluster.vq import kmeans, vq, whiten
from annic.core.helpers.set_management import optimize_set
from annic.definitions import CLASS_COLOR_RGB

class KMeansClassification():
    def __init__(self, image, training_set, class_number, training_error, 
                 max_iteration_number): 
        self.image = image
        self.training_set = optimize_set(training_set, class_number)
        self.class_number = class_number
        self.training_error = training_error
        self.max_iteration_number = max_iteration_number
        
    def run(self):
        centroids = self._get_k_means_centroids()
        classified_image = self._get_classified_image(centroids)    
                
        return classified_image
    
    def _get_k_means_centroids(self):
        whitened_set = whiten(self.training_set)
        centroids, _ = kmeans(obs = whitened_set, 
                              k_or_guess = self.class_number,
                              iter = self.max_iteration_number,
                              thresh = self.training_error)
        return centroids
        
    def _get_classified_image(self, centroids):
        org_data = list(self.image.getdata())
        whitened_org_data = whiten(org_data)
        
        pixel_classes, _ = vq(whitened_org_data, centroids)
        
        classified_data = \
                [CLASS_COLOR_RGB[pixel_class] for pixel_class in pixel_classes]
        
        classified_img = Image.new('RGB', self.image.size)
        classified_img.putdata(classified_data)
        
        return classified_img

