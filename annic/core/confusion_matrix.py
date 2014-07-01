"""

CONFUSION MATRIX

===================
This module verifies the classification quality thought a confusion matrix.
Inputs:
    - Classified image, and
    - Known samples per class.
Output:
    - Confusion matrix, and
    - Kappa coefficient.

This module summarizes the relation between known classes and classes got by 
the used classification algorithm.
In order to reach that goal, a confusion matrix and a Kappa coefficient are 
calculated.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from annic.definitions import CLASS_COLOR_RGB
import numpy as np
import itertools

class CalculateConfusionMatrix():
    def __init__(self, classified_image, samples_coordinates):
        self.classified_image = classified_image
        self.samples_coordinates = samples_coordinates
        
    def run(self):
        class_number = len(self.samples_coordinates)
        true_data, prediction = _get_data(class_number, self.classified_image,
                                          self.samples_coordinates)
        
        matrix = _get_basic_matrix(class_number, true_data, prediction)
        matrix = _add_commission_errors(class_number, matrix)
        matrix = _add_ommision_errors(class_number, matrix)

        kappa = _get_kappa_coefficient(class_number, matrix)
                
        return (matrix, kappa)
        
def _get_data(class_number, img, coordinates):
    true_data = []
    prediction = []
    
    for class_id in range(class_number):
        for box in coordinates[class_id]:
            cropped_data = _crop_image(img, box)
            prediction.extend(
                        [_get_pixel_class(pixel) for pixel in cropped_data])
            true_data.extend([class_id]*len(cropped_data))
    
    return (true_data, prediction)

def _get_basic_matrix(class_number, true_data, prediction):
    error = \
        np.array([zip(prediction, true_data).count(x) \
                 for x in itertools.product(range(class_number), repeat=2)])
    error = error.astype(float)
    
    return error.reshape(class_number, class_number)

def _add_commission_errors(class_number, matrix):
    total = [sum([row[i] for row in matrix]) for i in range(class_number)]
    rightness = [round(100.0*(matrix[i][i]/total[i]), 2) if total[i] != 0 \
                 else 0.0 for i in range(class_number)]
    error = [round(100.0 - rightness[i], 2) for i in range(class_number)]
    
    matrix = np.insert(matrix, class_number, total, axis = 0)
    matrix = np.insert(matrix, class_number + 1, rightness, axis = 0)
    matrix = np.insert(matrix, class_number + 2, error, axis = 0)
    
    return matrix

def _add_ommision_errors(class_number, matrix):
    total = [sum(row) for row in matrix[:-2]] + [None, None]
    rightness = [round(100.0*(matrix[i][i]/total[i]), 2) if total[i] != 0 \
                 else 0.0 for i in range(class_number)] + [None, None, None]
    error = [round(100.0-rightness[i], 2) for i in range(class_number)] \
            + [None, None, None]
                
    matrix = np.insert(matrix, class_number, total, axis = 1)
    matrix = np.insert(matrix, class_number + 1, rightness, axis = 1)
    matrix = np.insert(matrix, class_number + 2, error, axis = 1)
    
    return matrix

def _get_kappa_coefficient(class_number, matrix):
    total = matrix[class_number][class_number]
    observed= sum([matrix[i][i] for i in range(class_number)])/total
    expected = sum([matrix[class_number][i]*matrix[i][class_number] \
                    for i in range(class_number)]) / (total*total)
    return (observed-expected)/(1-expected)

def _crop_image(img, box):
    img_region = img.crop(box)
    return list(img_region.getdata())

def _get_pixel_class(pixel):
    return CLASS_COLOR_RGB.index(pixel)
