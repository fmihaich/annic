"""

ANNIC CLASSIFIERS

===================
This module:
    - Executes the selected classification algorithm when user starts it, 
    - Uses parameters selected by user (samples and training settings), and
    - Presents the classified image. (It is shown in classified image frame).
The available classifiers are:
    - Perceptron classifier,
    - SOM classifier, and
    - K-means classifier.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Button
from annic.core.k_means_classification import KMeansClassification
from annic.core.som_classification import SOMClassification
from annic.core.perceptron_classification import PerceptronClassification

class Classifier(Frame):
    def __init__(self, parent, method):
        Frame.__init__(self, parent)
        self.parent = parent
        self.method = method
        
        open_button = Button(self, text = 'Classify', relief = 'raised',
                             command=self._on_classify_image, width = 23)
        open_button.pack()
        
        self.observers = []
        
    def register_observer(self, observer):
        self.observers.append(observer)
        
    def _notify_observers(self, classified_img):
        for observer in self.observers:
            observer.set_classified_image(classified_img)
        
    def _on_classify_image(self):        
        classification_args = self._get_classification_arguments()
        classification = self.method(*classification_args)
        
        classified_img = classification.run()
        
        self._notify_observers(classified_img)
        
    def _get_classification_arguments(self):
        image = self.parent.original_img
        training_set = self.parent.samples
        class_number = self.parent.class_number
        training_error = self.parent.training_error
        max_iteration_number = self.parent.max_iteration
        return [image, training_set, class_number, training_error, 
                max_iteration_number]
        
    

class KMeansClassifier(Classifier):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Classifier.__init__(self,
                            parent = parent, 
                            method = KMeansClassification)
        

class SOMClassifier(Classifier):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Classifier.__init__(self,
                            parent = parent, 
                            method = SOMClassification)
        
class PerceptronClassifier(Classifier):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Classifier.__init__(self,
                            parent = parent, 
                            method = PerceptronClassification)
        
    def _get_classification_arguments(self):
        classification_args = Classifier._get_classification_arguments(self)
        classification_args.append(self.parent.hidden_layer_structure)
        return classification_args
        
