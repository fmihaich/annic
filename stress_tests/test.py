"""

ANNIC STRESS TEST

================
This module executes the stress test for any of the classification methods.
The available stress test are:
    - Perceptron stress test,
    - SOM stress test, and
    - K-means stress test.
----------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

import time
import numpy as np
import os

from annic.core.perceptron_classification import PerceptronClassification
from annic.core.som_classification import SOMClassification
from annic.core.k_means_classification import KMeansClassification
from annic.core.confusion_matrix import CalculateConfusionMatrix
from stress_tests.test_data_definition import FourColorsTestData, BoxesTestData
from annic.definitions import CLASS_COLOR_RGB

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'output')

class StressTest():
    def __init__(self, test_data, iterations, algorithm_name, output_file):
        self.test_data = FourColorsTestData() # Default test data
        if test_data == 'boxes':
            self.test_data = BoxesTestData()
         
        self.iterations = iterations
        
        self.algorithm_name = algorithm_name
        self.output_file = output_file
        
        self.classification = None
        self.classified_img = None
        
    def run(self):
        classification_time = []
        kappa = []
        
        for _ in range(self.iterations):
            classification_time.append(self._get_classification_time())
            kappa.append(self._get_kappa_coefficient())
            
        _save_stress_test_result(self.output_file, self.algorithm_name, 
                                 classification_time, kappa)
        
    def _get_classification_time(self):
        start_time = time.clock()
        self.classified_img = self.classification.run()
        self.classified_img.save(os.path.join(OUTPUT_DIR,'test_img.jpg'), 'JPEG')
        return time.clock()- start_time
       
    def _get_kappa_coefficient(self):
        validation_set = self._get_validation_set()
        verifier = CalculateConfusionMatrix( 
                                    classified_image = self.classified_img, 
                                    samples_coordinates = validation_set)
        _, kappa = verifier.run()
        return kappa
        
    def _get_validation_set(self):
        return self.test_data.validation_set
        

class PerceptronStressTest(StressTest):
    def __init__(self, test_data, iterations, algorithm_name, output_file):
        StressTest.__init__(self, test_data, iterations, algorithm_name, 
                            output_file)
        
        self.classification = PerceptronClassification(
            image = self.test_data.original_img, 
            samples_per_class = self.test_data.training_set, 
            class_number = self.test_data.class_number,
            training_error = self.test_data.training_error, 
            max_iteration_number = self.test_data.max_iteration_number,
            hidden_layer_structure = self.test_data.perceptron_hidden_layers) 
        

class SOMStressTest(StressTest):
    def __init__(self, test_data, iterations, algorithm_name, output_file):
        StressTest.__init__(self, test_data, iterations, algorithm_name, 
                            output_file)
                        
        self.classification = SOMClassification(
            image = self.test_data.original_img, 
            training_set = _get_one_samples_set(self.test_data.training_set), 
            class_number = self.test_data.class_number,
            training_error = self.test_data.training_error, 
            max_iteration_number = self.test_data.max_iteration_number) 

    def _get_validation_set(self):
        class_number = self.test_data.class_number
        validation_set = [[]] * self.test_data.class_number
        org_validation_set = self.test_data.validation_set
        
        for i in range(class_number):
            set_class = _get_set_class(self.classified_img, 
                                       org_validation_set[i])
            validation_set[set_class] = \
                    validation_set[set_class] + org_validation_set[i]
        
        return validation_set

class KMeansStressTest(StressTest):
    def __init__(self, test_data, iterations, algorithm_name, output_file):
        StressTest.__init__(self, test_data, iterations, algorithm_name, 
                            output_file)
        
        self.classification = KMeansClassification(
            image = self.test_data.original_img, 
            training_set = _get_one_samples_set(self.test_data.training_set), 
            class_number = self.test_data.class_number, 
            training_error = self.test_data.training_error, 
            max_iteration_number = self.test_data.max_iteration_number)


def _get_one_samples_set(samples_per_class):
    samples_set = []
    for samples in samples_per_class:
        samples_set.extend(samples)
    
    return samples_set


def _get_set_class(classified_img, box_set):
    print "% box_set[0]: ", box_set[0]
    x, _, y, _ = box_set[0]
    pixel = classified_img.getpixel((x,y))
    print "% pixel: ", pixel
    try:
        set_class = CLASS_COLOR_RGB.index(pixel)
        print "% set_class: ", set_class
        return set_class
    except ValueError:
        print "% set_class - default: ", 0
        return 0

        
def _save_stress_test_result(file_name, algorithm, times, kappa):
    result_file = os.path.join(OUTPUT_DIR, file_name)
    with open(result_file, 'w') as f:
        f.write('*** STRESS TEST RESULT ***\n\n')
        f.write('* Algorithm: {0}\n'.format(algorithm.upper()))
        f.write('* Test Data: 4colors\n\n')
        
        for i in range(len(times)):
            f.write(('- Iteration {0}: Classification time: {1} seconds - '
                     'Kappa Coefficient: {2}\n').\
                     format(i+1, round(times[i],4), round(kappa[i],4)))
        
        f.write('\n* TIME AVERAGE: {0}\n'.format(np.mean(times)))
        f.write('* KAPPA COEFFICIENT AVERAGE: {0}\n'.format(np.mean(kappa)))
        
        f.write('\n* Details:\n')
        f.write(('\t- Percentage of Kappa Coefficient less or equal than 0.00: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, -1.0, 0.0))))
        f.write(('\t- Percentage of Kappa Coefficient between 0.00 and 0.20: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, 0.0, 0.2))))
        f.write(('\t- Percentage of Kappa Coefficient between 0.21 and 0.40: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, 0.2, 0.4))))
        f.write(('\t- Percentage of Kappa Coefficient between 0.41 and 0.60: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, 0.4, 0.6))))
        f.write(('\t- Percentage of Kappa Coefficient between 0.61 and 0.80: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, 0.6, 0.8))))
        f.write(('\t- Percentage of Kappa Coefficient between 0.81 and 1.00: '
                 '{0}%\n'.format(_get_percentaje_between(kappa, 0.8, 1.0))))
            
def _get_percentaje_between(obs, a, b):
    obs_number = float(sum(a<i and i<=b for i in obs))/float(len(obs))
    return round(100.0*obs_number, 2)
