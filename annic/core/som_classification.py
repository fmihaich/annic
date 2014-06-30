"""

SOM CLASSIFICATION

===================
This module performs the image classification based on SOM ANN.
Inputs:
    - Original image,
    - Training samples,
    - Number of classes,
    - Maximum training error allowed, and
    - Maximum training iteration number allowed.
Output:
    - Classified image.

The algorithm trains a SOM network using training samples and settings. Each 
neuron in the network has associated a class.
When training process ends, the method introduce each image pixel to SOM ANN.
Pixel class is the nearest neuron class.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

import Image
import numpy as np
import neurolab as nl
from annic.core.helpers.set_management import optimize_set, \
                        normalize_pixel_set, get_pixel_set_from_normalized_set
from annic.definitions import CLASS_COLOR_RGB


class SOMClassification():
    def __init__(self, image, training_set, class_number, training_error, 
                 max_iteration_number):
        
        self.image = image
        self.training_set = optimize_set(training_set, class_number)
        self.class_number = class_number        
        self.training_error = training_error
        self.max_iteration_number = max_iteration_number
        
        first_pixel = image.getpixel((0,0))
        pixel_size = len(first_pixel) if isinstance(first_pixel, tuple) else 1
        self.network = nl.net.newc([[0.0, 1.0]]*pixel_size, class_number)
        
        
    def run(self):
        print '\n**** TRAINING SOM NETWORK (KOHONEN) ****\n'
        self._train_som_network()
        som_classes = self._get_som_image_classes()

    
        print '\n**** LOADING CLASS IMAGE  ****\n'
        classied_img = self._get_classified_image(som_classes)
        
        return classied_img
    
    def _train_som_network(self):
        normalized_training_set = normalize_pixel_set(self.training_set)
        
        error = self.network.train(normalized_training_set, 
                                   epochs = self.max_iteration_number,
                                   goal = self.training_error)
        return error[-1]
        
    def _get_som_image_classes(self):
        normalized_som_classes = self.network.layers[0].np['w']
        return get_pixel_set_from_normalized_set(normalized_som_classes)
                 
    def _get_classified_image(self, som_classes):
        org_data = list(self.image.getdata())
        classified_data = \
                [classify_pixel(pixel, som_classes) for pixel in org_data]
        
        classified_img = Image.new('RGB', self.image.size)
        classified_img.putdata(classified_data)
            
        return classified_img


def classify_pixel(pixel, classes):
    class_number = len(classes)
    distance_to_class = [np.linalg.norm(np.array(pixel)-np.array(classes[i])) 
                         for i in range(0, class_number)]

    pixel_class = distance_to_class.index(min(distance_to_class))
    return CLASS_COLOR_RGB[pixel_class]
