"""

ANNIC CLASSIFICATION MENU

===================
This module contains the definition of the available classification menus.
A classification menu allows user:
    - To select classification parameters (samples and training settings),
    - To start the classification algorithm (Perceptron, SOM or K-means), and
    - To save the classified image.
The available classification menus are:
    - Perceptron classification menu,
    - SOM classification menu, and
    - K-means classification menu.
There is also and "Empty classification menu" used to hide any other menu.
The result of the classification execution is shown in classified image frame.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Label
from annic.ui.image_processing.helpers.classifiers import KMeansClassifier, \
                                                          SOMClassifier, \
                                                          PerceptronClassifier
from annic.ui.image_processing.helpers.training_settings import TrainingSettings
from annic.ui.image_processing.helpers.samples_collection import SamplesCollection, \
                                                                 SamplesCollectionPerClass
from annic.ui.image_processing.helpers.perceptron_hidden_layers import HiddenLayers
from annic.ui.image_processing.helpers.save_classified_image import SaveClassifiedImage


class ClassificationMenu(Frame):
    def __init__(self, parent, image, title, samples_collection, classifier, 
                 additional_input_menu = None):
        Frame.__init__(self, parent, width=180)
        self.original_img = image
                
        self.title_label = Label(self, text = title)
        self.title_label.pack(anchor = 'center', padx = 5, pady = 5)
        
        self.samples_collection = samples_collection(self)
        self.samples_collection.pack_propagate(0)
        self.samples_collection.pack(anchor = 'w', padx = 5, pady = 5)
        
        self.training_settings = TrainingSettings(self)
        self.training_settings.pack_propagate(0)
        self.training_settings.pack(anchor = 'w', padx = 5, pady = 5)
        
        self.additional_input_menu = None
        if additional_input_menu:
            self.additional_input_menu = additional_input_menu(self)
            self.additional_input_menu.pack_propagate(0)
            self.additional_input_menu.pack(anchor = 'w', padx = 5, pady = 5)
                
        self.classifier = classifier(self)
        self.classifier.pack(anchor = 'center', padx = 5, pady = 5)
        
        self.save_classified_image = SaveClassifiedImage(self)
        self.save_classified_image.pack(anchor = 'center', padx = 5, pady = 5)
        
        self.classifier.register_observer(self.save_classified_image)
    
    def set_image(self, image):
        self.original_img = image
        self.samples_collection.reset()
        self.training_settings.reset()
    
    @property
    def original_img(self):
        return self.original_img
       
    @property
    def class_number(self):
        return self.samples_collection.number_of_classes.get()
    
    @property
    def samples(self):
        return self.samples_collection.samples_collector.get()
    
    @property
    def samples_collector(self):
        return self.samples_collection.samples_collector
          
    @property
    def training_error(self):
        return self.training_settings.training_error.get()
    
    @property
    def max_iteration(self):
        return self.training_settings.max_iteration.get()
    
    @property
    def classifier(self):
        return self.classifier
    
    @property
    def additional_input_menu(self):
        return self.additional_input_menu


class EmptyClassificationMenu(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width=190)


class KMeansClassificationMenu(ClassificationMenu):
    def __init__(self, parent, image):
        ClassificationMenu.__init__(self,
                                    parent = parent, 
                                    image = image, 
                                    title = 'K-means Classification',
                                    samples_collection =  SamplesCollection,
                                    classifier = KMeansClassifier)


class SOMClassificationMenu(ClassificationMenu):
    def __init__(self, parent, image):
        ClassificationMenu.__init__(self,
                                    parent = parent, 
                                    image = image, 
                                    title = 'SOM Classification',
                                    samples_collection =  SamplesCollection,
                                    classifier = SOMClassifier)

        
class PerceptronClassificationMenu(ClassificationMenu):
    def __init__(self, parent, image):
        ClassificationMenu.__init__(self,
                                parent = parent, 
                                image = image, 
                                title = 'Perceptron Classification',
                                samples_collection =  SamplesCollectionPerClass,
                                classifier = PerceptronClassifier,
                                additional_input_menu = HiddenLayers)
    
    @property
    def hidden_layer_structure(self):
        return self.additional_input_menu.structure
