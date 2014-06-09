from tkFileDialog import askopenfilename, asksaveasfilename
import Image

import tkMessageBox

def displayOption():
    """ Display the OptionMenu selection. """
    global optionMenuWidget, DEFAULTVALUE_OPTION
    if (optionMenuWidget.cget("text") == DEFAULTVALUE_OPTION):
        tkMessageBox.showerror("Tkinter OptionMenu Widget", "Select a valid option.")
    else:
        tkMessageBox.showinfo("Tkinter OptionMenu Widget", "OptionMenu value =" + optionMenuWidget.cget("text"))

class OpenImage(object):
    def __init__(self, parent):
        self.parent = parent
        self.observers = []
        
    def register_observer(self, observer):
        self.observers.append(observer)
    
    def _notify_observers(self, image):
        for observer in self.observers:
            observer.set_image(image)
            
    def run(self):
        file_types = [('Image Files', '*.tif *.jpg *.png')]
        try:
            path = askopenfilename(parent = self.parent, filetypes = file_types,
                                   title='Choose an image file')
            image = Image.open(path)
            self._notify_observers(image)
        except IOError:
            tkMessageBox.showerror("Open Image", 
                    "Ensure you have selected a valid and existing image file")

    
def save_image_file(parent, img):
    file_types = [('Image Files', '*.tif *.jpg *.png')]
    file_path = asksaveasfilename(parent = parent, 
                                  title='Save classified image as', 
                                  filetypes = file_types,
                                  initialfile = 'classified_image.jpg')
    if file_path:
        img.save(file_path, 'JPEG')
