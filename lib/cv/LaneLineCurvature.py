import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

class LaneLineCurvature:
    def __init__(self):
        """
            Initializes unit_type flag for curvature radius
            Initializes left and right curvature radius
            Initializes conversions from pixels to meters for y- and x-dimension
        """
        self.left_curverad_m = 0.0
        self.right_curverad_m = 0.0
        
        # Camera image has 720 relevant pixels or 30 meters long in the y-dimension
        self.ym_per_pix_m = 30/720 # Meters per Pixel in y dimension
        
        # Camera image has 700 relevant pixels or 3.7 meters wide in the x-dimension
        # 200 pixels were used on the left and 900 on the right
        self.xm_per_pix_m = 3.7/700 # Meters per Pixel in x dimension
        
    def measure_curvature_pixels(self, ploty, left_fit, right_fit):
        """
            Calculates the curvature of polynomial functions in pixels.
        """
        # y-value for where we want radius of curvature
        # Chose the max y-value,corresponding to bottom of image
        y_eval = np.max(ploty)
        
        # Calculates R-curve (radius of curvature)
        # Left Line R-curve
        self.left_curverad_m = ((1 + (2*left_fit[0]*y_eval + left_fit[1])**2)**1.5) / np.absolute(2*left_fit[0])
        
        # Right Line R-curve
        self.right_curverad_m = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])
        
        # Returns radius of lane curvature in pixels
        return self.left_curverad_m, self.right_curverad_m
        
    def measure_curvature_meters(self, ploty, left_fit_cr, right_fit_cr):
        """
            Calculates the curvature of polynomial functions in meters.
        """
        # y-value for where we want radius of curvature
        # Chose the max y-value,corresponding to bottom of image        
        y_eval = np.max(ploty)
        
        # Calculates R-curve (radius of curvature)
        # Left Line R-curve
        self.left_curverad_m = ((1 + (2*left_fit_cr[0]*y_eval*self.ym_per_pix_m + left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
        
        # Right Line R-curve
        self.right_curverad_m = ((1 + (2*right_fit_cr[0]*y_eval*self.ym_per_pix_m + right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])
        
        # Returns radius of lane curvature in meters
        return self.left_curverad_m, self.right_curverad_m        
        
    def display_curvature(self, unit_type):
        """
            Displays to screen lane curvature in pixels, meters, etc based on
            unit_type flag passed 
        """
        # Check unit type for radius of lane curvature
        if(unit_type == "pixels"):
            curverad_unit_type = "(pixels)"
        elif(unit_type == "meters"):
            curverad_unit_type = "(meters)"
        else:
            curverad_unit_type = "(undefined)"
            
        print("left_curverad = %s, right_curverad = %s, unit_type = %s" %(self.left_curverad_m, self.right_curverad_m, unit_type))