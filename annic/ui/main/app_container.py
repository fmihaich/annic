import os
from Tkinter import Tk, Frame
from annic.ui.main.menu_bar import AnnicMenuBar
from annic.ui.file_management.image_file import OpenImage, save_image_file
from annic.ui.image_processing.classification_menu import EmptyClassificationMenu, \
                                                          KMeansClassificationMenu, \
                                                          SOMClassificationMenu, \
                                                          PerceptronClassificationMenu
from annic.ui.image_processing.validation_menu import ConfusionMatrixMenu
from annic.ui.image_viewer.original_image import OriginalImage
from annic.ui.image_viewer.classified_image import ClassifiedImage


class AnnicMainContainer(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.root = root
        
        self._define_window_configuration(root)
        self._add_menu_bar(root)
        self.pack(fill='both', expand = 1)

        self.image_processing_menu = EmptyClassificationMenu(self)
        self.image_processing_menu.pack(side = 'left', expand = False)
        
        self.images = Images(self)
        self.images.pack(side = 'right', fill = 'both', expand = True)
        
        self.open_image = OpenImage(root)
        self.open_image.register_observer(self.images.original_img)


    def _define_window_configuration(self, root):
        current_dir = os.path.dirname(__file__)
        icon_path = os.path.join(current_dir, 'icon', 'neuron.ico')
         
        root.geometry("800x650")
        root.title("Artificial Neuronal Network Image Classification")
        root.iconbitmap(default=icon_path)

    def _add_menu_bar(self, root):
        menu_bar = AnnicMenuBar(root, self)
        root.config(menu = menu_bar)
        
    def on_open_image(self):
        self.images.classified_img.reset()
        self.open_image.run()
        
    def on_save_classified_image(self):
        classified_img = self.images.classified_img.image
        save_image_file(self, classified_img)
        
    def on_exit_from_application(self):
        self.root.quit()

    def on_apply_som_algorithm(self):
        self._refresh_image_processing_menu(menu = SOMClassificationMenu, 
                                            image = self.images.original_img.get())
        self._set_classification_observers(collection_per_class = False)
        print "Menu SOM"
        
    def on_apply_perceptron_algorithm(self):
        self._refresh_image_processing_menu(menu = PerceptronClassificationMenu,
                                            image = self.images.original_img.get())
        self._set_classification_observers(collection_per_class = True)
        print "Menu Perceptron"
        
    def on_apply_k_means_algorithm(self):
        self._refresh_image_processing_menu(menu = KMeansClassificationMenu,
                                            image = self.images.original_img.get())
        self._set_classification_observers(collection_per_class = False)
        print "Menu K-means"
            
    def on_calculate_confusion_matrix(self):
        self._refresh_image_processing_menu(menu = ConfusionMatrixMenu,
                                            image = self.images.classified_img.get())
        self._set_collection_per_class_observer()
        print "Menu confusion matrix"
        
        
    def _refresh_image_processing_menu(self, menu, image):
        self.images.original_img.reset()
        self.image_processing_menu.pack_forget()
        self.image_processing_menu = menu(self, image)
        self.image_processing_menu.pack(side = 'left', anchor = 'w', padx = 5)
    
    def _set_classification_observers(self, collection_per_class = False):
        open_image = self.open_image
        image_processing_menu = self.image_processing_menu
        original_image = self.images.original_img
        classified_image = self.images.classified_img
        classifier = self.image_processing_menu.classifier
        samples_collector = self.image_processing_menu.samples_collector
        
        open_image.register_observer(image_processing_menu)
        original_image.register_data_observers(samples_collector)
        classifier.register_observer(classified_image)
        if collection_per_class:
            samples_collector.register_observer(original_image)
            
    def _set_collection_per_class_observer(self):
        original_image = self.images.original_img
        samples_collector = self.image_processing_menu.samples_collector
            
        original_image.register_coordinates_observers(samples_collector)
        samples_collector.register_observer(original_image)




class Images(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        
        self.original_img = OriginalImage(self)
        self.original_img.pack(side = 'left', expand = True, anchor = 'center')
        
        self.classified_img = ClassifiedImage(self)
        self.classified_img.pack(side = 'right', expand = True, 
                                 anchor = 'center')         
    @property
    def original_img(self):
        return self.original_img
        
    @property
    def classified_img(self):
        return self.classified_img
               
        


class AnnicUI(object):
    def __init__(self):
        self.root = Tk()
        AnnicMainContainer(self.root)
        
    def run(self):
        self.root.mainloop()


