"""

TRAINING SETTINGS

===================
This module allows user to select training settings to use during classification
    - User can select the maximum training error allowed, and 
    - User can select the maximum training iterations allowed.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Label, DoubleVar, IntVar, OptionMenu
from annic.definitions import DEFAULT_TRAINING_ERROR, DEFAULT_MAX_ITERATIONS

class TrainingSettings(Frame):
    def __init__(self, parent, differentiate_class = True):
        Frame.__init__(self, parent, width=170, heigh=85, bd=1, relief='ridge')
        
        self.title_label = Label(self, text = 'Training Settings')
        self.title_label.pack()
          
        self.training_error = TrainingError(self)
        self.training_error.pack(anchor = 'w', side='top')
        
        self.max_iteration = MaximumNumberOfIterations(self)
        self.max_iteration.pack(anchor = 'w', side='bottom')
        
    def reset(self):
        self.training_error.reset()
        self.max_iteration.reset()
        
    @property
    def training_error(self):
        return self.training_error
    
    @property
    def max_iteration(self):
        return self.max_iteration
            
            
class TrainingError(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        training_error_laber = Label(self, text = 'Training Error: ')
        training_error_laber.pack(side = 'left')
        
        error_options = [round(0.1 + i*0.1, 2) for i in range(25)]
        self.selected_error = DoubleVar(self, value = DEFAULT_TRAINING_ERROR)
        option_menu = OptionMenu(self, self.selected_error, *error_options, 
                                 command = self._on_error_selection)
        option_menu.pack(side = 'right')
    
    def get(self):
        return self.selected_error.get()
    
    def reset(self):
        self.selected_error.set(DEFAULT_TRAINING_ERROR)
        
    def _on_error_selection(self, selected_error):
        print "Selected training error: ", selected_error
          
            
class MaximumNumberOfIterations(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        max_iteration_laber = Label(self, text = 'Max iteration: ')
        max_iteration_laber.pack(side = 'left')
        
        max_iteration_options = [500 + i*500 for i in range(15)]
        self.selected_maximum = IntVar(self, value = DEFAULT_MAX_ITERATIONS)
        option_menu = OptionMenu(self, self.selected_maximum, 
                                 *max_iteration_options, 
                                 command = self._on_maximum_selection)
        option_menu.pack(side = 'right')
        
    def get(self):
        return self.selected_maximum.get()
    
    def reset(self):
        self.selected_maximum.set(DEFAULT_MAX_ITERATIONS)
    
    def _on_maximum_selection(self, selected_maximum):
        print "Selected max number of iteration: ", selected_maximum
            