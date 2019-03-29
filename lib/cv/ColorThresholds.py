import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import cv2

# Color space is a specific organization of colors
# They provide a way to categorize colors and represent them in digital images

# RGB Thresholding doesn't work well under varying light conditions
# or under varying color like yellow

# HLS Thresholding isolates lightness (L), which varies most under
# different lighting conditions.
# H and S channels stay consistent in shadow or excessive brightness

# HLS can be used to detect lane lines of different colors under
    # different lighting conditions

# Hue - represents color independent of any change in brightness
# Lightness and Value - represent different ways to measure relative
    # lightness or darkness of a color
# Saturation - measurement of colorfulness
    # As colors get lighter (white), their saturation value is lower
    # Most intense colors (bright red, blue , yellow) have high saturation

class ColorThresholds:
    # Apply Grayscale Thresholding
    def apply_gray_thresh(self, img, thresh = (0, 255)):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        binary_img = np.zeros_like(gray)
        binary_img[ (gray > thresh[0]) & (gray <= thresh[1]) ] = 1
        return binary_img
    
    # Thresholding individual RGB Color Channels
    def apply_r_thresh(self, img, thresh = (0, 255)):
        r_img = img[:,:,0]
        binary_img = np.zeros_like(r_img)
        binary_img[ (r_img > thresh[0]) & (r_img <= thresh[1]) ] = 1
        return binary_img
    
    def apply_g_thresh(self, img, thresh = (0, 255)):
        g_img = img[:,:,1]
        binary_img = np.zeros_like(g_img)
        binary_img[ (g_img > thresh[0]) & (g_img <= thresh[1]) ] = 1
        return binary_img        

    def apply_b_thresh(self, img, thresh = (0, 255)):
        b_img = img[:,:,2]
        binary_img = np.zeros_like(b_img)
        binary_img[ (b_img > thresh[0]) & (b_img <= thresh[1]) ] = 1
        return binary_img  
    
    # Apply Combined RGB Thresholding
    def apply_rgb_thresh(self, img, thresh = [(0, 255), (0, 255), (0, 255)]):
        r_binary = self.apply_r_thresh(img, thresh[0])
        g_binary = self.apply_g_thresh(img, thresh[1])
        b_binary = self.apply_b_thresh(img, thresh[2])
        combined = np.zeros_like(b_binary)
        combined[ (r_binary == 1) & (g_binary == 1) & (b_binary == 1) ] = 1
        return combined
    
    # Thresholding individual HSL Color Channels
    def apply_h_thresh(self, img, thresh = (0, 255)):
        h_img = img[:,:,0]
        binary_img = np.zeros_like(h_img)
        binary_img[ (h_img > thresh[0]) & (h_img <= thresh[1]) ] = 1
        return binary_img
    
    def apply_l_thresh(self, img, thresh = (0, 255)):
        l_img = img[:,:,1]
        binary_img = np.zeros_like(l_img)
        binary_img[ (l_img > thresh[0]) & (l_img <= thresh[1]) ] = 1
        return binary_img
    
    def apply_s_thresh(self, img, thresh = (0, 255)):
        s_img = img[:,:,2]
        binary_img = np.zeros_like(s_img)
        binary_img[ (s_img > thresh[0]) & (s_img <= thresh[1]) ] = 1
        return binary_img
    
    # Apply Combined HLS Thresholding
    def apply_hls_thresh(self, img, thresh = [(0, 255), (0, 255), (0, 255)]):
        h_binary = self.apply_h_thresh(img, thresh[0])
        l_binary = self.apply_l_thresh(img, thresh[1])
        s_binary = self.apply_s_thresh(img, thresh[2])
        combined = np.zeros_like(s_binary)
        combined[ (h_binary == 1) & (l_binary == 1) & (s_binary == 1) ] = 1
        return combined
    
    def visualize_thresholded_img(self, undist_img, binary_img, undist_img_title, thresh_img_title):
        """
        Visualize color thresholded image
        """
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24,9))
        f.tight_layout()
        ax1.imshow(undist_img)
        ax1.set_title(undist_img_title, fontsize=50)
        ax2.imshow(binary_img, cmap = 'gray')
        ax2.set_title(thresh_img_title, fontsize=50)
        plt.subplots_adjust(left=0, right=1, top=0.9, bottom=0.)