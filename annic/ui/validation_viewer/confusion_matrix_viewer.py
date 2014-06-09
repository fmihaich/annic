from Tkinter import Frame, Label, Button, Toplevel, Entry, StringVar

DEFAULT_FONT = ('Arial', 10)
BOLD_FONT = ('Arial', 10, 'bold')
DEFAULT_WIDTH = 10


class ConfusionMatrixViewer():
    def __init__(self, class_number, matrix, kappa):
        self.class_number = class_number
        self.matrix = matrix
        self.kappa = kappa
        
        self.child_window = Toplevel(height = 800, width = 1500)
        self.child_window.title('Verification of image classification')
        
    def run(self):
        confusion_matrix_table = ConfusionMatrixTable(self.child_window, 
                                                self.class_number, self.matrix)
        confusion_matrix_table.pack(padx = 5, pady = 5)
        
        kappa_label = Label(self.child_window, font = BOLD_FONT,
                            text = 'Kappa Coefficient: {0}'.format(self.kappa))
        kappa_label.pack(anchor = 'w', padx = 5)
        
        save_button = Button(self.child_window, text = 'Save Validation', 
                             relief = 'raised', width = 30,
                             command = self._save_validation)
        save_button.pack(anchor = 'center', padx = 5, pady = 5)
        
    def _save_validation(self):
        pass


class ConfusionMatrixTable(Frame):
    def __init__(self, parent, class_number, matrix):
        Frame.__init__(self, parent)
        self.class_number = class_number
        self.matrix = matrix
        self.grid()
        
        class_names = [str(i) for i in range(1, class_number + 1)]
        self.row_header = class_names + ['Total', 'Rightness', 'C. Error']
        self.column_header = class_names + ['Total', 'Rightness', 'O. Error']
        self.column_header.insert(0, '')
        
        self._comple_table_headers()
        self._compcomple_table_data()
        
    def _comple_table_headers(self):        
        for i, label in enumerate(self.column_header):
            TableHeader(self, i, 0, label)
        for i, label in enumerate(self.row_header):
            TableHeader(self, 0, i+1, label)
            
    def _compcomple_table_data(self):        
        for i in range(1, len(self.column_header)):
            for j in range(1, len(self.row_header) + 1):
                if i-1 < self.class_number and j-1 < self.class_number:
                    TableData(self, i, j, '%d' % self.matrix[i-1][j-1])
                elif i-1 == self.class_number and j-1 <= self.class_number:
                    TableBoldData(self, i, j, '%d' % self.matrix[i-1][j-1])
                elif j-1 == self.class_number and i-1 <= self.class_number:
                    TableBoldData(self, i, j, '%d' % self.matrix[i-1][j-1])
                else:
                    msg = '%0.2f' % self.matrix[i-1][j-1]
                    msg = msg + '%' if msg != 'nan' else ''
                    TableData(self, i, j, msg)

class TableElement(Entry):
    def __init__(self, master, x, y, text):
        Entry.__init__(self, master = master)
        
        self.text = StringVar()
        self.text.set(text)
        self.config(relief = 'ridge', justify = 'center', width = DEFAULT_WIDTH,
                    textvariable = self.text, state = 'readonly')
        self.grid(column = x, row = y)
        
class TableHeader(TableElement):
    def __init__(self, master, x, y, text):
        TableElement.__init__(self, master, x, y, text)
        self.config(font = BOLD_FONT, bg = 'navy', fg = 'white',
                    readonlybackground = 'navy',)
        
class TableData(TableElement):
    def __init__(self, master, x, y, text):
        TableElement.__init__(self, master, x, y, text)
        self.config(font = DEFAULT_FONT)
        
class TableBoldData(TableElement):
    def __init__(self, master, x, y, text):
        TableElement.__init__(self, master, x, y, text)
        self.config(font = BOLD_FONT)
