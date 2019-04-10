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
        
    def measure_radius_curvature(self, ploty, left_fit, right_fit, unit_type):
        """
            Calculates the curvature of polynomial functions in pixels or meters.
        """
        # y-value for where we want radius of curvature
        # Chose the max y-value,corresponding to bottom of image
        y_eval = np.max(ploty)

        # Generate x and y values for plotting
        left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
        right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]       

        # Fit new polynomials to x, y in real world space
        left_fit_rw = np.polyfit(ploty*self.ym_per_pix_m, left_fitx*self.xm_per_pix_m, 2)
        right_fit_rw = np.polyfit(ploty*self.ym_per_pix_m, right_fitx*self.xm_per_pix_m, 2)
        
        if(unit_type == "pixels"):
            # Calculates R-curve (radius of curvature)
            # Left Line R-curve
            self.left_curverad_m = ((1 + (2*left_fit[0]*y_eval + left_fit[1])**2)**1.5) / np.absolute(2*left_fit[0])
        
            # Right Line R-curve
            self.right_curverad_m = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])
            self.units_m = "(p)"
        elif(unit_type == "meters"):
            # Calculates R-curve (radius of curvature)
            # Left Line R-curve
            self.left_curverad_m = ((1 + (2*left_fit_rw[0]*y_eval*self.ym_per_pix_m + left_fit_rw[1])**2)**1.5) / np.absolute(2*left_fit_rw[0])
        
            # Right Line R-curve
            self.right_curverad_m = ((1 + (2*right_fit_rw[0]*y_eval*self.ym_per_pix_m + right_fit_rw[1])**2)**1.5) / np.absolute(2*right_fit_rw[0])
            self.units_m = "(m)"
        
        # Returns radius of lane curvature
        return self.left_curverad_m, self.right_curverad_m, self.units_m
        

    def display_radius_curvature(self):
        """
            Displays to screen lane curvature in pixels, meters, etc based on
            unit_type flag passed 
        """
        print("Left Lane Line Curvature Radius = %d %s" %(self.left_curverad_m, self.units_m))

        print("Right Lane Line Curvature Radius = %d %s" %(self.right_curverad_m, self.units_m))