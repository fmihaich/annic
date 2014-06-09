from Tkinter import Menu

def AnnicMenuBar(root, main_frame):
    menu_bar = Menu(root)
    
    file_menu = FileMenu(main_frame, menu_bar)
    classification_menu = getClassificationMenu(main_frame, menu_bar)
    validation_menu = getValidationMenu(main_frame, menu_bar)
    
    menu_bar.add_cascade(label = 'File', menu = file_menu.get())
    menu_bar.add_cascade(label = 'Classify', menu = classification_menu)
    menu_bar.add_cascade(label = 'Validate', menu = validation_menu)

    return menu_bar

class FileMenu(object):
    def __init__(self, main_frame, menu_bar):
        self.menu = Menu(menu_bar, tearoff=0)
        
        self.menu.add_command(label = 'Open image', 
                              command = main_frame.on_open_image)
        self.menu.add_command(label = 'Save classified image', 
                              command = main_frame.on_save_classified_image)
        
        self.menu.add_separator()
        
        self.menu.add_command(label = 'Exit', 
                              command = main_frame.on_exit_from_application)
        
    def get(self):
        return self.menu


def getClassificationMenu(main_frame, menu_bar):
    menu = Menu(menu_bar, tearoff=0)
    
    menu.add_command(label = 'SOM classification', 
                     command = main_frame.on_apply_som_algorithm)
    menu.add_command(label = 'Perceptron classification',
                     command = main_frame.on_apply_perceptron_algorithm)
    
    menu.add_separator()
    menu.add_command(label = 'K-means classification',
                     command = main_frame.on_apply_k_means_algorithm)
    
    return menu

def getValidationMenu(main_frame, menu_bar):
    menu = Menu(menu_bar, tearoff=0)

    menu.add_command(label = 'Confusion matrix', 
                     command = main_frame.on_calculate_confusion_matrix)
    
    return menu
