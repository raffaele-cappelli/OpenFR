import numpy as np
import cv2 as cv
import json


# Segmentation parameters
class Parameters(dict):

    def __init__(self, window_size = 9, percentile = 95, threshold = 0.25, closing_count = 9, opening_count = 15):
        self.window_size = window_size
        self.percentile = percentile
        self.threshold = threshold
        self.closing_count = closing_count
        self.opening_count = opening_count

    def __repr__(self):
        d = {k:round(v,2) if isinstance(v,float) else v for k,v in self.__dict__.items()}
        return str(d)

    def save(self, path):
        with open(path, 'w') as file:
            json.dump(self.__dict__, file)        


# Load Parameters object from file
def load_parameters(path):
    with open(path, 'r') as file:
        return Parameters(**json.load(file))

    
# Segmentation algorithm
def run(img, parameters = Parameters(), intermediate_results = False):
    
    if intermediate_results: ir = []
    
    # Calculates gradient magnitude    
    gx, gy = cv.spatialGradient(img)
    sm = cv.magnitude(gx.astype(np.float32), gy.astype(np.float32))
    if intermediate_results: ir += [(sm, 'Gradient magnitude')]
    
    # Integral on parameters.window_size x parameters.window_size neighborhood
    r = cv.boxFilter(sm, -1, (parameters.window_size, parameters.window_size), normalize = False)
    if intermediate_results: ir += [(r, 'Sum over the window')]
    
    # Apply the threshold to the gradient magnitude at the required percentile (integrated over the window)
    norm_t = np.percentile(sm, parameters.percentile) * parameters.window_size * parameters.window_size * parameters.threshold
    
    # Selects pixels with gradient magnitude above the normalized threshold
    mask = cv.threshold(r, norm_t, 255, cv.THRESH_BINARY)[1].astype(np.uint8)
    if intermediate_results: ir += [(np.copy(mask), 'Thresholding')]
    
    if parameters.closing_count > 0:
        # Applies closing to fill small holes and gulfs
        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, _se3x3, iterations = parameters.closing_count)        
        if intermediate_results: ir += [(np.copy(mask), 'After closing')]
        
    # Remove all but the largest component
    _remove_other_cc(mask)
    if intermediate_results: ir += [(np.copy(mask), 'Largest component')]    
    
    # Use connected components labeling to fill holes (except those connected to the image border)
    _, cc, stats, _ = cv.connectedComponentsWithStats(cv.bitwise_not(mask))
    h, w = img.shape
    index_small = np.where(
        (stats[:,cv.CC_STAT_LEFT] > 0) &
        (stats[:,cv.CC_STAT_LEFT] + stats[:,cv.CC_STAT_WIDTH] < w-1) &
        (stats[:,cv.CC_STAT_TOP] > 0) &
        (stats[:,cv.CC_STAT_TOP] + stats[:,cv.CC_STAT_HEIGHT] < h-1)
        )
    mask[np.isin(cc, index_small)] = 255
    if intermediate_results: ir += [(np.copy(mask), 'After fill holes')]
    
    if parameters.opening_count > 0:
        # Applies opening to remove small blobs and protrusions
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, _se3x3, iterations = parameters.opening_count)    
        if intermediate_results: ir += [(np.copy(mask), 'After opening')]
    
    # The previous step may have created more cc: keep only the largest
    _remove_other_cc(mask)
    
    return (mask, ir) if intermediate_results else mask



    
def _remove_other_cc(mask):
    num, cc, stats, _ = cv.connectedComponentsWithStats(mask)
    if num > 1:
        index = np.argmax(stats[1:,cv.CC_STAT_AREA]) + 1
        mask[cc!=index] = 0        

_se3x3 = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3, 3))
