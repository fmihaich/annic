from Tkinter import Frame, Button
from annic.ui.file_management.image_file import save_image_file

class SaveClassifiedImage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.parent = parent
        self.classified_img = None
        
        self.save_button = Button(self, text = 'Save classified image', 
                                  relief = 'raised', width = 23,
                                  command=self._save_classified_image,
                                  state = 'disabled')
        self.save_button.pack()
        
    def set_classified_image(self, classified_img):
        self.classified_img = classified_img
        self.save_button.config(state = 'normal')
        
    def _save_classified_image(self):
        save_image_file(self, self.classified_img)
