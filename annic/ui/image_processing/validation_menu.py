"""

ANNIC VALIDATION MENU

===================
This module contains the definition of the available validation menu.
The verification method available is "confusion matrix", that allows user:
    - To select validation parameters (number of classes and class samples),
    - To start the verification.
The result of the verification are:
    - The confusion matrix, and 
    - The related Kappa coefficient.
They are shown in a new window.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Label
from annic.ui.image_processing.helpers.samples_collection import SamplesCollectionPerClass
from annic.ui.image_processing.helpers.verifiers import ConfusionMatrixVerifier

     
class ConfusionMatrixMenu(Frame):
    def __init__(self, parent, image):
        Frame.__init__(self, parent, width=180)
        self.classified_image = image
                
        self.title_label = Label(self, text = 'Confusion Matrix')
        self.title_label.pack(anchor = 'center', padx = 5, pady = 5)
        
        self.samples_collection = SamplesCollectionPerClass(self)
        self.samples_collection.pack_propagate(0)
        self.samples_collection.pack(anchor = 'w', padx = 5, pady = 5)

        self.verifier = ConfusionMatrixVerifier(self)
        self.verifier.pack(anchor = 'center', padx = 5, pady = 5)
        
    @property
    def classified_image(self):
        return self.classified_image
        
    @property
    def samples_coordinates(self):
        return self.samples_collection.samples_collector.get_coordinates()
    
    @property
    def samples_collector(self):
        return self.samples_collection.samples_collector
