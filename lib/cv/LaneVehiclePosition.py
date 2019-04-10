import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

# LaneVehiclePosition calculates vehicle's position with respect to the center
# of the lane

class LaneVehiclePosition:
    def __init__(self):
        """
            Initializes conversion from pixels to meters
        """
        # Camera image has 720 relevant pixels or 30 meters long in the y-dimension
        self.ym_per_pix_m = 30/720 # Meters per Pixel in y dimension
        
        # Camera image has 700 relevant pixels or 3.7 meters wide in the x-dimension
        # 200 pixels were used on the left and 900 on the right
        self.xm_per_pix_m = 3.7/700 # Meters per Pixel in x dimension
        
    def measure_vehicle_position(self, binary_warped, left_fit, right_fit, unit_type):
        """
            Determines vehicle's distance from center of the lane
        """
        imshape = binary_warped.shape
        img_h = imshape[0]
        img_w = imshape[1]
        
        # Vehicle position with respect to camera mounted at the center of the car
        vehicle_position = img_w/2
        
        # Calculate x-intercept for the left and right polynomial
        left_fit_x_int = left_fit[0]*img_h**2 + left_fit[1]*img_h + left_fit[2]
        right_fit_x_int = right_fit[0]*img_h**2 + right_fit[1]*img_h + right_fit[2]
        
        # Calculate lane center position from x-intercepts
        lane_center_position = (left_fit_x_int + right_fit_x_int)/2
        
        # Calculate vehicle's distance from center of lane in pixels or meters
        if(unit_type == "pixels"):
            self.dist_center_m = np.abs(vehicle_position - lane_center_position)
            self.units_m = "(p)"
        elif(unit_type == "meters"):
            self.dist_center_m = np.abs(vehicle_position - lane_center_position)*self.xm_per_pix_m
            self.units_m = "(m)"
        else:
            self.dist_center_m = "undefined"
            
        # Check if vehicle's position is left to center or right to center
        if(lane_center_position > vehicle_position):
            # Side of center that the vehicle is on
            self.side_center_m = "left of center"
        else:
            self.side_center_m = "right of center"
        
        return self.dist_center_m, self.units_m, self.side_center_m
    
    def display_vehicle_position(self):
        """
            Displays to screen vehicle's position with respect to center
        """
        print("Vehicle is %.2f %s %s" %(self.dist_center_m, self.units_m, self.side_center_m))