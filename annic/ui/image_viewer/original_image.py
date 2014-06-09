from Tkinter import Frame, Canvas
from ImageTk import PhotoImage
import Image
from annic.definitions import CLASS_COLOR

class OriginalImage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent
        
        self.orginal_img = Canvas(self)
        self.orginal_img.grid(row = 0, column = 0)
        
        self.orginal_img.bind('<ButtonPress-1>', self.on_mouse_down)
        self.orginal_img.bind('<B1-Motion>', self.on_mouse_drag)
        self.orginal_img.bind('<ButtonRelease-1>', self.on_mouse_up)
        self.orginal_img.bind('<Button-3>', self.on_right_click)
        
        self._set_variables_initial_state()
        
    def _set_variables_initial_state(self):
        self.drag_color = CLASS_COLOR[0]
        self.item = None
        self.data_observers = []
        self.coordinates_observers = []

    def get(self):
        try:
            return self.orginal_img.image
        except Exception:
            return None
        
    def register_data_observers(self, observers):
        self.data_observers.append(observers)
        
    def register_coordinates_observers(self, observers):
        self.coordinates_observers.append(observers)
        
    def _notify_data_observers(self, pixel_values):
        for observer in self.data_observers:
            observer.add_samples(pixel_values)
            
    def _notify_coordinates_observers(self, img_region):
        for observer in self.coordinates_observers:
            observer.add_sample_coordinates(img_region)

    def set_image(self, current_image):
        self.orginal_img.image = current_image
        
        self.orginal_img.photo = PhotoImage(self.orginal_img.image)
        
        self.orginal_img.create_image(0, 0, image = self.orginal_img.photo, 
                                      anchor = 'nw', tags = 'img')
        
        w, h = self.orginal_img.image.size
        self.orginal_img.config(width = w, height = h, 
                                scrollregion = self.orginal_img.bbox('all'))    
            
    def set_drag_color(self, color):
        self.drag_color = color
        
    def reset(self):
        try:
            self.orginal_img.create_image(0, 0, image = self.orginal_img.photo, 
                                          anchor = 'nw', tags = 'img')
            self._set_variables_initial_state()
        except AttributeError:
            # No image was previously opened
            pass
        
    def on_mouse_down(self, event):        
        self.anchor = (event.widget.canvasx(event.x),
                       event.widget.canvasy(event.y))
        self.item = None

    def on_mouse_drag(self, event):        
        bbox = self.anchor + (event.widget.canvasx(event.x),
                              event.widget.canvasy(event.y))
        if self.item is None:
            self.item = event.widget.create_rectangle(bbox,
                            outline = self.drag_color, fill = self.drag_color)
        else:
            event.widget.coords(self.item, *bbox)

    def on_mouse_up(self, event):        
        if self.item:
            self.on_mouse_drag(event) 

            box = tuple((int(round(v)) for v in event.widget.coords(self.item)))
            box = tuple([i if i>0 else 0 for i in box])

            img_region = self.orginal_img.image.crop(box)
            pixel_values = list(img_region.getdata())
            
            self._notify_data_observers(pixel_values)
            self._notify_coordinates_observers(box)
            

    def on_right_click(self, event):        
        found = event.widget.find_all()
        for iid in found:
            if event.widget.type(iid) == 'rectangle':
                event.widget.delete(iid)
        
