import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pickle
import glob
import cv2
# CameraCalibration class removes inherent distortions from the camera that can affect
# its perception of the world
class CameraCalibration:
    def __init__(self, nx, ny, cam_cal_dfp):
        # nx = corners for a row
        self.m_nx = nx
        # ny = corners for a column
        self.m_ny = ny
        self.m_cal_dfp = cam_cal_dfp
        # list of calibration images
        self.m_images = glob.glob(self.m_cal_dfp)
        self.m_objp = self.get_prepared_objp()
        # Arrays to store object points and image points from all the images
        self.m_objpoints, self.m_imgpoints = self.extract_obj_img_points()
    
    def get_prepared_objp(self):
        """
        Prepare object points, like (0,0,0), (1,0,0) ..., (6,5,0)
        """
        objp = np.zeros( (self.m_ny * self.m_nx, 3), np.float32 )
        objp[:,:2] = np.mgrid[0:self.m_nx, 0:self.m_ny].T.reshape(-1,2)
        return objp
        
    def extract_obj_img_points(self):
        """
        Extract 3D Object Points and 2D Image Points
        """
        objpoints = [] # 3D points in real world space
        imgpoints = [] # 2D points in image plane
        # Step through calibration image list and find chessboard corners
        for counter_x, fname in enumerate(self.m_images):
            img = mpimg.imread(fname)
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
            ret, corners = cv2.findChessboardCorners(gray, (self.m_nx,self.m_ny), None)
            # As long as ret is True, then corners found
            if ret == True:
                # Extract object 3D and image 2D points
                objpoints.append(self.m_objp)
                imgpoints.append(corners)
                # Draw and display corners
                # cv2.drawChessboardCorners(img, (self.m_nx,self.m_ny), corners, ret)
                # write_name = "corners_found"+str(counter_x)+".jpg"
                # cv2.imwrite(write_name, img)
        return objpoints, imgpoints
    
    def cmpt_mtx_and_dist_coeffs(self, src_img_fpath):
        """
        Compute Camera Calibration Matrix and Distortion Coefficients using a set of
        chessboard images (initial), then curved lane line images.
        
        Returns distorted image, camera calibration matrix and distortion coefficients
        """
        # Test undistortion on a distorted image
        dist_img = mpimg.imread(src_img_fpath)
        # Get image size, which will be needed for calibrateCamera()
        img_size = (dist_img.shape[1], dist_img.shape[0])
        # Do camera calibration given object 3D points and image 2D points
        ret, mtx, dist_coeff, rvecs, tvecs = cv2.calibrateCamera(self.m_objpoints,
                                              self.m_imgpoints, img_size, None, None)    
        return mtx, dist_coeff
    
    def correct_distortion(self, src_img_fpath, mtx, dist_coeff):
        """
        Apply Distortion Correction on an image by passing computed camera calibration
        matrix and distortion coefficients into undistort().
        
        Returns distorted image and undistorted image
        """
        # Test undistortion on a distorted image
        dist_img = mpimg.imread(src_img_fpath)
        # Using camera calibration matrix and distortion coefficients to undistort img
        undist_img = cv2.undistort(dist_img, mtx, dist_coeff, None, mtx)
        # Retrieve distorted image and undistorted image
        return dist_img, undist_img
    
    def save_undistorted_img(self, dst_img_fpath, dst_img, mtx, dist_coeff):
        """
        Save undistorted image using OpenCV and then pickle
        """
        # Save tested image after corrected distortion
        cv2.imwrite(dst_img_fpath + ".jpg", dst_img)
        # Save camera calibration result for later use
        dist_pickle = {}
        # Camera Matrix is used to perform transformation from distorted to undistorted
        dist_pickle["mtx"] = mtx
        dist_pickle["dist"] = dist_coeff
        pickle.dump( dist_pickle, open(dst_img_fpath + "_pickle.p", "wb") )    
    
    def visualize_undistortion(self, src_img, dst_img):
        """
        Visualize original distorted image and undistorted image using Matplotlib
        """
        f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20,10))
        ax1.imshow(src_img)
        ax1.set_title("Original Image", fontsize=30)
        ax2.imshow(dst_img)
        ax2.set_title("Undistorted Image", fontsize=30)