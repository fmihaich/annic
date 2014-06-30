"""

SAVE CONFUSION MATRIX

===================
This module allows user to save confusion matrix and Kappa coefficient.
-------------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

from tkFileDialog import asksaveasfilename
import numpy as np

def save_validation_results(parent, matrix, kappa):
    file_types = [('Text Files', '*.txt')]
    file_path = asksaveasfilename(parent = parent, 
                                  title='Save validation results as', 
                                  filetypes = file_types,
                                  initialfile = 'validation_results.txt')
    print "** confusion matrix path: ", file_path
    np.set_printoptions(precision=2)
    if file_path:
        with open(file_path, 'w') as outfile:
            np.savetxt(outfile, matrix, fmt='%-7.2f')
            outfile.write('\nKappa coefficient: {0}'.format(kappa))
