"""

ANNIC CLASSIFICATION VERIFIER

===================
This module:
    - Executes the verification of the classification when user starts it, and
    - Presents the validation results.
The result of the verification are:
    - The confusion matrix, and 
    - The related Kappa coefficient.
They are shown in a new window (defined in confusion matrix viewer module).
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Button
from annic.ui.validation_viewer.confusion_matrix_viewer import ConfusionMatrixViewer
from annic.core.confusion_matrix import CalculateConfusionMatrix


class ConfusionMatrixVerifier(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        open_button = Button(self, text = 'Calculate', relief = 'raised',
                             command=self._on_calculate, width = 23)
        open_button.pack()
                
    def _on_calculate(self):
        print "CONFUSION MATRIX - samples_coordinates: ", self.parent.samples_coordinates
        confusion_matrix_calculator = \
                    CalculateConfusionMatrix(
                                classified_image = self.parent.classified_image, 
                                samples_coordinates = self.parent.samples_coordinates) 
        
        confusion_matrix, kappa = confusion_matrix_calculator.run()
        
        class_number = len(self.parent.samples_coordinates)
        
        displayer = ConfusionMatrixViewer(class_number, confusion_matrix, kappa)
        displayer.run()

        print "Confusion Matrix Verifier running!"