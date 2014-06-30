"""

ANNIC STRESS TEST

================
This module allows user to execute stress test running the following command:
    - python stress_test.py --algorithm <algorithm_name> 
                            --data <data_option> 
                            --iterations <iterations_number> 
                            --output <output_file_path>
The stress method could Perceptron, SOM or K-means.
The stress data is defined in test data file based on available test images.
It also available a help menu executing:
    -  python stress_test.py --help
----------------

@author: Florencia Mihaich
@version: 1.0
@date: June 6th, 2014

"""

import argparse
from stress_tests.test import PerceptronStressTest, SOMStressTest, KMeansStressTest

DEFAULT_ITERATION_NUM = 100
DEFAULT_OUTPUT_FILE_NAME = 'stress_test_result.txt'

def main():
    args = _get_cmd_args()
    if not (args.algorithm and args.data):
        print 'Stress algorithm and data shall be provided. Show --help menu'
        return
    
    algorithm = args.algorithm
    data = args.data
    iterations = args.iterations if args.iterations else DEFAULT_ITERATION_NUM
    output = args.output if args.output else DEFAULT_OUTPUT_FILE_NAME
                                 
    stress_test = _get_stress_test(data, iterations, algorithm, output)
    if not stress_test:
        print 'Error getting stress test. Check input parameters in --help menu'
        return
    
    print 'Running {0} stress test for {1} data'.format(algorithm, data)           
    stress_test.run()


def _get_cmd_args():
    """ Retrieves all known command line arguments """
    parser = argparse.ArgumentParser(
                description='Image Classification Stress Test')
    parser.add_argument('--algorithm', choices=['perceptron', 'som', 'kmeans'],
                        help='Classification algorithm to execute')
    parser.add_argument('--data', choices=['boxes', '4colors'],
                        help='Image and data to use during stress test')
    parser.add_argument('--iterations', type = int, 
                        help='Times to run stress test')
    parser.add_argument('--output', 
                        help = 'File name to save stress test results')
    return parser.parse_args()


def _get_stress_test(data, iterations, algorithm, output):
    if algorithm == 'perceptron':
        return PerceptronStressTest(data, iterations, algorithm, output)
    
    if algorithm == 'som':
        return SOMStressTest(data, iterations, algorithm, output)
    
    if algorithm == 'kmeans':
        return KMeansStressTest(data, iterations, algorithm, output)
    
    return None


if __name__ == '__main__':
    main()