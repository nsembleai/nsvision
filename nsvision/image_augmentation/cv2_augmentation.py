import cv2
from skimage.exposure import rescale_intensity
from skimage.segmentation import slic
from skimage.util import img_as_float
from skimage import io
import numpy as np
import os
import argparse
import os.path


class ImageAugmentation():
	def __init__(self, image_path, dst_path):
		self.image_path = image_path				# input image path
		self.dst_path = dst_path					# Augmented image saving path

    # FILP
	def flip_image(self, flip_angle = 0):			# flip the image around horizontally or vertically
		if os.path.isfile(self.image_path):			# flip_angle = 0 - Vertical flip 
			img = cv2.imread(self.image_path)		# flip_angle = 1 - Horizontal flip
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			flipimage = cv2.flip(np.array(img), flip_angle)
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_flip' + str(flip_angle) + image_ext), flipimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for fl in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, fl))
				dst_image = os.path.join(self.dst_path, fl)
				flipimage = cv2.flip(np.array(img), flip_angle)
				image_name = os.path.splitext(os.path.basename(fl))[0]
				image_ext = os.path.splitext(os.path.basename(fl))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_flip' + str(flip_angle) + image_ext), flipimage)


	# BILETERAL BLUR
	def bileteralBlur(self, a, b, c):
		# first parameter(a) is the image we want to blur
		# second parameter(b) is the diameter of our pixel neighborhood.
		# third parameter(c) is for color.
		# blurring methods has been to reduce noise and detail in an image.
		# to reduce noise while still maintaining edges, we can use bilateral blurring
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			bilateral = cv2.bilateralFilter(np.array(img),a,b,c)
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_bilateral' + str(a) + str(b) + str(c) + image_ext), bilateral)
		else:
			if not self.dst_path:
				dst = self.image_path
			for bl in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, bl))
				dst_image = os.path.join(self.dst_path, bl)
				bilateral = cv2.bilateralFilter(np.array(img),a,b,c)
				image_name = os.path.splitext(os.path.basename(bl))[0]
				image_ext = os.path.splitext(os.path.basename(bl))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_bileteral' + str(a) + str(b) + str(c) + image_ext), bilateral)
		return bilateral
		

	# AVERAGING BLUR
	def averagingBlur(self, x):
		# as the size (x = (k * k)) of the Averaging(kernel) increases, the more blurred our image will become.
		# This function requires two arguments: first k - the image we want to blur and second k - the size of the kernel.
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			average = cv2.blur(np.array(img),x)
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_average' + str(x) + image_ext), average)
		else:
			if not self.dst_path:
				dst = self.image_path
			for avg in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, avg))
				dst_image = os.path.join(self.dst_path, avg)
				average = cv2.blur(np.array(img),x)
				image_name = os.path.splitext(os.path.basename(avg))[0]
				image_ext = os.path.splitext(os.path.basename(avg))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_average' + str(x) + image_ext), average)
		return average


	# RESIZE
	def resize_image(self,w,h):
		# Resize is exactly what it sounds like minimize or maximize the image size.
		# The aspect ratio is the proportional relationship of the width(w) and the height(h) of the image.
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			resizeimage = cv2.resize(np.array(img),(w,h))
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_resize' + str(w) + str(h) + image_ext), resizeimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for rs in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, rs))
				dst_image = os.path.join(self.dst_path, rs)
				resizeimage = cv2.resize(np.array(img), (w, h))
				image_name = os.path.splitext(os.path.basename(rs))[0]
				image_ext = os.path.splitext(os.path.basename(rs))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_resize' + str(w) + str(h) + image_ext), resizeimage)
		return resizeimage


    # ROTATE
	def rotate_image(self,deg):
		# Rotation is exactly what it sounds like: rotating an image by some angle θ
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			(h, w) = img.shape[:2]		# rotate around the center of the image.
			center = (w // 2, h // 2)   # w = width, h = height

			M = cv2.getRotationMatrix2D(center, deg, 1)  #matrix to rotate the image.
			# three arguments:1)Center point at which we want to rotate the image around
			# 2) specify θ(deg)
			# 3) regular size, minimize size and maximize size to rotate the image
			rotateimage = cv2.warpAffine(np.array(img), M, (w, h)) 
			# first argument to this function is the image we want to rotate.
			# second argument rotation matrix M 
			# Third argument along with the output dimensions (width and height)
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_rotate' + str(deg) + image_ext), rotateimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for rot in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, rot))
				(h, w) = img.shape[:2]		# rotate around the center of the image.
				center = (w // 2, h // 2)   # w = width, h = height
				dst_image = os.path.join(self.dst_path, rot)
				M = cv2.getRotationMatrix2D(center, deg, 1)
				rotateimage = cv2.warpAffine(np.array(img), M, (w, h))
				image_name = os.path.splitext(os.path.basename(rot))[0]
				image_ext = os.path.splitext(os.path.basename(rot))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_rotate' + str(deg) + image_ext), rotateimage)


	# CROP
	def crop_image(self,y1,y2,x1,x2):
		# crop image is to remove unnecessary part of the image.
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			cropimage = np.array(img)[y1:y2,x1:x2]
			# extract a rectangular region of the image(y1:y2, x1:x2)
			# the height first(y1:y2) and the width second(x1:x2)
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_crop' + str(y1) + str(y2) + str(x1) + str(x2) + image_ext), cropimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for crp in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, crp))
				dst_image = os.path.join(self.dst_path, crp)
				cropimage = np.array(img)[y1:y2,x1:x2]
				image_name = os.path.splitext(os.path.basename(crp))[0]
				image_ext = os.path.splitext(os.path.basename(crp))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_crop' + str(y1) + str(y2) + str(x1) + str(x2) + image_ext), cropimage)


	# GAUSSIAN
	def gausian_blur(self,blur):
		# Gaussian blurring is similar to average blurring. 
		# The end result is that image is less blurred, but more naturally blurred.
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			gausianimage = cv2.GaussianBlur(np.array(img),(5,5),blur)
			# The first argument to the function is the image we want to blur
			# The second argument we provide a tuple representing our kernel size.
			# The last parameter is our σ, the standard deviation in the x-axis direction.
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_gausian' + str(blur) + image_ext), gausianimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for gau in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, gau))
				dst_image = os.path.join(self.dst_path, gau)
				gausianimage = cv2.GaussianBlur(np.array(img),(5,5),blur)
				image_name = os.path.splitext(os.path.basename(gau))[0]
				image_ext = os.path.splitext(os.path.basename(gau))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_gausian' + str(blur) + image_ext), gausianimage)


	# MEDIAN
	def median_blur(self,shift):
		# Median blurring is more effective at removing salt-and-pepper style noise from an image
		# because each central pixel is always replaced with a pixel intensity that exists in the image.
		if os.path.isfile(self.image_path):
			img = cv2.imread(self.image_path)
			if not self.dst_path:
				dst = os.path.split(self.image_path)[0]

			medianimage = cv2.medianBlur(np.array(img),shift)
			# two arguments: The first argument the image we want to blur 
			# The second argument the size of our kernel. 
			dst_image = os.path.join(self.dst_path, self.image_path)
			image_name = os.path.splitext(os.path.basename(self.image_path))[0]
			image_ext = os.path.splitext(os.path.basename(self.image_path))[1]		
			cv2.imwrite(os.path.join(self.dst_path, image_name + '_median' + str(shift) + image_ext), medianimage)
		else:
			if not self.dst_path:
				dst = self.image_path
			for med in os.listdir(self.image_path):
				img = cv2.imread(os.path.join(self.image_path, med))
				dst_image = os.path.join(self.dst_path, med)
				medianimage = cv2.medianBlur(np.array(img),shift)
				image_name = os.path.splitext(os.path.basename(med))[0]
				image_ext = os.path.splitext(os.path.basename(med))[1]		
				cv2.imwrite(os.path.join(self.dst_path, image_name + '_median' + str(shift) + image_ext), medianimage)