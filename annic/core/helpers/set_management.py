import numpy as np

MAX_PIXEL_ND = 255

def optimize_set(org_set, class_number):
    """ Mix elements of training set in order to do not have together elements
        of a possible same class.
        For example: 
            If original set is [1, 1, 2, 2, 3, 3] and class number is 
            Then, optimize method returns [1, 2, 3, 1, 2, 3]            
    """
    org_set.sort()
    shift = len(org_set)/class_number
    
    optimized_set = [org_set[i+shift*j] for i in range(shift) \
                    for j in range(class_number)]
    
    if len(org_set)-shift*class_number != 0:
        optimized_set.extend(org_set[-(len(org_set)-shift*class_number):])
        
    return optimized_set    


def normalize_pixel_set(org_set):
    """ Normalize pixel data. The return set will be a list of lists.
        For example:
            - For [(a, b, c)] the result will be [[norm_a, norm_b, norm_c]]
            - For [a, b] the result will be [[norm_a], [norm_b]]            
    """
    return [np.atleast_1d(np.array(pixel_nd)/float(MAX_PIXEL_ND)).tolist()
            for pixel_nd in org_set]


def get_pixel_set_from_normalized_set(normalized_set):
    """ Get a pixel set from a normalized pixel set.
        Examples of returned values are:
            - For [[norm_a, norm_b, norm_c]] the result will be [(a, b, c)]
            - For [[norm_a], [norm_b]] the result will be [a, b]            
    """
    pixel_size = normalized_set.size / len(normalized_set)
    
    if pixel_size == 1:
        return [int((np.array(value)*MAX_PIXEL_ND).astype(int))
                for value in normalized_set]  
           
    return [tuple((np.array(value)*MAX_PIXEL_ND).astype(int))
            for value in normalized_set]
