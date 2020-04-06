try:
	import cv2
except:
	cv2 = None

def live_video(source=0,color_mode=None,resize=None,preprocess_function=None):
	"""
	Displays live stream on window. You can press `q` to stop.
	Parameters:
		source: Camera port default is 0
		color_mode: convert image to 'rgb' or 'grayscale'
		resize: (height , width) tuple resize incoming video frame
		preprocess_function: Submit preprocessing function if you need extra preprocessing for image
		Preprocessing Function Syntax:
		#defining function
		def preprocessing_function(frame): #RGB frame as input
			// do preprocessing stuff here
			return processed_frame (image as ndarray)

		#submitting to nv.live_video()
		nv.live_video(preprocessing_function)
	"""

	if cv2 is None:
		raise ImportError('OpenCV is required for running this function\n'
			'Please install cv2 using `pip install opencv-python`')

	video = cv2.VideoCapture(source)

	frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	while True:
		# Capture frame-by-frame
		retval, frame = video.read()

		if resize is not None:
			if not isinstance(resize, tuple):
				raise ValueError(f'resize must be tuple of (height,width) but got {resize} instead')
			if (frame_height,frame_width) != resize:
				frame = cv2.resize(frame,resize)
		
		if color_mode is not None:
			if color_mode == 'rgb':
				frame = frame[...,::-1] #convert image to RGB
			elif color_mode == 'grayscale':
				frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #convert image to grayscale
			else:
				raise ValueError(f'Expected color_mode to be `rgb` or `grayscale` or None but got {color_mode} instead')
		if callable(preprocess_function): #check if preprocess_function is present
			frame = preprocess_function(frame)

		# Display the resulting frame
		cv2.imshow('frame', frame) #show image on screen

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything is done, release the capture
	video.release()
	cv2.destroyAllWindows()