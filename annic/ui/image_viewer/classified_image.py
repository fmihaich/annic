from Tkinter import Frame, Label
from ImageTk import PhotoImage

class ClassifiedImage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self._set_no_image()
        
    @property
    def image(self):
        return self.classified_img.image
    
    def get(self):
        try:
            return self.classified_img.image
        except Exception:
            return None
        
    def set_classified_image(self, img):
        self.classified_img.image = img
        photo = PhotoImage(self.classified_img.image)
        self.classified_img.configure(image = photo)
        self.classified_img.photo = photo
        
    def reset(self):
        self.classified_img.pack_forget()
        self._set_no_image()
        
    def _set_no_image(self):
        self.classified_img = Label(self)
        self.classified_img.image = None
        self.classified_img.pack()