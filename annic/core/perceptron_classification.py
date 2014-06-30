"""

SOM CLASSIFICATION

===================
This module performs the image classification based on Perceptron ANN.
Inputs:
    - Original image,
    - Training samples per class,
    - Number of classes,
    - Maximum training error allowed,
    - Maximum training iteration number allowed, and
    - Hidden layer structure.
Output:
    - Classified image using Perceptron network during training phase.

The algorithm trains a Perceptron network using training samples and settings:
    - The number of neurons of the input layer is equal to image grey levels,
    - The hidden layer structure is the one provided by user,
    - The output layer has only one neuron that takes values from 0 to 1,
    - Each training set has associated a numeric representation of the class:
        - class(i) = i / (class_number - 1)
When training process ends, the method introduce each image pixel to the 
network. Pixel class is the nearest neuron class (winner neuron class).
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

import Image
import neurolab as nl
from annic.core.helpers.set_management import optimize_set, normalize_pixel_set
from annic.definitions import CLASS_COLOR_RGB

class PerceptronClassification():
    def __init__(self, image, samples_per_class, class_number, training_error, 
                 max_iteration_number, hidden_layer_structure):
        
        self.image = image
        self.samples_per_class = samples_per_class
        self.class_number = class_number
        self.training_error = training_error
        self.max_iteration_number = max_iteration_number
        
        first_pixel = image.getpixel((0,0))
        pixel_size = len(first_pixel) if isinstance(first_pixel, tuple) else 1
        
        # Create a perceptron network using 'pixel size' as number of inputs, 
        # with 'hidden_layer_structure' and an output layer of one neuron
        self.network = nl.net.newff([[0.0, 1.0]] * pixel_size, 
                                    hidden_layer_structure + [1])
    
    def run(self):
        
        self.training_set = get_perceptron_training_set(self.samples_per_class)
        
        self.target_base = get_target_base(self.class_number)
        self.target_patterns = get_perceptron_target_patterns(
                                    self.training_set,
                                    self.samples_per_class, self.target_base)
 
        print '\n**** TRAINING PERCEPTRON NETWORK ****\n'
        self._train_network()
    
        network_output = self._simulate_network_using_full_image()
        classified_img = self._get_classified_image(network_output)
        classified_img.save("classified_perceptron.jpg", 'JPEG')
        
        return classified_img

    def _train_network(self):
        norm_training_set = normalize_pixel_set(self.training_set)

        error = self.network.train(norm_training_set, self.target_patterns, 
                                   epochs = self.max_iteration_number, 
                                   show = 100, goal = self.training_error)
        
        return error
    
    def _simulate_network_using_full_image(self):
        img_data = list(self.image.getdata())
        norm_img_data  = normalize_pixel_set(img_data)
        return self.network.sim(norm_img_data)
    
    def _get_classified_image(self, network_output):
        classified_data = \
            [get_output_class_color(network_output[i], self.target_base) 
             for i in range(len(network_output))]

        classified_img = Image.new('RGB', self.image.size)
        classified_img.putdata(classified_data)
        
        return classified_img


def get_perceptron_training_set(samples_per_class):
    class_number = len(samples_per_class)
    training_set = [samples_per_class[i][j] \
                                    for i in range(class_number) \
                                    for j in range(len(samples_per_class[i]))]
    return optimize_set(training_set, class_number)
    
def get_target_base(class_number):
    return [i/float(class_number-1) for i in range(class_number)]

def get_perceptron_target_patterns(samples, samples_per_class, target_base):
    target_patterns = []
    for sample in samples:
        sample_class = get_sample_class(sample, samples_per_class)
        target_patterns.append([target_base[sample_class]])
    
    return target_patterns

def get_sample_class(sample, samples_per_class):
    for i in range(len(samples_per_class)):
        if sample in samples_per_class[i]:
            return i
    return None

def get_output_class_color(output_value, pattern):
    distances = [abs(pattern[i] - output_value[0]) \
                 for i in range(len(pattern))]

    output_value_class =  distances.index(min(distances))
    return CLASS_COLOR_RGB[output_value_class]
    
