# Artificial Neural Network Image Classification (ANNIC)


Description
-----
This software is able to explore no traditional image classification algorithms based on artificial neural networks (ANN), in particular, using Perceptron ANN and SOM ANN.
The product's aim is to compare the effectiveness and efficiency of these methods that are not based on any 
precondition against traditional categorization methods such as K-means classification algorithm.


General Capacities
-----
ANNIC system allows users to classify digital images using any of the following supervised methods: ANN Perceptron, ANN SOM or K-means algorithm.
Moreover, ANNIC software provides the possibility to evaluate the quality of the classification through the calculation of a confusion matrix based on the classified image and the related Kappa coefficient.


Required libraries
-----
In order to use the application, the following python distributable libraries are required:

- [neurolab](https://pypi.python.org/pypi/neurolab)
- [numpy](https://pypi.python.org/pypi/numpy)
- [PIL](http://www.pythonware.com/products/pil/)
- [csipy](http://www.scipy.org/install.html)


How to run
-----
In order to run ANNIC product execute the following command in annic working directory:

	python annic.py

In order to run annic stress test execute the following command in annic working directory:

	python stress_test.py --algorithm <algorithm_name> --data <data_option> --iterations <iterations_number> --output <output_file_path>

To get help about stress test options run:

	python stress_test.py --help
