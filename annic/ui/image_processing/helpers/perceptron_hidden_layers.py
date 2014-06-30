"""

PERCEPTRON HIDDEN LAYERS

===================
This module allows user to select perceptron hidden layer structure:
    - User can select the number of hidden layers, and 
    - User can select the number of neuron per hidden layer.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from Tkinter import Frame, Label, IntVar, OptionMenu

DEFAULT_NUMBER_OF_HIDDEN_LAYERS = 1
MAX_NUMBER_OF_HIDDEN_LAYERS = 3

DEFAULT_NEURON_NUMBER_PER_HIDDEN_LAYER = 5
MAX_NEURON_NUMBER_PER_HIDDEN_LAYER = 12

class HiddenLayers(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width=170, heigh=150, bd=1, relief='ridge')
        
        self.title_label = Label(self, text = 'Hidden Layers')
        self.title_label.pack()
          
        self.number_of_layers = NumberOfHiddenLayers(self)
        self.number_of_layers.pack(anchor = 'center', side='top')
         
        self.neuron_number_per_layer = HiddenNeuronNumberPerLayer(self)
        self.neuron_number_per_layer.pack(anchor = 'w', side='bottom')
        
        self.number_of_layers.register_observer(self.neuron_number_per_layer)
     
    @property
    def structure(self):
        return self.neuron_number_per_layer.get()
            

class NumberOfHiddenLayers(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
                
        number_of_layers_label = Label(self, text = 'Number of layers: ')
        number_of_layers_label.grid(row=0, column=0)
        
        number_options = range(DEFAULT_NUMBER_OF_HIDDEN_LAYERS, 
                               MAX_NUMBER_OF_HIDDEN_LAYERS + 1)
        
        selected_number = IntVar(self, value = DEFAULT_NUMBER_OF_HIDDEN_LAYERS)
        option_menu = OptionMenu(self, selected_number, *number_options, 
                            command = self._on_hidden_layers_number_selection)
        option_menu.grid(row=0, column=1)

        self.observers = []
        
    def register_observer(self, observer):
        self.observers.append(observer)
        
    def _on_hidden_layers_number_selection(self, hidden_layers_number):
        for observer in self.observers:
            observer.set_number_of_hidden_layers(hidden_layers_number)


class HiddenNeuronNumberPerLayer(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.selected_class = IntVar()

        self.neuron_number = []
        for i in range(MAX_NUMBER_OF_HIDDEN_LAYERS):
            nueron_number_collector = HiddenNeuronNumber(self, layer_id = i)
            nueron_number_collector.pack(anchor = 'w', padx = 2)
            self.neuron_number.append(nueron_number_collector)
        
        self.hidden_layers_number = DEFAULT_NUMBER_OF_HIDDEN_LAYERS
        for i in range(self.hidden_layers_number):   
            self.neuron_number[i].enable()

    def get(self):
        return [self.neuron_number[i].get() \
                for i in range(self.hidden_layers_number)]
        
    def set_number_of_hidden_layers(self, hidden_layers_number):
        self.hidden_layers_number = hidden_layers_number
        for i in range(hidden_layers_number):
            self.neuron_number[i].enable()
        for i in range(hidden_layers_number, MAX_NUMBER_OF_HIDDEN_LAYERS):            
            self.neuron_number[i].disable()
            
        
class HiddenNeuronNumber(Frame):
    def __init__(self, parent, layer_id):
        Frame.__init__(self, parent)
        self.parent = parent
        
        # Layer id is a number in range(MAX_NUMBER_OF_HIDDEN_LAYERS)
        self.layer_id = layer_id
        
        label_text = 'Neurons for layer {0}: '.format(layer_id + 1)
        self.label = Label(self, text = label_text)
        self.label.grid(row=0, column=0)
         
        
        number_options = range(1, MAX_NEURON_NUMBER_PER_HIDDEN_LAYER + 1)
        self.selected_number = \
                    IntVar(self, value = DEFAULT_NEURON_NUMBER_PER_HIDDEN_LAYER)
     
        self.option_menu = OptionMenu(self, self.selected_number, \
                                      *number_options)
        self.option_menu.grid(row=0, column=1)

        self.disable()
    
    def get(self):
        return self.selected_number.get()
        
    def enable(self):
        self.label.config(state = 'normal')
        self.option_menu.config(state = 'normal')
        
    def disable(self):
        self.label.config(state = 'disabled')
        self.option_menu.config(state = 'disabled')
        
