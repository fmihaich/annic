from Tkinter import Frame, Label, Radiobutton, IntVar, OptionMenu
from annic.definitions import MAX_NUMBER_OF_CLASSES, CLASS_COLOR, \
                              DEFAULT_NUMBER_OF_CLASS, DEFAULT_CLASS
from tkMessageBox import askquestion

class SamplesCollection(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width = 170, heigh = 180, bd = 1, 
                       relief = 'ridge')
        
        self.title_label = Label(self, text = 'Samples Collection')
        self.title_label.pack()
          
        self.number_of_classes = NumberOfClasses(self)
        self.number_of_classes.pack(side='top')
        
        self.samples_collector = SamplesCollector(self)
        self.samples_collector.pack(side = 'bottom', anchor = 'w', padx = 5, pady = 5)

    @property
    def number_of_classes(self):
        return self.number_of_classes
    
    @property
    def samples_collector(self):
        return self.samples_collector
    
    def reset(self):
        self.number_of_classes.reset()
        self.samples_collector.reset()


class SamplesCollectionPerClass(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width = 170, heigh = 280, bd = 1, 
                       relief = 'ridge')
        
        self.title_label = Label(self, text = 'Samples Collection')
        self.title_label.pack()
          
        self.number_of_classes = NumberOfClasses(self)
        self.number_of_classes.pack(side = 'top')
        
        self.samples_collector = SamplesCollectorPerClass(self)
        self.samples_collector.pack(side = 'bottom', anchor = 'w', padx = 5)
        self.number_of_classes.register_observer(self.samples_collector)
   
    @property
    def number_of_classes(self):
        return self.number_of_classes
    
    @property
    def samples_collector(self):
        return self.samples_collector
    
    def reset(self):
        self.number_of_classes.reset()
        self.samples_collector.reset()


class NumberOfClasses(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        number_of_classes_label = Label(self, text = 'Number of classes: ')
        number_of_classes_label.grid(row = 0, column = 0)
        
        number_options = range(DEFAULT_NUMBER_OF_CLASS, MAX_NUMBER_OF_CLASSES+1)
        self.selected_number = IntVar(self, value = DEFAULT_NUMBER_OF_CLASS)
        option_menu = OptionMenu(self, self.selected_number, *number_options, 
                                 command = self._on_number_selection)
        option_menu.grid(row = 0, column = 1)

        self.observers = []
        
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self, class_number):
        for observer in self.observers:
            observer.set_class_number(class_number)
        
    def _on_number_selection(self, selected_number):
        self.notify_observers(selected_number)
    
    def get(self):
        return self.selected_number.get()
    
    def reset(self):
        self.selected_number.set(DEFAULT_NUMBER_OF_CLASS)


class SamplesCollector(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, width = 160, heigh = 300)
        label = Label(self)
        label_text = ( 'Collect samples for different\n'
                       'classes in order to optimize\n'
                       'the algorithm.\n' )
        
        label['text'] = label_text
        label.pack()
        
        self.samples = []
        
    def add_samples(self, samples):
        self.samples.extend(samples)
        
    def get(self):
        return self.samples
    
    def reset(self):
        self.samples = []
        

class SamplesCollectorPerClass(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.observers = []
        
        self.CLASS_NAME = ['Class {0}'.format(i+1) 
                           for i in range(MAX_NUMBER_OF_CLASSES)]
        
        self.selected_class = IntVar()
        self.class_buttons = {}
        for i in range(MAX_NUMBER_OF_CLASSES):
            class_button = Radiobutton(
                              self, text = self.CLASS_NAME[i], 
                              fg = CLASS_COLOR[i], state = 'disabled', 
                              variable = self.selected_class, value = i, 
                              command = self._on_sample_class_selection)
            class_button.pack(anchor = 'w', padx=5)
            self.class_buttons[i] = class_button
        
        self.label = Label(self)
        self.label.pack()
        
        self.class_number = DEFAULT_NUMBER_OF_CLASS
        self.samples = [[]] * MAX_NUMBER_OF_CLASSES
        self.samples_coordinates = [[]] * MAX_NUMBER_OF_CLASSES
        self.select_default_class()
        
    def register_observer(self, observer):
        self.observers.append(observer)
        
    def notify_observers(self, class_color):
        for observer in self.observers:
            observer.set_drag_color(class_color)
            
    def add_samples(self, new_samples):
        current_class = self.selected_class.get()
        self.samples[current_class] = self.samples[current_class] + new_samples
        print "Sample collector - add samples: ", \
                [len(self.samples[i]) for i in range(MAX_NUMBER_OF_CLASSES)]
                
    def add_sample_coordinates(self, new_coordinates):
        current_class = self.selected_class.get()
        self.samples_coordinates[current_class] = \
                self.samples_coordinates[current_class] + [new_coordinates]
    
    def get(self):
        return self.samples[:self.class_number]
    
    def get_coordinates(self):
        return self.samples_coordinates[:self.class_number]
    
    def select_default_class(self):
        self.class_buttons[DEFAULT_CLASS].config(state = 'normal')
        self.class_buttons[DEFAULT_CLASS].select()
        self._on_sample_class_selection()
    
    def set_class_number(self, new_class_number):
        if (self.selected_class.get() > new_class_number and 
            greater_samples_were_taken(self.samples, new_class_number)):
            if not _ask_to_reset_sample_collection():
                return
        self.class_number = new_class_number
        self._activate_class_buttons()
        
    def _activate_class_buttons(self):
        # Activate 'number_of_classes' class buttons
        if self.selected_class.get() > self.class_number:
            self.select_default_class()
            
        for i in range(self.class_number):
            self.class_buttons[i].config(state = 'normal')
        for i in range(self.class_number, MAX_NUMBER_OF_CLASSES):            
            self.class_buttons[i].config(state = 'disabled')
        
    def _on_sample_class_selection(self):
        class_name = self.CLASS_NAME[self.selected_class.get()]
        selection_text = 'Select \'{0}\' samples'.format(class_name)
        self.label.config(text = selection_text)
        
        class_color = CLASS_COLOR[self.selected_class.get()]
        self.notify_observers(class_color)
        
    def reset(self):
        self.samples = [[]] * MAX_NUMBER_OF_CLASSES
        self.select_default_class()

def greater_samples_were_taken(samples, class_number):
    for i in range(class_number, MAX_NUMBER_OF_CLASSES):            
        if samples[i]:
            return True
    return False

def _ask_to_reset_sample_collection():
    dialog_msg = ( 'All collected samples will be lost due to '
                   'you have selected an smaller number of class.\n'
                   'Do you want to continue?' )
    answer = askquestion('Sample Selection', dialog_msg, icon='warning')
    return answer